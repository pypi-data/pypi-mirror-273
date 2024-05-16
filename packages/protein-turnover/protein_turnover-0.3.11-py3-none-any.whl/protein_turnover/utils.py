from __future__ import annotations

import hashlib
import math
from dataclasses import asdict
from dataclasses import dataclass
from functools import reduce
from pathlib import Path
from typing import Any
from typing import Literal
from typing import TypedDict

import numpy as np
import pandas as pd
from scipy.fft import fft
from scipy.fft import ifft

from .config import DINOSAUR
from .config import EICS
from .config import MZMAP
from .config import MZML
from .config import PEPXML
from .config import PROTXML
from .config import RESULT_EXT
from .types.pepxmltypes import PepXMLRow
from .types.pepxmltypes import PepXMLRunRow


@dataclass
class PeptideSettings:
    rtTolerance: float = 15.0  # seconds
    mzTolerance: float = 1e-5  # ppm
    labelledIsotopeNumber: int = 15
    labelledElement: str = "N"
    maximumLabelEnrichment: float = 0.95
    retentionTimeCorrection: Literal["UseInSample", "SimpleMedian"] = "SimpleMedian"
    useObservedMz: bool = False
    minProbabilityCutoff: float = 0.8
    # fdrMaximum: float = 0.0
    # psmFilters: Filter | None = None

    def hash(self) -> str:
        from hashlib import md5

        m = md5()
        for k, v in asdict(self).items():
            if isinstance(v, float):
                v = round(v, 6)
            m.update(f"{k}={v}".encode())
        return m.hexdigest()

    def __hash__(self) -> int:
        return int(self.hash(), 16)


NPA = np.array


def NPI(list_of_ints: list[int]) -> np.ndarray[Any, np.dtype[np.int32]]:
    return np.array(list_of_ints, dtype=np.int32)


NAMES = np.array(["C", "H", "O", "N", "P", "S", "Se"])
# "C", "H", "O" ,"N", "P", "S" , "Se"
# minus H20
#   "U": NPI([3,5,1,1,0,0,1])
aminoAcids = {
    "A": NPI([3, 5, 1, 1, 0, 0, 0]),
    "C": NPI([3, 5, 1, 1, 0, 1, 0]),
    "D": NPI([4, 5, 3, 1, 0, 0, 0]),
    "E": NPI([5, 7, 3, 1, 0, 0, 0]),
    "F": NPI([9, 9, 1, 1, 0, 0, 0]),
    "G": NPI([2, 3, 1, 1, 0, 0, 0]),
    "H": NPI([6, 7, 1, 3, 0, 0, 0]),
    "I": NPI([6, 11, 1, 1, 0, 0, 0]),
    "K": NPI([6, 12, 1, 2, 0, 0, 0]),
    "L": NPI([6, 11, 1, 1, 0, 0, 0]),
    "M": NPI([5, 9, 1, 1, 0, 1, 0]),
    "N": NPI([4, 6, 2, 2, 0, 0, 0]),
    "P": NPI([5, 7, 1, 1, 0, 0, 0]),
    "Q": NPI([5, 8, 2, 2, 0, 0, 0]),
    "R": NPI([6, 12, 1, 4, 0, 0, 0]),
    "S": NPI([3, 5, 2, 1, 0, 0, 0]),
    "T": NPI([4, 7, 2, 1, 0, 0, 0]),
    "V": NPI([5, 9, 1, 1, 0, 0, 0]),
    "W": NPI([11, 10, 1, 2, 0, 0, 0]),
    "Y": NPI([9, 9, 2, 1, 0, 0, 0]),
    "a": NPI([2, 2, 1, 0, 0, 0, 0]),
    "c": NPI([5, 8, 2, 2, 0, 1, 0]),
    "m": NPI([5, 9, 2, 1, 0, 1, 0]),
    "U": NPI([3, 5, 1, 1, 0, 0, 1]),
}


class AtomicProperties(TypedDict):
    isotopeNr: np.ndarray[Any, np.dtype[np.int32]]
    abundance: np.ndarray[Any, np.dtype[np.float64]]
    mass: np.ndarray[Any, np.dtype[np.float64]]


atomicProperties: dict[str, AtomicProperties] = dict(
    C=dict(
        isotopeNr=NPI([12, 13]),
        mass=NPA([12.0, 13.0033548378]),
        abundance=NPA([0.9889, 0.0111]),
    ),
    H=dict(
        isotopeNr=NPI([1, 2]),
        mass=NPA([1.0078250321, 2.0141017780]),
        abundance=NPA([0.9998, 0.0001]),
    ),
    O=dict(
        isotopeNr=NPI([16, 17, 18]),
        mass=NPA([15.9949146, 16.9991312, 17.9991603]),
        abundance=NPA([0.9976, 0.0004, 0.0020]),
    ),
    N=dict(
        isotopeNr=NPI([14, 15]),
        mass=NPA([14.0030740052, 15.0001088984]),
        abundance=NPA([0.99633, 0.00367]),
    ),
    # need entry for formula...
    P=dict(isotopeNr=NPI([31]), mass=NPA([30.97376163]), abundance=NPA([1.0])),
    # out of (isotope number) order abundance...
    S=dict(
        isotopeNr=NPI([32, 34, 33, 36]),
        mass=NPA([31.97207070, 33.96786665, 32.97145843, 35.96708062]),
        abundance=NPA([0.9502, 0.0421, 0.0075, 0.0002]),
    ),
    # Se=dict(
    #     isotopeNr=NPI([74, 76, 77, 78, 80, 82]),
    #     mass=NPA(
    #         [73.9224764, 75.9192136, 76.9199140, 77.9173091, 79.9165213, 81.9166994],
    #     ),
    #     abundance=NPA([0.0089, 0.0937, 0.0763, 0.2377, 0.4961, 0.0873]),
    # ),
    Se=dict(
        isotopeNr=NPI([80, 78, 76, 82, 77, 74]),
        mass=NPA(
            [79.9165213, 77.9173091, 75.9192136, 81.9166994, 76.919914, 73.9224764],
        ),
        abundance=NPA([0.4961, 0.2377, 0.0937, 0.0873, 0.0763, 0.0089]),
    ),
)


def getNr(element: str) -> int:
    """get isotope number for most abundant element"""
    if element not in atomicProperties:
        raise ValueError(f'unknown element: "{element}"')
    at = atomicProperties[element]
    a = at["abundance"]
    return int(at["isotopeNr"][a.argmax()])


def okNr(element: str) -> set[int]:
    at = atomicProperties[element]
    a = at["isotopeNr"]
    return {int(i) for i in a}


def roundit(n: float, nsig: int = 3) -> int:
    from math import log10

    assert n > 0, str(n)
    pwr = round(log10(n))
    pwr = max(0, pwr - nsig)
    num = 10**pwr
    return round(n / num) * num


# return C H O N P S Se count list
def peptideFormula(peptideSequence: str) -> np.ndarray[Any, np.dtype[np.int32]]:
    startComp = NPI([0, 2, 1, 0, 0, 0, 0])
    return reduce(
        lambda total, aa: total + aminoAcids[aa],
        list(peptideSequence),
        startComp,
    )


def get_abundance(setting: PeptideSettings) -> float:
    a = atomicProperties[setting.labelledElement]
    b = a["isotopeNr"] == setting.labelledIsotopeNumber
    return a["abundance"][b][0]


def isotopicDistribution(
    peptideSequence: str,
    abundances: dict[str, np.ndarray] | None = None,
    abundanceCutoff: float = 1e-10,
    maxMass: int = 100,
) -> np.ndarray[Any, np.dtype[np.float64]]:
    """return abundance of "heavy" peptides"""
    if abundances is None:
        abundances = {}

    formula = peptideFormula(peptideSequence)

    maxElements = np.sum(formula > 0, dtype=int)

    A = np.zeros((maxElements, maxMass))

    elements = []
    for i, e in enumerate(NAMES):
        n = formula[i]
        if n > 0:
            elements.append(n)
            if e in abundances:
                a = abundances[e]
            else:
                # use natural abundance
                a = atomicProperties[e]["abundance"]
            A[len(elements) - 1, 0 : len(a)] = a

    tA = fft(A)
    ptA = np.ones((maxMass,), dtype=np.complex128)

    for i in range(maxElements):
        ptA *= tA[i] ** elements[i]

    riptA = np.real(ifft(ptA))
    mx = np.max(np.where(riptA > abundanceCutoff))
    riptA = riptA[0 : int(mx) + 1]
    return np.fmax(riptA, 0.0)
    # return np.where(riptA > 0.0, riptA, 0.0)


def labelledAtomicAbundances(
    labelledIsotopeNumber: int,
    element: str,
    abundance: float,
) -> dict[str, np.ndarray]:
    if element in atomicProperties:
        ap = atomicProperties[element]
        if labelledIsotopeNumber in ap["isotopeNr"]:
            a = ap["abundance"]
            label = ap["isotopeNr"] == labelledIsotopeNumber
            adjustedAbundance: np.ndarray = (1 - abundance) * a / np.sum(a[~label])

            adjustedAbundance[label] = abundance
            return {element: adjustedAbundance}
    raise ValueError(f"unknown element {element}[{labelledIsotopeNumber}]")


def labelledAtomicAbundances2(settings: PeptideSettings) -> dict[str, np.ndarray]:
    return labelledAtomicAbundances(
        settings.labelledIsotopeNumber,
        settings.labelledElement,
        settings.maximumLabelEnrichment,
    )


def theoretical_dist(
    peptide: str,
    labelEnrichment: float,
    settings: PeptideSettings,
) -> np.ndarray:
    from .config import ABUNDANCE_CUTOFF  # pylint: disable=import-outside-toplevel

    abundances = labelledAtomicAbundances(
        settings.labelledIsotopeNumber,
        settings.labelledElement,
        labelEnrichment,
    )
    theoreticalDist = isotopicDistribution(
        peptide,
        abundances,
        abundanceCutoff=ABUNDANCE_CUTOFF,
    )
    return theoreticalDist


def okiso(settings: PeptideSettings) -> bool:
    props = atomicProperties[settings.labelledElement]
    isotopeNr, abundance = props["isotopeNr"], props["abundance"]
    idx = (isotopeNr == settings.labelledIsotopeNumber)[0]
    ab = (abundance == np.max(abundance))[0]
    return idx != ab


def isoMzDiff(pep: PepXMLRow, settings: PeptideSettings) -> float:
    props = atomicProperties[settings.labelledElement]
    mass, abundance = props["mass"], props["abundance"]
    isoDiff = (
        mass[props["isotopeNr"] == settings.labelledIsotopeNumber]
        - mass[abundance == np.max(abundance)]
    )
    isoMzDiff = isoDiff[0] / pep.assumed_charge
    return isoMzDiff


def eic_mzranges(pep: PepXMLRunRow, settings: PeptideSettings) -> np.ndarray:
    # requires
    # maxIso, mz, assumed_charge and
    # (settings.{labelledElement,labelledIsotopeNumber}, mzTolerance)
    isoDiff = isoMzDiff(pep, settings)
    mz = pep.observed_mz if settings.useObservedMz else pep.mz
    tol = mz * settings.mzTolerance
    isoRange = range(-1, round(pep.maxIso) + 1)

    # NOTE: pep.maxIso might be a floating point number if
    # pep is actually a pd.Series
    mzranges = [
        [
            mz + iso * isoDiff - tol,
            mz + iso * isoDiff + tol,
        ]
        for iso in isoRange
    ]
    return np.array(mzranges, dtype=np.float32)


def resize(a: np.ndarray, width: int) -> np.ndarray:
    d = width - len(a)
    if d > 0:
        return np.pad(a, (0, d), "constant", constant_values=(0, 0))
    if d < 0:
        return a[:width]
    return a


def ensure_pos(a: np.ndarray) -> np.ndarray:
    # use np.fmax if we want to set a[i] to zero if a[i] is NaN
    return np.maximum(a, 0.0)
    # return np.where(a >= 0, a, 0.0)


def human(num: int, suffix: str = "B", scale: int = 1) -> str:
    if not num:
        return f"0{suffix}"
    num *= scale
    magnitude = int(math.floor(math.log(abs(num), 1000)))
    val = num / math.pow(1000, magnitude)
    if magnitude > 7:
        return "{:.1f}{}{}".format(val, "Y", suffix)
    return "{:3.1f}{}{}".format(
        val,
        ["", "k", "M", "G", "T", "P", "E", "Z"][magnitude],
        suffix,
    )


def hash256(filename: Path, bufsize: int = 4096 * 5) -> str:
    sha256_hash = hashlib.sha256()
    with filename.open("rb") as f:
        # Read and update hash string value in blocks of 4K
        for byte_block in iter(lambda: f.read(bufsize), b""):
            sha256_hash.update(byte_block)
    return sha256_hash.hexdigest()


def fileok(cached: list[Path], original: Path) -> bool:
    if not cached:
        return False
    if not original.is_file():
        return False
    omtime = original.stat().st_mtime
    for cache in cached:
        if not cache.is_file() or omtime > cache.stat().st_mtime:
            return False
    return True


class BaseResourceFile:
    def __init__(
        self,
        original: Path | str,
        cache_dir: Path | str | None = None,
    ):
        self.original = Path(original).expanduser().resolve()
        if cache_dir is None:
            self.cache_dir = self.original.parent
        else:
            self.cache_dir = Path(cache_dir).expanduser().resolve()
        self._hash: str | None = None

    @property
    def name(self) -> str:
        return self.original.name

    @property
    def exists(self) -> bool:
        return self.original.exists()

    def extok(self, *ext: str) -> bool:
        targets = [self.cache_file(e) for e in ext]
        return fileok(targets, self.original)

    def cache_file(self, ext: str) -> Path:
        # return self.cache_dir.joinpath(self.name + ext)
        return self.cache_dir.joinpath(self.hash + ext)

    def touch(self) -> bool:
        return False

    def cache_ok(self) -> bool:
        return False

    @property
    def hash(self) -> str:
        if self._hash is not None:
            return self._hash

        self._hash = self.get_hash()
        return self._hash

    def get_hash(self) -> str:
        return hash256(self.original)


class MzMLResourceFile(BaseResourceFile):
    @property
    def runName(self) -> str:
        """Name possibly in pep.xml file as <spectrum_query spectrum="{runName}.{start_scan}.{end_scan}.0 ...>"""
        return self.original.stem

    def cache_mzml(self) -> Path:
        return self.cache_file(MZML)

    def cache_memmap(self) -> Path:
        return self.cache_file(MZMAP)

    def cache_dinosaur(self) -> Path:
        return self.cache_file(DINOSAUR)

    def cache_mzml_ok(self) -> bool:
        from .dinosaur.dinosaur import DinoRunner

        ok = self.extok(MZMAP, MZML)
        if not ok:
            return False
        ok = self.extok(DINOSAUR)
        if ok:
            return True

        dino = DinoRunner.from_config()
        # no dino file check if we can generate it...
        if dino is not None and dino.can_run():
            return False
        # ok we can't generate it so cache is "fine..."
        return True

    def cache_ok(self) -> bool:
        return self.cache_mzml_ok()

    def touch(self) -> bool:
        if self.cache_ok():
            self.cache_memmap().touch()
            self.cache_mzml().touch()
            return True
        return False


class MzMLResourceFileLocal(MzMLResourceFile):
    def __init__(
        self,
        original: Path | str,
        directory: Path | str | None = None,
        name: str | None = None,
    ):
        super().__init__(original, directory)
        if name is None:
            name = self.runName
        self.outname = name

    def cache_file(self, ext: str) -> Path:
        # return self.cache_dir.joinpath(self.name + ext)
        return self.cache_dir.joinpath(self.outname + ext)

    def cache_mzml(self) -> Path:
        from .config import EXT

        return self.cache_file("." + EXT)

    def cache_memmap(self) -> Path:
        return self.cache_file(".mzi")

    def cache_mzml_ok(self) -> bool:
        from .config import EXT

        return self.extok("." + EXT, ".mzi")


class PepXMLResourceFile(BaseResourceFile):
    def cache_pepxml(self) -> Path:
        return self.cache_file(PEPXML)

    def cache_pepxml_ok(self) -> bool:
        return self.extok(PEPXML)

    def cache_ok(self) -> bool:
        return self.cache_pepxml_ok()

    def touch(self) -> bool:
        if self.cache_ok():
            self.cache_pepxml().touch()
            return True
        return False


class ProtXMLResourceFile(BaseResourceFile):
    def cache_protxml(self) -> Path:
        return self.cache_file(PROTXML)

    def cache_protxml_ok(self) -> bool:
        return self.extok(PROTXML)

    def cache_ok(self) -> bool:
        return self.cache_protxml_ok()

    def touch(self) -> bool:
        if self.cache_ok():
            self.cache_protxml().touch()
            return True
        return False


class ResultsResourceFile(BaseResourceFile):
    def cache_result(self) -> Path:
        return self.cache_file(RESULT_EXT)

    def cache_pepxml(self) -> Path:
        return self.cache_file(PEPXML)

    def cache_envelope(self) -> Path:
        return self.cache_file(EICS)

    def cache_file(self, ext: str) -> Path:
        return self.cache_dir.joinpath(self.original.name + ext)


class ResourceFiles:
    def __init__(
        self,
        pepxmls: list[PepXMLResourceFile],
        protxml: ProtXMLResourceFile,
        mzmlfiles: list[MzMLResourceFile],
    ):
        self.pepxmls = pepxmls
        self.protxml = protxml
        self.mzmlfiles = mzmlfiles
        self.cache_dirs = {
            *[s.cache_dir for s in pepxmls],
            *[s.cache_dir for s in mzmlfiles],
        }

    def lock(self, job_id: str) -> None:
        for c in self.cache_dirs:
            c.joinpath(job_id + ".lock").touch()

    def unlock(self, job_id: str) -> None:
        for c in self.cache_dirs:
            c.joinpath(job_id + ".lock").unlink(missing_ok=True)  # type: ignore

    def is_locked(self) -> bool:
        return len([f for c in self.cache_dirs for f in c.glob("*.lock")]) > 0

    def todo(self) -> list[BaseResourceFile]:
        ret: list[BaseResourceFile] = []
        for pepxml in self.pepxmls:
            if not pepxml.cache_pepxml_ok():
                ret.append(pepxml)
        for mzml in self.mzmlfiles:
            if not mzml.cache_mzml_ok():
                ret.append(mzml)
        return ret

    def ensure_directories(self) -> None:
        for cd in self.cache_dirs:
            if not cd.is_dir():
                cd.mkdir(parents=True, exist_ok=True)


def rmfiles(files: list[Path]) -> None:
    from contextlib import suppress

    for f in files:
        with suppress(OSError):
            Path(f).unlink()


def rehydrate_turnover(turn: pd.DataFrame) -> pd.DataFrame:
    if "modifications" in turn.columns and "modcol" not in turn.columns:
        turn["modcol"] = turn["modifications"].apply(Apply.modcol)
    if "eics" in turn.columns and "eics_shape" in turn.columns:
        turn["eics"] = turn[["eics", "eics_shape"]].apply(
            Apply.eics_reshape,
            axis=1,
        )
        turn.drop(columns=["eics_shape"], inplace=True)
    if "mzranges" in turn.columns:
        turn["mzranges"] = turn["mzranges"].apply(lambda mz: mz.reshape((-1, 2)))
    if "isotopeRegressions" in turn.columns:
        turn["isotopeRegressions"] = turn["isotopeRegressions"].apply(
            lambda mz: mz.reshape((-1, 2)),
        )
    return turn


# def read_rds(filename: str) -> pd.DataFrame:
#     df = IO(filename).read_df()
#     df = rehydrate_turnover(df)
#     return df


def duplicate_rows(df: pd.DataFrame, on: list[str]) -> pd.DataFrame:
    return df[df.duplicated(on, keep=False)]


def fdr(df: pd.DataFrame) -> float:
    decoy = df["is_decoy"].sum()
    denom = len(df) - decoy
    return float(decoy) / denom if denom > 0 else np.inf


def calculate_fdrs(
    df: pd.DataFrame,
    nbins: int = 50,
    score: str = "peptideprophet_probability",
) -> pd.Series:
    """Requires peptideprophet_probability, is_decoy"""
    # df['fdr'] = calculate_fdrs(df)
    from math import ceil

    decoys = df["is_decoy"]
    pbins = df[score].apply(lambda p: ceil(p * nbins))

    mx = int(pbins.max())

    fdrs: dict[int, float] = {}
    for binno in range(mx + 1):
        target = pbins >= binno
        n = target.sum()
        if n == 0:
            fdrs[binno] = fdrs.get(binno - 1, 0.0)
            continue
        ndecoys = decoys[target].sum()
        denom = n - ndecoys
        fdrs[binno] = ndecoys / denom if denom > 0 else np.inf
    return pbins.apply(lambda binno: fdrs[binno]).astype(np.float32)


class Apply:
    @staticmethod
    def eics_reshape(s: pd.Series) -> np.ndarray:
        return s["eics"].reshape(s["eics_shape"])

    @staticmethod
    def eics_reshape_np(s: pd.Series) -> np.ndarray:
        return np.array(s["eics"]).reshape(s["eics_shape"])

    @staticmethod
    def modcol(mods: list[dict], n: int = 3) -> str:
        mods = sorted(mods, key=lambda d: d["position"])
        return ":".join([f"{d['mass']:.{n}f}@{d['position']}" for d in mods])

    @staticmethod
    def binrt(rt: float, rttol: float = 15.0) -> int:
        return round(rt / rttol)

    @staticmethod
    def binmz(mz: float, mztol: float = 10e-6) -> int:
        return round(mz / mztol)


class IO:
    def __init__(self, filename: Path | str, df: pd.DataFrame | None = None):
        self.df = df
        self.filename = Path(filename)

    def save_df(self, index: bool = False) -> None:
        assert self.df is not None
        try:
            self.df.to_parquet(self.filename, index=index)

        except (Exception, KeyboardInterrupt):
            rmfiles([self.filename])  # cleanup
            raise

    def read_df(self, columns: list[str] | None = None) -> pd.DataFrame:
        if self.filename.name.endswith(".feather"):
            return pd.read_feather(self.filename, columns=columns, use_threads=True)
        return pd.read_parquet(self.filename, columns=columns, use_threads=True)


def df_can_write(fmt: str) -> bool:
    from io import BytesIO

    df = pd.DataFrame({"x", [0]})  # pylint: disable=unhashable-member
    func = getattr(df, f"to_{fmt}", None)
    if func is None:
        return False
    try:
        func(BytesIO())
        return True
    except ModuleNotFoundError:
        return False


def df_can_write_parquet() -> bool:
    return df_can_write("parquet")


def df_can_write_excel() -> bool:
    return df_can_write("excel")


def getsize(fname: Path) -> int:
    return fname.stat().st_size
