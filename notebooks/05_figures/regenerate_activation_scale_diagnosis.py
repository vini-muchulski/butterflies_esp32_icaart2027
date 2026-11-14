from pathlib import Path

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.patches import Patch
from matplotlib.ticker import LogFormatterSciNotation


plt.style.use("seaborn-v0_8-whitegrid")
mpl.rcParams.update({
    "figure.dpi": 120,
    "savefig.dpi": 300,
    "font.size": 10,
    "axes.titlesize": 11,
    "axes.labelsize": 10,
    "legend.fontsize": 9,
})


ROOT = Path(__file__).resolve().parent
TABLES = ROOT / "tables"
FIGURES = ROOT / "figures"


def save(figure, stem):
    FIGURES.mkdir(exist_ok=True)
    for extension in ("png", "pdf"):
        path = FIGURES / f"{stem}.{extension}"
        figure.savefig(path, dpi=300, bbox_inches="tight")
        print(path)
    plt.close(figure)


def plot_scale_ratios(summary):
    blocks = summary["block"].astype(int).to_numpy()
    ratios = summary["scale_ratio"].to_numpy()
    colors = [
        "#4C72B0" if block in (1, 2, 5) else "#DD8452" if block == 3 else "#B7B7B7"
        for block in blocks
    ]

    figure, axis = plt.subplots(figsize=(7.4, 4.4))
    bars = axis.bar(blocks, ratios, color=colors, width=0.7)
    axis.set_yscale("log")
    axis.set_yticks([100, 200, 300, 400, 600])
    axis.yaxis.set_major_formatter(
        LogFormatterSciNotation(
            base=10,
            labelOnlyBase=False,
            minor_thresholds=(np.inf, np.inf),
        )
    )
    axis.set_xticks(blocks)
    axis.set_xlabel("MobileViT inverted residual block")
    axis.set_ylabel("Max/min estimated channel-scale ratio")
    axis.set_title("Activation-scale heterogeneity before grouping")
    axis.legend(
        handles=[
            Patch(color="#4C72B0", label="Grouped in both variants (1, 2, 5)"),
            Patch(color="#DD8452", label="Added in extended variant (3)"),
            Patch(color="#B7B7B7", label="Ungrouped in both variants (4, 6, 7)"),
        ],
        frameon=False,
        fontsize=8,
        loc="upper right",
    )
    for bar, ratio in zip(bars, ratios):
        axis.annotate(
            f"{ratio:.0f}×",
            (bar.get_x() + bar.get_width() / 2, ratio),
            xytext=(0, 3),
            textcoords="offset points",
            ha="center",
            va="bottom",
            fontsize=8,
        )
    save(figure, "figure_1a_activation_scale_heterogeneity")


def plot_effective_levels(summary, blocks):
    medians = summary.pivot(
        index="block", columns="configuration", values="median_effective_levels"
    ).loc[blocks]
    configurations = (
        ("Original", "Ungrouped", "#C44E52"),
        ("g8_4_4", "g8_4_4", "#8172B2"),
        ("g8_4_4 + b3_g4", "g8_4_4 + b3_g4", "#55A868"),
    )
    positions = np.arange(len(blocks))
    width = 0.24

    figure, axis = plt.subplots(figsize=(7.6, 4.6))
    for offset, (key, label, color) in zip((-width, 0, width), configurations):
        axis.bar(positions + offset, medians[key], width=width, color=color, label=label)
    axis.axhline(16, color="#C44E52", linestyle="--", linewidth=0.9)
    axis.axhline(32, color="#DD8452", linestyle=":", linewidth=1.1)
    axis.set_yscale("log", base=2)
    axis.set_ylim(0.8, 320)
    axis.set_xticks(positions, blocks)
    axis.set_xlabel("MobileViT inverted residual block")
    axis.set_ylabel("Median estimated effective INT8 levels")
    axis.set_title("Estimated numerical resolution by configuration")
    axis.legend(title="Channel grouping", frameon=False, ncol=3, fontsize=8)
    axis.text(
        0.98, 0.05, "Dashed: 16 levels\nDotted: 32 levels",
        transform=axis.transAxes, ha="right", va="bottom", fontsize=8,
        bbox={"facecolor": "white", "edgecolor": "#BBBBBB"},
    )
    save(figure, "figure_1b_estimated_effective_int8_levels")


def main():
    activation = pd.read_csv(TABLES / "block_activation_summary.csv").sort_values("block")
    effective = pd.read_csv(TABLES / "estimated_effective_levels_summary.csv")
    plot_scale_ratios(activation)
    plot_effective_levels(effective, activation["block"].astype(int).to_numpy())


if __name__ == "__main__":
    main()
