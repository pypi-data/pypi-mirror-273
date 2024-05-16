from __future__ import annotations

import click

from .cli import cli
from .cli import Config
from .cli import pass_config


@cli.command(
    epilog="""

Running a webserver + turnover backend.

If not specifed with options or in a configuration file.
job results will be stored in `./turnover_jobs` (created if not existing)
and file caches will use `./turnover_cache` (created in not existing).

\b
Configuration
=============

If a configuration file is specified then you can specifiy
JOBSDIR, CACHEDIR.

The program will look for a file `~/.turnover-web.cfg` for website
configuration if no `--web-config` is given.
""",
)
@click.option(
    "-n",
    "--no-browse",
    is_flag=True,
    help="don't open web application in browser",
)
@click.option(
    "-w",
    "--workers",
    type=int,
    help="number of background workers [default: half the number of cpus]",
)
@click.option("-g", "--gunicorn", is_flag=True, help="run webapp with gunicorn")
@click.option(
    "--web-config",
    type=click.Path(file_okay=True, dir_okay=False, exists=True),
    help="configuration file for web browser",
)
@click.option(
    "--jobs-dir",
    type=click.Path(file_okay=False),
    help="directory to run job [default: directory of jobfile]",
)
@click.option(
    "--cache-dir",
    type=click.Path(file_okay=False),
    help="directory to store file caches",
)
@click.option(
    "--view-only",
    is_flag=True,
    help="only view data",
)
@click.option(
    "--port",
    default=8000,
    help="port to run webservice on",
    show_default=True,
)
@click.argument("web_options", nargs=-1)
@pass_config
def web(
    cfg: Config,
    no_browse: bool,
    workers: int,
    web_config: str | None,
    gunicorn: bool = False,
    jobs_dir: str | None = None,
    cache_dir: str | None = None,
    port: int = 8000,
    web_options: tuple[str, ...] = (),
    view_only: bool = False,
) -> None:
    """Run full website (requires protein-turnover-website)."""
    from .web import webrunner
    from pathlib import Path
    from os import cpu_count

    if web_config is None:
        path = Path("~/.turnover-web.cfg").expanduser()
        if path.exists():
            web_config = str(path)
    if workers is None:
        workers = max((cpu_count() or 1) // 2, 1)
    defaults = {}
    if cache_dir is not None:
        defaults["CACHEDIR"] = cache_dir

    if jobs_dir is not None:
        defaults["JOBSDIR"] = jobs_dir
    webrunner(
        not no_browse,
        workers,
        web_config,
        gunicorn,
        configfile=cfg.user_config,
        defaults=defaults,
        port=port,
        extra=web_options,
        view_only=view_only,
    )


@cli.command()
@click.option(
    "-n",
    "--no-browse",
    is_flag=True,
    help="don't open web application in browser",
)
@click.option("-g", "--gunicorn", is_flag=True, help="run webapp with gunicorn")
@click.option(
    "--port",
    default=8000,
    help="port to run webservice on",
    show_default=True,
)
@click.argument("jobfile", type=click.Path(file_okay=True, exists=True, dir_okay=False))
@pass_config
def view(
    cfg: Config,
    no_browse: bool,
    jobfile: str,
    gunicorn: bool = False,
    port: int = 8000,
) -> None:
    """View a completed run in a browser"""
    from pathlib import Path
    from .web import webrunner

    jf = Path(jobfile).expanduser().resolve()
    if not jf.exists():
        click.secho(f"no such file {jobfile}", fg="red")
        raise click.Abort()

    jobsddir = jf.parent
    defaults = {"JOBSDIR": str(jobsddir), "DATAID": jf.stem}

    webrunner(
        browse=not no_browse,
        workers=1,
        web_config=None,
        gunicorn=gunicorn,
        configfile=cfg.user_config,
        defaults=defaults,
        port=port,
        # extra=web_options,
        view_only=True,
        flask_app="protein_turnover_website.wsgi_view",
    )
