"""Plots two heatmaps: 1. changes of profession share and 2. changes in female proportions within these professions"""

from pathlib import Path
import matplotlib.pyplot as plt
from matplotlib.colors import BoundaryNorm, Normalize
from matplotlib.lines import Line2D
from matplotlib.patches import Patch
import pandas as pd


BASE_DIR = Path(__file__).resolve().parent.parent
OUTPUT_DIR = BASE_DIR / "analysis" / "outputs"
INPUT_PATH = OUTPUT_DIR / "filtering_distribution_comparison.csv"

EXPERIMENTS = [
    ("GPT", "GPT"),
    ("GPT", "Llama"),
    ("Llama", "GPT"),
    ("Llama", "Llama"),
]

SCORING_MODES = [
    ("content_only", "CO"),
    ("explanation_aware", "EA"),
]

# Discrete intervals for second heatmap
GENDER_BOUNDS = [-50, -30, -20, -10, -5, -2, -1, 1, 2, 5, 10, 20, 30, 50]


def draw_heatmap(axis, data, value_column, title):
    """Draws one heatmap for either profession-share changes or female-proportion changes """
    professions = data["profession_name"].drop_duplicates().tolist()
    changes = pd.DataFrame(index=professions)
    kept_counts = pd.DataFrame(index=professions)

    for generator, filtering_model in EXPERIMENTS: # loop over 4 generator filter combinations
        for scoring_mode, short_label in SCORING_MODES: # loop over 2 scoring modes
            selected = data[ # select correct data for the config
                (data["generator"] == generator)
                & (data["filtering_model"] == filtering_model)
                & (data["scoring_mode"] == scoring_mode)
            ]
            selected = selected.set_index("profession_name")

            # Make label, extract relevant data and keep counts of total kept biographies
            label = f"{generator}/{filtering_model}\n{short_label}"
            changes[label] = selected[value_column]
            kept_counts[label] = selected["kept_total"]

    limit = changes.abs().max().max() # decide the scale of the heatmap by finding largest absolute change
    if limit == 0:
        limit = 1

    if value_column == "women_change_pp": # set the color scale for the right heatmap
        if changes.min().min() < GENDER_BOUNDS[0] or changes.max().max() > GENDER_BOUNDS[-1]:
            raise ValueError("Gender changes fall outside the chosen colour intervals.")
        colours = plt.get_cmap("RdBu_r", len(GENDER_BOUNDS) - 1).copy()
        colour_scale = BoundaryNorm(GENDER_BOUNDS, colours.N)
    else:
        colours = plt.get_cmap("RdBu_r").copy()
        colour_scale = Normalize(vmin=-limit, vmax=limit)

    colours.set_bad("#d9d9d9") # missing values color: now as grey

    image = axis.imshow( # draw the cells
        changes.to_numpy(),
        aspect="auto",
        interpolation="nearest",
        cmap=colours,
        norm=colour_scale,
    )

    axis.set_xticks( # label the columns
        range(len(changes.columns)),
        labels=changes.columns,
        rotation=45,
        ha="right",
        fontsize=9,
    )

    # clean up profession names
    occupation_labels = []
    for profession in professions:
        occupation_labels.append(profession.replace("_", " "))

    # adds profession label
    axis.set_yticks(
        range(len(professions)),
        labels=occupation_labels,
        fontsize=10,
    )
    axis.set_title(title, fontsize=13, pad=12)
    axis.tick_params(length=0)

    # Separate the four generator/filter combinations.
    for boundary in [1.5, 3.5, 5.5]:
        axis.axvline(boundary, color="white", linewidth=2)

    # finds profession with 0 retained biographies and adds circle to cell (for left heatmap)
    for row in range(len(professions)):
        for column in range(len(changes.columns)):
            if kept_counts.iloc[row, column] == 0 and value_column == "profession_change_pp":
                axis.plot(
                    column,
                    row,
                    marker="o",
                    markersize=5,
                    markerfacecolor="white",
                    markeredgecolor="black",
                    markeredgewidth=0.7,
                    linestyle="None",
                )

    if value_column == "women_change_pp": # for the right heatmap add color bar
        colour_bar = axis.figure.colorbar(
            image,
            ax=axis,
            fraction=0.04,
            pad=0.03,
            boundaries=GENDER_BOUNDS,
            ticks=GENDER_BOUNDS,
            spacing="uniform",
            drawedges=True,
        )
        colour_bar.set_label("Change in female proportion (pp)", fontsize=10)
    else: # for the left heatmap add color bar
        colour_bar = axis.figure.colorbar(
            image,
            ax=axis,
            fraction=0.04,
            pad=0.03,
        )
        colour_bar.set_label("Change in profession share (pp)", fontsize=10)

    # Show the actual minimum and maximum on the left colour bar and format its labels
    if value_column == "profession_change_pp":
        minimum = changes.min().min()
        maximum = changes.max().max()
        ticks = [minimum]
        for tick in colour_bar.get_ticks():
            if minimum < tick < maximum:
                ticks.append(tick)
        ticks.append(maximum)

        tick_labels = []
        for tick in ticks:
            tick_labels.append(f"{tick:.2f}".rstrip("0").rstrip("."))

        colour_bar.set_ticks(ticks, labels=tick_labels)
        colour_bar.ax.set_ylim(minimum, maximum)


def plot_heatmaps():
    """Reads the comparison csv and plots 2 heatmaps by using the draw_heatmap function twice"""
    data = pd.read_csv(INPUT_PATH)

    # We dont need total for the heatmap only the professions
    data = data[data["profession_name"] != "TOTAL"]

    figure, axes = plt.subplots(1, 2, figsize=(16, 10), sharey=True)
    # Call draw_heatmap twice to fill the left and right panels
    draw_heatmap(
        axes[0],
        data,
        "profession_change_pp",
        "(a) Change in profession share",
    )
    draw_heatmap(
        axes[1],
        data,
        "women_change_pp",
        "(b) Change in female proportion within professions",
    )

    axes[1].tick_params(labelleft=False)

    # The legend
    legend_items = [
        Line2D(
            [], [], marker="o", markersize=5,
            markerfacecolor="white", markeredgecolor="black",
            markeredgewidth=0.7, linestyle="None",
            label="No biographies retained",
        ),
        Patch(
            facecolor="#d9d9d9", edgecolor="none",
            label="Undefined gender proportion",
        ),
    ]
    figure.legend(
        handles=legend_items,
        loc="lower center",
        bbox_to_anchor=(0.5, 0.035),
        ncol=2,
        frameon=False,
        fontsize=10,
    )

    figure.text(
        0.5,
        0.015,
        "Columns: generator/filtering model. "
        "CO = content-only; EA = explanation-aware.",
        ha="center",
        fontsize=10,
    )

    figure.tight_layout(rect=(0, 0.12, 1, 1))

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    output_path = OUTPUT_DIR / "filtering_distribution_heatmaps.png"

    figure.savefig(output_path, dpi=300, bbox_inches="tight")
    plt.close(figure)

    print(f"Saved: {output_path}")


plot_heatmaps()
