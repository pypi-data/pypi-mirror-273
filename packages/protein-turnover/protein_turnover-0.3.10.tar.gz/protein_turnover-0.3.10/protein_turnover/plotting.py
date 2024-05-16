from __future__ import annotations

from base64 import b64encode
from io import BytesIO

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.axes import Axes
from matplotlib.figure import Figure
from scipy import stats

from .logger import logger
from .sns import despine
from .types.turnovertype import TurnoverDict
from .types.turnovertype import TurnoverRow
from .utils import ensure_pos
from .utils import isotopicDistribution
from .utils import PeptideSettings
from .utils import resize


EICS_CMAP = plt.get_cmap("viridis")

NEICS_CMAP = len(EICS_CMAP.colors)

EIC_COLUMNS = ["peptide", "modcol", "eics", "eics_shape", "monoFitParams"]


def peptide_legend(peptide: TurnoverRow, enrichment: float | None = None) -> str:
    if enrichment is None:
        enrichment = peptide.enrichment
    if enrichment is not None:
        ie = round(peptide.enrichment * 100, 1)
        ia = round(peptide.relativeIsotopeAbundance * 100, 1)
        return f"{peptide.peptide}\nLPF: {ia}%\nEnrichment: {ie}%"
    else:
        return f"{peptide.peptide},\nunable to estimate enrichment / LPF"


def despine_bottom(ax: Axes) -> None:
    despine(ax=ax, bottom=True, trim=True)


def despine_top(ax: Axes, offset: int = 5) -> None:
    despine(ax=ax, top=True, trim=True, offset=offset)


def plotEICS(peptide: TurnoverRow, ax: Axes | None = None) -> Axes:
    from .config import FIGSIZE
    from .fitenvelopes import normalIntensityFunction, FAIL_W_CURVE

    pep = peptide.peptide
    mod = peptide.modcol
    eics = peptide.eics
    monoFitParams = peptide.monoFitParams
    fail = len(monoFitParams) == 0  # old way
    if hasattr(peptide, "fail"):  # my way
        fail = fail | (getattr(peptide, "fail") & (1 << FAIL_W_CURVE))

    # maxInt = eics[0,:, 1].max()
    # ylim = (0, maxInt)
    if ax is None:
        fig = Figure(figsize=FIGSIZE)
        ax = fig.subplots()
    ax.set(xlabel="retention time", ylabel="Intensity", title=f"{pep} {mod}")

    m = eics[0]
    rt, im = m[:, 0], m[:, 1]
    ax.plot(rt, im, color="dodgerblue", lw=2)
    oeics = eics[2:]
    step = max(NEICS_CMAP // len(oeics), 1) if len(oeics) else 1

    for idx, e in enumerate(oeics):
        rt, i = e[:, 0], e[:, 1]
        icolor = min(idx * step, NEICS_CMAP - 1)
        ax.plot(
            rt,
            i,
            color=EICS_CMAP.colors[icolor],
            alpha=0.2,
            linestyle="dashed",
        )

    mono = eics[1]
    rt, im = mono[:, 0], mono[:, 1]
    ax.plot(rt, im, color="red", lw=2)
    d = dict(handlelength=0)
    if not fail:
        i = normalIntensityFunction(rt, *monoFitParams)
        ax.plot(rt, i, color="#8b2252", lw=2)  # violetred4
        ax.legend(labels=["Good"], labelcolor="darkgreen", **d)
    else:
        ax.legend(labels=["Bad"], labelcolor="salmon", **d)

    return ax


def intrange(n: int) -> np.ndarray:
    return np.arange(0, n, 1, dtype=np.int32)


LABELLED_COLUMNS = [
    "labelledEnvelopes",
    "labelledElementCount",
    "peptide",
    "enrichment",
    "relativeIsotopeAbundance",
    "theoreticalDist",
]


def plotLabelledEnvelope(
    peptide: TurnoverRow,
    settings: PeptideSettings,
    ax: Axes | None = None,
    scaled: bool = True,
) -> Axes:
    from .config import FIGSIZE
    from .fitenvelopes import get_enrichments

    if ax is None:
        fig = Figure(figsize=FIGSIZE)
        ax = fig.subplots()
    if len(peptide.labelledEnvelopes) > 0:
        e = peptide.labelledEnvelopes
        e = e if isinstance(e, np.ndarray) else np.array(e)
        x = intrange(len(e))
        enrichments = get_enrichments(peptide.peptide, settings)
        enrichments = resize(enrichments, len(e))
        if scaled:
            total = e.sum()
            e = e / total
        ax.bar(x, e, color="turquoise", edgecolor="black")
        ax.set_xticks(x)
        ax.set_xticklabels(
            [f"[{i}]{v:.2f}" for i, v in enumerate(enrichments)],
            rotation=-90,
        )
        ax.set(xlabel="enrichment")
        if scaled:
            ax.set(ylim=(0.0, 1.0), ylabel="fraction")

    else:
        ie = peptide.labelledElementCount
        x = intrange(ie + 1)
        ax.bar(x, np.repeat(0, ie + 1), color="turquoise")
        ax.set_xticks(x)
    ax.legend(labels=[peptide_legend(peptide)], handlelength=0)
    despine_bottom(ax)
    ax.xaxis.set_ticks_position("none")
    ax.set(title="labelledEnvelopes")
    return ax


# def norm(peptide: TurnoverRow, settings: PeptideSettings):

#     theoreticalDist = theoretical_dist(peptide.peptide, peptide.enrichment, settings)

#     LPF = peptide.relativeIsotopeAbundance
#     ndist = isotopicDistribution(peptide.peptide)
#     naturalDist = ndist * (1 - LPF)
#     labelledDist = theoreticalDist * LPF

#     monoPeak = peptide.isotopeEnvelopes[1]
#     denom = naturalDist[0] + labelledDist[0]
#     fraction = 1.0 / denom if denom != 0 else np.inf
#     scalingFactor = monoPeak * fraction

#     naturalDist = resize(naturalDist, peptide.maxIso + 1)
#     theoreticalDist = resize(labelledDist, peptide.maxIso + 1)
#     # LPF == 0 => monoPeak * ndist/ndist[0]
#     # LPF == 1 => monoPeak * ndist^A/ndist^A[0]
#     # (theoreticalDist * scalingFactor)[0]  + (naturalDist * scalingFactor)[0] = monoPeak
#     return theoreticalDist * scalingFactor, naturalDist * scalingFactor


FITTED_COLUMNS = [
    "peptide",
    "modcol",
    "isotopeEnvelopes",
    "maxIso",
    "relativeIsotopeAbundance",
    "enrichment",
    # "adjustedRsq",
]


def plotFittedEnvelopes(
    peptide: TurnoverRow,
    settings: PeptideSettings,
    ax: Axes | None = None,
) -> Axes:
    from .config import FIGSIZE

    pep = peptide.peptide
    mod = peptide.modcol
    isotopeEnvelopes = peptide.isotopeEnvelopes
    if len(isotopeEnvelopes) == 0:
        logger.warning("plotFittedEnvelopes[%s]: no envelope!", pep)
        return ax
    has_adj = hasattr(peptide, "adjustedRsq")
    if has_adj:
        adjustedRsq = resize(np.array(peptide.adjustedRsq), peptide.maxIso + 2)
    # theoreticalDist, naturalDist = norm(peptide, settings)

    isotopeEnvelopes = resize(isotopeEnvelopes, peptide.maxIso + 2)

    theoreticalDist = np.array(peptide.theoreticalDist)
    naturalDist = isotopeEnvelopes[1] * isotopicDistribution(peptide.peptide)

    naturalDist = resize(naturalDist, peptide.maxIso + 1)
    theoreticalDist = resize(theoreticalDist, peptide.maxIso + 1)

    x = intrange(len(isotopeEnvelopes)) - 1

    heavyDistribution = ensure_pos(isotopeEnvelopes[1:] - naturalDist)
    if ax is None:
        fig = Figure(figsize=FIGSIZE)
        ax = fig.subplots()
    xm1, x1 = x[:1], x[1:]  # skip negative heavy atom
    ax.set(title=f"{pep} {mod}")
    ax.bar(
        x1,
        isotopeEnvelopes[1:],
        color="turquoise",
        alpha=1.0,
    )
    ax.bar(x1, heavyDistribution, color="blue", width=0.5, alpha=0.3)
    if has_adj:
        ax.bar(x1, adjustedRsq[1:] * isotopeEnvelopes[1], color="tomato")

    ax.legend(labels=[peptide_legend(peptide)], handlelength=0, facecolor="none")
    ax.bar(xm1, isotopeEnvelopes[:1], color="red", alpha=0.3)
    ax.bar(x1, -theoreticalDist, color="#98F5FF", alpha=0.3)  # cadetblue1
    nd = resize(naturalDist, len(x) - 1)
    ax.vlines(x1, 0, nd, color="orange", linestyle="dashed")
    ax.scatter(x1, nd, color="orange", marker="o", s=20)

    xlabel = f"number of ${{}}^{{{settings.labelledIsotopeNumber}}}{settings.labelledElement}$ atoms"
    nfailed = np.isnan(isotopeEnvelopes[1:]).sum()
    if nfailed > 0:
        xlabel += f" [{nfailed} failed fits]"
    ax.set(xlabel=xlabel)

    ax.set_xticks(x)

    despine_bottom(ax)
    ax.xaxis.set_ticks_position("none")

    return ax


def plotIntensities(
    peptide: TurnoverRow,  # eics
    eici: list[int] | None = None,
    ax: Axes | None = None,
    figsize: tuple[float, float] | None = None,
) -> Axes:
    from scipy.linalg import lstsq
    from .config import FIGSIZE

    intensity = peptide.eics[1, :, 1]
    im = np.c_[np.ones(len(intensity)), intensity]
    x = np.linspace(np.min(intensity), np.max(intensity), num=30)
    idx = set(range(peptide.eics.shape[0]))
    if eici is None:
        eici = list(idx)
    else:
        eici = list(sorted(set(eici) & idx))
    if ax is None:
        fig = Figure(figsize=figsize if figsize else FIGSIZE)
        ax = fig.subplots(1, 1)
    for i in eici:
        ints = peptide.eics[i, :, 1]
        fit, _residues, _rank, _s = lstsq(im, ints)

        y = fit[0] + fit[1] * x
        ax.scatter(intensity, ints, s=10)
        ax.plot(x, y)
    ax.set(
        title=f"{peptide.peptide} {peptide.modcol}",
        xlabel="mono intensity",
        ylabel="intensity",
    )
    return ax


def enrichment_plot(
    turn: pd.DataFrame,
    factor: float = 2.0,
    ax: Axes | None = None,
    figsize: tuple[float, float] | None = None,
    column: str = "enrichment",
) -> Axes:
    from .config import FIGSIZE

    enrich = turn[column]
    enrich = enrich[enrich.notna()]
    em = enrich.mean()
    esd = enrich.std()
    if ax is None:
        fig = Figure(figsize=figsize if figsize else FIGSIZE)
        ax = fig.subplots(1, 1)

    x = np.linspace(enrich.min() - 3 * esd, enrich.max() + 3 * esd, 40)
    y = stats.norm(em, esd).pdf(x)
    ax.hist(
        enrich,
        bins=40,
        color="turquoise",
        alpha=0.4,
        density=True,
        edgecolor="#999",
    )
    ax.plot(x, y)
    ax.vlines([em - factor * esd, em + factor * esd], 0, [2.5, 2.5], color="red")
    despine_top(ax, offset=5)
    return ax


def nnls_values(
    df: pd.DataFrame,
    percent: float = 0.01,
) -> pd.Series:
    nnls_residual = df["nnls_residual"]
    if "totalNNLSWeight" in df.columns:
        nnls_residual = nnls_residual / df["totalNNLSWeight"]

    nnls_residual = nnls_residual[nnls_residual.notna()]
    if percent == 0.0:
        return nnls_residual

    bins, bounds = np.histogram(nnls_residual, bins=500)

    maxval = bins.max()
    imax: int = np.argmax(bins == maxval)  # type: ignore
    idx: int = min(len(bounds) - 1, imax + np.argmin(bins[imax:] / maxval > percent))  # type: ignore

    return nnls_residual[nnls_residual < bounds[idx]]


def nnls_plot(
    df: pd.DataFrame,
    ax: Axes | None = None,
    figsize: tuple[float, float] | None = None,
    percent: float = 0.01,
) -> Axes:
    from .config import FIGSIZE

    nnls = nnls_values(df, percent=percent)

    if ax is None:
        fig = Figure(figsize=figsize if figsize else FIGSIZE)
        ax = fig.subplots(1, 1)
    # mn,mx = nnls_residual.min(), nnls_residual.max()
    ax.hist(nnls, bins="auto", color="turquoise")
    despine(ax, trim=True, offset=5)
    ax.set(ylabel="counts", xlabel="NNLS residual")
    return ax


def correlation_plot(
    df: pd.DataFrame,
    column: str,
    xlabel: str | None = None,
    ax: Axes | None = None,
    figsize: tuple[float, float] | None = None,
) -> Axes:
    from .config import FIGSIZE

    if ax is None:
        fig = Figure(figsize=figsize if figsize else FIGSIZE)
        ax = fig.subplots(1, 1)
    # mn,mx = nnls_residual.min(), nnls_residual.max()
    col = df[column]
    ax.hist(col, bins="auto", color="turquoise")
    despine(ax, trim=True, offset=5)
    ax.set(ylabel="counts", xlabel=xlabel or column)
    return ax


ALL_COLUMNS = list(set(EIC_COLUMNS) | set(FITTED_COLUMNS) | set(LABELLED_COLUMNS))


def plot_all(
    peptide: TurnoverRow,
    settings: PeptideSettings,
    figsize: tuple[float, float] | None = None,
    hspace: float = 0.5,
    portrait: bool = True,
) -> tuple[Figure, list[Axes]]:
    from .config import FIGSIZE

    if figsize is None:
        figsize = FIGSIZE[0], 3 * FIGSIZE[1]

    if not portrait:
        r, c = 1, 3
    else:
        r, c = 3, 1
    fig = Figure(figsize=figsize)
    axes = fig.subplots(r, c, gridspec_kw=dict(hspace=hspace))

    plotEICS(peptide, ax=axes[0])
    plotFittedEnvelopes(peptide, settings, ax=axes[1])
    plotLabelledEnvelope(peptide, settings, ax=axes[2])
    # plotIntensities(peptide, [1, 2, 3, 4, 5, 6], ax=ax4)
    return fig, axes


def rename(s: pd.Series, suffix: str = "_me") -> pd.Series:
    r = pd.Series(dtype=object)
    for key in [
        "isotopeEnvelopes",
        "relativeIsotopeAbundance",
        "monoFitParams",
        "eics",
        "labelledEnvelopes",
        "labelledElementCount",
        "enrichment",
        "heavyFitParams",
        "heavyCor",
    ]:
        r[key] = s[key + suffix]

    r.peptide = s.peptide
    r.modcol = s.modcol
    r.maxIso = int(s["maxIso" + suffix])
    return r


def plot_eics_sidebyside(
    b: TurnoverRow,
    suffix: str = "_me",
    figsize: tuple[float, float] = (15.0, 5.0),
) -> tuple[Figure, Axes, Axes]:
    fig = Figure(figsize=figsize)
    [ax1, ax2] = fig.subplots(1, 2)

    plotEICS(b, ax=ax1)
    plotEICS(rename(b, suffix), ax=ax2)
    return fig, ax1, ax2


def plot_fitted_sidebyside(
    b: TurnoverRow,
    settings: PeptideSettings,
    suffix: str = "_me",
    figsize: tuple[float, float] = (15, 5),
) -> tuple[Figure, Axes, Axes]:
    fig = Figure(figsize=figsize)
    [ax1, ax2] = fig.subplots(1, 2)

    plotFittedEnvelopes(b, settings, ax=ax1)
    plotFittedEnvelopes(rename(b, suffix), settings, ax=ax2)
    return fig, ax1, ax2


def plot_labelled_sidebyside(
    b: TurnoverRow,
    settings: PeptideSettings,
    suffix: str = "_me",
    figsize: tuple[float, float] = (15, 5),
) -> tuple[Figure, Axes, Axes]:
    fig = Figure(figsize=figsize)
    [ax1, ax2] = fig.subplots(1, 2)

    plotLabelledEnvelope(b, settings, ax=ax1)
    plotLabelledEnvelope(rename(b, suffix), settings, ax=ax2)
    return fig, ax1, ax2


def plot_fit_arrays(
    row: TurnoverRow,
    suffix: str = "_me",
    figsize: tuple[float, float] = (15, 12),
) -> tuple[Figure, list[list[Axes]]]:
    b: TurnoverDict = row  # type: ignore
    fig = Figure(figsize=figsize)
    axes = fig.subplots(
        5,
        2,
        gridspec_kw=dict(hspace=0.5),
    )
    [[ax1, ax2], [ax3, ax4], [ax5, ax6], [ax7, ax8], [ax9, ax10]] = axes

    def plot_a(name: str, ax: Axes) -> None:
        x = list(range(0, len(b[name])))  # type: ignore
        v = b[name + suffix]  # type: ignore
        if len(x) != len(v):
            ax.set(title=f"bad {name}")
            return
        dodge = np.nanmax(np.abs(v)) / 50
        ax.plot(x, b[name])  # type: ignore
        ax.plot(x, v + dodge)
        ax.set(title=f"{name}")

    def plot_a_col(name: str, ax: Axes, col: int) -> None:
        x = list(range(0, len(b[name][:, col])))  # type: ignore
        v = b[name + suffix][:, col]  # type: ignore
        if len(x) != len(v):
            ax.set(title=f"bad {name}")
            return
        dodge = np.nanmax(np.abs(v)) / 50
        ax.plot(x, b[name][:, col])  # type: ignore
        ax.plot(x, v + dodge)
        ax.set(title=f"{name}")

    # def plot_heavy_fit(ax: Axes) -> None:
    #     from .fitenvelopes import normalIntensityFunction2

    #     params = b["heavyFitParams"]
    #     if params is None or len(params) == 0:
    #         return

    #     hd = b["heavyDistribution"]

    #     x = np.array(list(range(len(hd))), dtype=np.float32)
    #     mu, sigma, k, r_sq, r_adj = params
    #     y: np.ndarray = normalIntensityFunction2(x, mu, sigma, k)  # type: ignore
    #     ax.plot(x, y, color="#5555ff")
    #     ax.text(x[0], y.max(), f"r_adj={r_adj:.2f}", fontsize=10)

    def ratio(name: str) -> np.ndarray:
        a = b[name]  # type: ignore
        m = b[name + suffix]  # type: ignore
        if len(a) != len(m):
            return a * 0
        both = (a == 0) & (m == 0)
        ret = m / np.where(a != 0, a, 1e-6)
        if both.sum() > 0:  # 0/0 is 1 !
            ret = np.where(both, 1.0, ret)
        return ret

    def plot_ratio(name: str, ax: Axes) -> None:
        val = b[name]  # type: ignore
        x = list(range(0, len(val)))
        ax.plot(x, ratio(name))
        ax.set(title=f"{name} ratio")

    plot_a_col("isotopeRegressions", ax1, 1)
    ax1.set(title="regression intensity")

    plot_a_col("isotopeRegressions", ax2, 0)
    ax2.set(title="adjusted R-squared")

    plot_a("isotopeEnvelopes", ax3)
    # plot_a("heavyDistribution", ax4)
    # plot_heavy_fit(ax4)
    plot_a("labelledEnvelopes", ax5)
    plot_a("monoFitParams", ax6)
    # plot_a("heavyFitParams", ax7)

    plot_ratio("monoFitParams", ax8)
    plot_ratio("isotopeEnvelopes", ax9)
    # plot_ratio("heavyDistribution", ax10)

    return fig, axes


# for use in jupyter notebooks....
def plot_all_sidebyside(
    b: TurnoverRow,
    settings: PeptideSettings,
) -> tuple[Figure, Figure, Figure, Figure]:
    f1, *_axes = plot_eics_sidebyside(b)
    f2, *_axes = plot_fitted_sidebyside(b, settings)
    f3, *_axes = plot_labelled_sidebyside(b, settings)
    f4, _axes = plot_fit_arrays(b)
    return f1, f2, f3, f4


def to_image_url(fig: Figure, format: str = "png") -> str:
    out = BytesIO()
    fig.savefig(out, format=format)
    data = f"data:image/{format.lower()};base64,".encode("ascii") + b64encode(
        out.getbuffer(),
    )
    return data.decode("ascii")


def plotLPF(
    df: pd.DataFrame,  # ['peptide', 'relativeIsotopeAbundance']
    ax: Axes | None = None,
    figsize: tuple[float, float] = (8.0, 1.5),
    sort: bool = True,
) -> Axes:
    if ax is None:
        fig = Figure(figsize=figsize)
        ax = fig.subplots()
    d = df.set_index("peptide")
    d = d["relativeIsotopeAbundance"]
    if sort:
        d = d.sort_values()
    # d.plot(ax=ax, style=".-", color="turquoise")
    d.plot(ax=ax, kind="bar", color="turquoise", edgecolor="black")
    ax.set(ylabel="LPF", ylim=(0, 1), xticks=[])
    despine(
        ax=ax,
        top=True,
        bottom=False,
        trim=True,
        offset=0,
    )
    legend = ax.get_legend()
    if legend is not None:
        legend.remove()

    ax.get_figure().tight_layout()
    return ax


def plotLogSigmaLPF(
    df: pd.DataFrame,
    ax: Axes | None = None,
    figsize: tuple[float, float] = (8.0, 4.0),
    remove_zero_std: bool = True,
) -> Axes:
    if ax is None:
        fig = Figure(figsize=figsize)
        ax = fig.subplots()
    key = df["lpf_median"] != 0.0
    if remove_zero_std:
        key = key & (df["lpf_std"] != 0.0)
    d = df[key]
    x = np.log((d["lpf_std"] + 1e-4) / (d["lpf_median"]))

    x.plot.hist(ax=ax, bins=100, color="turquoise", grid=False)
    despine(ax, trim=True, offset=5)
    ax.set(ylabel="counts", xlabel=r"$log(\sigma/LPF)$")
    return ax
