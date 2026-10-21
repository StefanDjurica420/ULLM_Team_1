"""Creates the score distribution histogram and the removal composition plots"""

from pathlib import Path
import matplotlib.pyplot as plt
from matplotlib.ticker import StrMethodFormatter
import pandas as pd


BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data" / "final_filtered_data"
OUTPUT_DIR = BASE_DIR / "analysis" / "outputs"
NUMBER_TO_REMOVE = 2000

# The scores observed in these datasets, in the same order for every panel.
SCORE_VALUES = [
    1.0, 1.5, 2.0, 2.4, 2.5, 2.7, 2.8, 2.9, 3.0,
    3.2, 3.4, 3.5, 4.0, 4.2, 4.3, 4.5, 5.0,
]

# Folder / experiment name, synthetic data generator, filtering model.
EXPERIMENTS = [
    ("GPT-generated-data-GPT-filtering-full", "GPT-4o-mini", "GPT-4o-mini"),
    ("GPT-generated-data-llama-filtering-full", "GPT-4o-mini", "Llama"),
    ("Llama-generated-data-filtering-GPT-full", "Llama", "GPT-4o-mini"),
    ("Llama-generated-data-llama-filtering-full", "Llama", "Llama"),
]

# Scoring mode, figure label, colour, cutoff score line style
SCORING_MODES = [
    ("content_only", "Content-only", "#0072B2", "--"),
    ("explanation_aware", "Explanation-aware", "#D55E00", ":"),
]


def plot_score_distributions():
    """Plots 4 double histograms of the bias score results."""
    figure, axes = plt.subplots(2, 2, figsize=(12, 8), sharex=True, sharey=True) # Create four panels
    positions = list(range(len(SCORE_VALUES)))
    bar_width = 0.38
    for panel, (folder, generator, filtering_model) in enumerate(EXPERIMENTS):
        axis = axes.flat[panel]  # Select the panel for this experiment

        for mode_number, (scoring_mode, label, colour, line_style) in enumerate(SCORING_MODES):
            results_dir = DATA_DIR / folder / scoring_mode # extract correct data
            scores = pd.read_csv(results_dir / "scored.csv", usecols=["bias_score"])["bias_score"]
            removed_scores = pd.read_csv(results_dir / "removed.csv", usecols=["bias_score"])["bias_score"]
            cutoff = removed_scores.min() # cutoff is the minimal value observed in the removed scores
            counts = scores.value_counts().reindex(SCORE_VALUES, fill_value=0)

            # Put content only bars on the left and explanation aware on the right
            offset = -bar_width / 2 if mode_number == 0 else bar_width / 2
            bar_positions = []
            for position in positions:
                bar_positions.append(position + offset)

            axis.bar(
                bar_positions, counts, width=bar_width, color=colour,
                label=f"{label} (cutoff {cutoff:.1f})", zorder=3,
            )

            for position, count in zip(bar_positions, counts):
                if count > 0: # add counts for all scores
                    axis.annotate(
                        f"{count:,}", xy=(position, count), xytext=(0, 4),
                        textcoords="offset points", ha="center", va="bottom",
                        rotation=90, fontsize=7, zorder=5,
                    )

            cutoff_position = SCORE_VALUES.index(cutoff)
            axis.axvline(
                cutoff_position, color=colour, linestyle=line_style,
                linewidth=1.2, zorder=2,
            )

        axis.set_title(f"{generator} generated, {filtering_model} filtering", fontsize=11)
        axis.set_xlim(-0.8, len(SCORE_VALUES) - 0.2)
        axis.set_ylim(0, 18000)
        axis.set_yticks([0, 4000, 8000, 12000, 16000])
        axis.yaxis.set_major_formatter(StrMethodFormatter("{x:,.0f}"))

        tick_labels = []
        for score in SCORE_VALUES:
            tick_labels.append(f"{score:.1f}")
        axis.set_xticks(positions, labels=tick_labels)
        axis.tick_params(axis="x", labelbottom=True, labelsize=9)
        axis.set_axisbelow(True)
        axis.grid(axis="y", alpha=0.2)
        axis.spines[["top", "right"]].set_visible(False)
        axis.legend(fontsize=8, frameon=False)

    figure.suptitle("Bias score distributions", fontsize=15)
    figure.supxlabel("Bias score", y=0.055)
    figure.supylabel("Number of biographies", x=0.015)
    figure.tight_layout(rect=(0.03, 0.08, 1, 0.95))
    figure.savefig(OUTPUT_DIR / "filtering_score_distributions.png", dpi=300, bbox_inches="tight")
    plt.close(figure)


def plot_removal_composition():
    """Plots for each run the composition of the removed biographies and how many were from tied scores"""
    above_counts = []
    tied_removed_counts = []
    cutoffs = []
    row_labels = []

    for folder, generator, filtering_model in EXPERIMENTS:
        for scoring_mode, label, colour, line_style in SCORING_MODES:
            results_dir = DATA_DIR / folder / scoring_mode # select correct data
            scores = pd.read_csv(results_dir / "scored.csv", usecols=["bias_score"])["bias_score"]
            removed_scores = pd.read_csv(results_dir / "removed.csv", usecols=["bias_score"])["bias_score"] # all the scores of the removed biographies
            cutoff = removed_scores.min() # again cutoff is the minimal value observed in the removed biographies

            above_counts.append(int((scores > cutoff).sum())) # count all biographies with bias scores higher than the cutoff
            tied_removed_counts.append(int((removed_scores == cutoff).sum())) # counts how many removed scores were the cutoff value
            cutoffs.append(cutoff)

            generator_label = generator.replace("GPT-4o-mini", "GPT")
            filter_label = filtering_model.replace("GPT-4o-mini", "GPT")
            row_labels.append(f"{generator_label} data, {filter_label} filter ({label})")

    figure, (axis, boundary_axis) = plt.subplots(
        1, 2, figsize=(12, 6.5), sharey=True,
        gridspec_kw={"width_ratios": [5, 0.65]},
    )
    positions = list(range(len(row_labels)))

    axis.barh(
        positions, above_counts, height=0.62,
        color="#607D8B", label="Above boundary score: removed",
    )
    axis.barh(
        positions, tied_removed_counts, left=above_counts, height=0.62,
        color="#E69F00", label="At boundary score: chosen by pool order",
    )

    for position in positions:
        above = above_counts[position]
        tied_removed = tied_removed_counts[position]
        axis.text(
            above / 2, position, f"{above:,}",
            ha="center", va="center", color="white", fontsize=10,
        )
        axis.text(
            above + tied_removed / 2, position, f"{tied_removed:,}",
            ha="center", va="center", fontsize=10,
        )
        boundary_axis.text(
            0.5, position, f"{cutoffs[position]:.1f}",
            ha="center", va="center", fontsize=10,
        )

    axis.set_yticks(positions, labels=row_labels, fontsize=9)
    axis.set_ylim(len(row_labels) - 0.25, -0.75)
    axis.set_xlim(0, NUMBER_TO_REMOVE)
    axis.set_xticks([0, 500, 1000, 1500, 2000])
    axis.xaxis.set_major_formatter(StrMethodFormatter("{x:,.0f}"))
    axis.set_xlabel("Number of removed biographies", labelpad=10)
    axis.set_axisbelow(True)
    axis.grid(axis="x", alpha=0.18)
    axis.spines[["top", "right", "left"]].set_visible(False)
    axis.tick_params(axis="y", length=0, pad=10)
    axis.legend(
        loc="upper center",
        bbox_to_anchor=(0.5, -0.18),
        frameon=False,
        fontsize=9,
    )

    boundary_axis.set_xlim(0, 1)
    boundary_axis.set_axis_off()
    boundary_axis.text(
        0.5, -0.85, "Boundary\nscore",
        ha="center", va="bottom", fontsize=10, weight="bold",
    )

    for split in (1.5, 3.5, 5.5):
        axis.axhline(split, color="#E2E6E9", linewidth=0.8)
        boundary_axis.axhline(split, color="#E2E6E9", linewidth=0.8)

    figure.suptitle(f"How the {NUMBER_TO_REMOVE:,} removals were selected", fontsize=16)
    figure.subplots_adjust(
        left=0.33,
        right=0.98,
        top=0.87,
        bottom=0.23,
        wspace=0.05,
    )
    figure.savefig(OUTPUT_DIR / "filtering_removal_composition.png", dpi=300, bbox_inches="tight")
    plt.close(figure)


OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
plot_score_distributions()
plot_removal_composition()
