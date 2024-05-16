from __future__ import annotations

from dataclasses import dataclass

import click

# from click_didyoumean import DYMGroup


IsFile = click.Path(dir_okay=False, file_okay=True)


@dataclass
class Config:
    logfile: str | None = None
    loglevel: str | None = None
    user_config: str | None = None


pass_config = click.make_pass_decorator(Config, ensure=True)


def update_mailhost(mailhost: str) -> None:
    from . import config

    config.MAIL_SERVER = mailhost


def update_config(filename: str) -> None:
    from . import config
    import tomli as tomllib

    try:
        with open(filename, "rb") as fp:
            d = tomllib.load(fp)
    except Exception as e:
        raise click.BadParameter(
            f"can't read configuration file: {e}",
            param_hint="config",
        )

    for k, v in d.items():
        k = k.upper()
        # don't changes these!
        if k in {
            "PEPXML",
            "PROTXML",
            "MZML",
            "MZMAP",
            "EICS",
            "EXT",
            "RESULT_EXT",
            "VERSION",
            "DINOSAUR",
        }:
            continue
        if hasattr(config, k):
            setattr(config, k, v)
        else:
            click.secho(f"unknown configuration attribute {k}", fg="red")


@click.group(epilog=click.style("turnover commands\n", fg="magenta"))
@click.option(
    "-l",
    "--level",
    type=click.Choice(
        ["info", "debug", "warning", "error", "critical"],
        case_sensitive=False,
    ),
    help="log level",
)
@click.option(
    "--logfile",
    type=click.Path(file_okay=True, dir_okay=False),
    help="log file to write to (use '-' to log to stderr)",
)
@click.option(
    "-m",
    "--mailhost",
    help="where to send emails to",
    metavar="HOST",
)
@click.option(
    "-c",
    "--config",
    type=click.Path(file_okay=True, dir_okay=False, exists=True),
    help="configuration file for turnover",
)
@click.version_option()
@click.pass_context
def cli(
    ctx: click.Context,
    level: str | None,
    logfile: str | None = None,
    config: str | None = None,
    mailhost: str | None = None,
) -> None:
    from .logger import init_logger

    # from .utils import df_can_write_parquet

    # if not df_can_write_parquet():
    #     click.secho(
    #         "Please install pyarrow or fastparquet", fg="red", bold=True, err=True
    #     )
    #     raise click.Abort()

    ctx.obj = Config(
        logfile=logfile,
        loglevel=level,
        user_config=config,
    )
    if level is None:
        level = "WARNING"

    if config is not None:
        update_config(config)
    if mailhost is not None:
        update_mailhost(mailhost)

    init_logger(level=level, logfile=logfile)
