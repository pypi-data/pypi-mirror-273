from __future__ import annotations

import os
import subprocess
import sys
import time
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from pprint import pprint
from tempfile import NamedTemporaryFile
from threading import Thread
from typing import Any
from typing import Callable
from typing import IO
from typing import TypedDict

import click
from typing_extensions import NotRequired

from .background import Processing


def dict2conf(outfile: str, dictionary: dict[str, Any]) -> None:
    with open(outfile, "w", encoding="utf8") as fp:
        dict2conffp(fp, dictionary)


def dict2conffp(fp: IO, dictionary: dict[str, Any]) -> None:
    for k, v in dictionary.items():
        print(k, " = ", file=fp, end="")
        pprint(v, stream=fp)


class PopenArgs(TypedDict):
    process_group: NotRequired[int | None]
    creationflags: int
    preexec_fn: Callable[[], None] | None


@dataclass
class Runner:
    name: str
    cmd: list[str]
    directory: str = "."
    env: dict[str, str] | None = None
    showcmd: bool = False
    shell: bool = False
    prevent_sig: bool = False  # prevent Cntrl-C from propagating to child process

    def getenv(self) -> dict[str, str] | None:
        if not self.env:
            return None
        return {**os.environ, **self.env}

    def start(self) -> subprocess.Popen[bytes]:
        if self.showcmd:
            click.secho(" ".join(str(s) for s in self.cmd), fg="blue")

        kwargs = PopenArgs(creationflags=0, preexec_fn=None)
        if self.prevent_sig:
            if sys.platform == "win32":
                kwargs["creationflags"] = (
                    subprocess.DETACHED_PROCESS | subprocess.CREATE_NEW_PROCESS_GROUP
                )
            else:
                if sys.version_info >= (3, 11):
                    kwargs["process_group"] = 0
                else:
                    kwargs["preexec_fn"] = os.setpgrp
        return subprocess.Popen(  # type: ignore
            self.cmd,
            cwd=self.directory,
            env=self.getenv(),
            shell=self.shell,
            **kwargs,
        )


def browser(url: str = "http://127.0.0.1:8000", sleep: float = 5.0) -> Thread:
    import webbrowser

    def run() -> None:
        time.sleep(sleep)
        webbrowser.open_new_tab(url)

    tr = Thread(target=run)
    tr.daemon = True  # exit when main process exits
    tr.start()
    return tr


def has_package(package: str) -> bool:
    import importlib

    try:
        importlib.import_module(package)
        return True
    except ModuleNotFoundError:
        return False


def default_conf() -> dict[str, Any]:
    # from tempfile import gettempdir

    conf = {
        "MOUNTPOINTS": [
            ("~", "HOME"),
        ],
        "JOBSDIR": "~/turnover_jobs",
        "CACHEDIR": "~/turnover_cache",
        "WEBSITE_STATE": "single_user",
    }
    return conf


def instance_conf(config: str) -> dict[str, Any]:
    """We *must* have flask in our environment by now"""
    from flask import Config  # pylint: disable=import-error

    conf = Config(".")
    conf.from_pyfile(config)
    return conf


def webrunner(
    browse: bool,
    workers: int,
    web_config: str | None,  # ~/.turnover-web.cfg or commandline
    gunicorn: bool = False,
    *,
    view_only: bool = True,
    configfile: str | None = None,  # turnover config file
    defaults: dict[str, Any] | None = None,  # CACHEDIR etc. from commanline
    port: int = 8000,
    extra: tuple[str, ...] = (),  # extra commandline arguments after --
    flask_app: str = "protein_turnover_website.wsgi",
) -> None:
    """Run full website."""

    if not has_package("protein_turnover_website"):
        click.secho(
            "Please install protein_turnover_website [pip install protein-turnover-website]!",
            fg="red",
            err=True,
        )
        raise click.Abort()
    if gunicorn and not has_package("gunicorn"):
        click.secho(
            "Please install gunicorn [pip install gunicorn]!",
            fg="red",
            err=True,
        )
        raise click.Abort()

    fp = None
    web_conf = default_conf()
    if web_config:
        # just need JOBSDIR
        web_conf.update(instance_conf(web_config))

    if defaults is not None:
        web_conf.update(defaults)

    # need to read config file just for jobsdir
    jobsdir = Path(web_conf["JOBSDIR"]).expanduser()
    if not jobsdir.exists():
        jobsdir.mkdir(parents=True, exist_ok=True)

    cfg = [f"--config={configfile}"] if configfile is not None else []
    if not view_only:
        background = Runner(
            "background",
            [
                sys.executable,
                "-m",
                "protein_turnover",
                *cfg,
                "--level=info",
                "background",
                f"--workers={workers}",
                "--no-email",
                str(jobsdir),
            ],
            directory=".",
            prevent_sig=True,
        )
    Url = f"127.0.0.1:{port}"
    with NamedTemporaryFile("w+t") as fp:
        dict2conffp(fp, web_conf)
        fp.flush()

        if not gunicorn:
            website = Runner(
                "flask",
                [
                    sys.executable,
                    "-m",
                    "flask",
                    "--app",
                    flask_app,
                    "run",
                    f"--port={port}",
                    *extra,
                ],
                env={"TURNOVER_SETTINGS": fp.name, "FLASK_DEBUG": "0"},
                prevent_sig=True,
            )
        else:
            website = Runner(
                "gunicorn",
                [
                    sys.executable,
                    "-m",
                    "gunicorn",
                    f"--bind={Url}",
                    *extra,
                    flask_app,
                ],
                env={"TURNOVER_SETTINGS": fp.name},
                prevent_sig=True,
            )
        if view_only:
            procs = [website]
        else:
            procs = [background, website]
        # handler = InterruptHandler()
        threads = [(p.name, p.start()) for p in procs]

        if browse:
            browser(url=f"http://{Url}", sleep=5.0)

        worker = Processing(jobsdir)
        ninterrupts = 0
        prev = datetime.now()
        while True:
            try:
                time.sleep(100.0)

            except KeyboardInterrupt:
                # too long between ^C
                now = datetime.now()
                if ninterrupts > 0 and (now - prev).total_seconds() > 5:
                    ninterrupts = 0
                    prev = now
                    continue
                ninterrupts += 1
                if ninterrupts >= 2:
                    for name, tr in threads:
                        try:
                            click.secho(f"terminating...{name}", fg="blue")
                            tr.terminate()
                        except OSError:
                            tr.wait()
                    # pth = Path(fp.name)
                    # if pth.exists():
                    #     pth.unlink(missing_ok=True)
                    sys.exit(os.EX_OK)

                prev = now

                if not view_only and worker.is_processing():
                    click.secho(
                        "Warning! The background process is running a job!",
                        fg="yellow",
                        bold=True,
                    )
                click.secho("interrupt... ^C again to terminate")

        # os.system("stty sane")
