from __future__ import annotations

from pathlib import Path
from typing import Callable

import click

from .cli import IsFile
from .debug_df import debug
from .logger import logger


@debug.command(name="pepxml-create")
@click.option(
    "-o",
    "--out",
    help="directory to write [default is same directory as pepxml file]",
    type=click.Path(dir_okay=True, file_okay=False),
)
@click.option(
    "-w",
    "--workers",
    type=int,
    help="number of background workers [default: half the number of cpus]",
)
@click.option("--force", is_flag=True, help="force creation")
@click.argument("pepxmlfiles", nargs=-1, type=IsFile)
def pepxml_create_cmd(
    pepxmlfiles: list[str],
    out: str | None,
    workers: int | None,
    force: bool = False,
) -> None:
    """read and save pepXML file"""

    from functools import partial
    from os import cpu_count
    from .utils import PepXMLResourceFile
    from .parallel_utils import parallel_result
    from .pepxml import pepxml_create, pepok

    pout = Path(out) if out else None

    if pout is not None and not pout.is_dir():
        pout.mkdir(exist_ok=True, parents=True)

    if workers is None:
        workers = max((cpu_count() or 1) // 2, 1)

    targets = [PepXMLResourceFile(f, pout) for f in set(pepxmlfiles)]

    todo = [t for t in targets if not pepok(t, force)]

    skipped = set(targets) - set(todo)

    if skipped:
        for t in skipped:
            logger.info("skipping creation of %s cache", t.original.name)
    if not todo:
        return
    exe: list[Callable[[], None]] = []

    for idx, target in enumerate(todo):
        exe.append(partial(pepxml_create, target, idx, len(todo), workers=1))

    ntotal = len(exe)
    for idx, _ in enumerate(parallel_result(exe, workers=workers), start=1):
        logger.info("pepxml prepare task done: [%d/%d]", idx, ntotal)


@debug.command()
@click.option(
    "--kind",
    default="dataclass",
    type=click.Choice(["dataclass", "dict", "tuple"]),
    help="as a TypedDict",
)
@click.argument("name")
@click.argument("filename", type=IsFile)
def dataclass(name: str, filename: str, kind: str) -> None:
    """Generate a dataclass for a DataFrame (devtool)"""
    from .types.checking import dftoclass
    from .utils import IO

    df = IO(filename).read_df()
    dftoclass(name, df, kind)


@debug.command()
@click.argument("dataframe", type=IsFile)
def typecheck_pepxml(dataframe: str) -> None:
    """type check a pepxml data file"""
    from .types.checking import check_pepxml_columns
    from .utils import IO

    lines = check_pepxml_columns(IO(dataframe).read_df(), full=True)
    if lines:
        for line in lines:
            click.secho(line)
    else:
        click.secho("OK", fg="green", bold=True)


@debug.command()
@click.argument("dataframe", type=IsFile)
def typecheck_turnover(dataframe: str) -> None:
    """typecheck a turnover data file"""
    from .types.checking import check_df_columns
    from .types.turnovertype import TurnoverRow
    from .utils import IO

    lines = check_df_columns(IO(dataframe).read_df(), TurnoverRow, full=True)
    if lines:
        for line in lines:
            click.secho(line)
    else:
        click.secho("OK", fg="green", bold=True)


@debug.command()
@click.argument("pepxmlfile", type=IsFile)
def pepxml_spectra_count(pepxmlfile: str) -> None:
    """Count spectra in a pepxml file"""
    from .utils import human
    from .pepxml import count_spectra
    import pandas as pd

    pth = Path(pepxmlfile)

    print(human(pth.stat().st_size))
    s = pd.Series(count_spectra(pth))
    print(s)
    print("total:", s.sum())


@debug.command()
@click.option(
    "-o",
    "--out",
    help="directory to write [default is same directory as pepxml file]",
    type=click.Path(dir_okay=True, file_okay=False),
)
@click.argument("pepxml")
def read_pepxml(pepxml: str, out: str) -> None:
    """Test pepxml_reader"""
    from .pepxml_reader import pepxml_dataframe

    df = pepxml_dataframe(Path(pepxml))
    if out is not None:
        pepxml = str(Path(out).joinpath(Path(pepxml).name))
    pepxml += ".parquet"
    click.secho(f"writing: {pepxml}")
    df.to_parquet(pepxml)
