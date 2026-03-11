import pandas as pd
import matplotlib.pyplot as plt
import argparse



def read_arff(filepath):
    data_started = False
    rows = []
    columns = []

    with open(filepath, "r") as f:
        for line in f:
            line = line.strip()

            if not line or line.startswith("%"):
                continue

            if line.lower().startswith("@attribute"):
                parts = line.split()
                columns.append(parts[1])
                continue

            if line.lower().startswith("@data"):
                data_started = True
                continue

            if data_started:
                rows.append(line.split(","))

    df = pd.DataFrame(rows, columns=columns)

    # convert numeric columns
    for col in df.columns:
        if col != "EYE_MOVEMENT_TYPE":
            df[col] = pd.to_numeric(df[col])

    return df


def parse_args():
    parser = argparse.ArgumentParser(description="Plot eye movements from ARFF file")
    parser.add_argument("input_arff",help="Path to input ARFF file")
    return parser.parse_args()


def main(input_arff):
    df = read_arff(input_arff)

    color_map = {
        "SACCADE": "red",
        "FIX": "green",
        "SP": "blue",
        "NOISE": "yellow",
        "BLINK": "black",
        "UNKNOWN": "gray",
        "NOISE_CLUSTER": "orange",
        "PSO": "purple"
    }

    colors = df["EYE_MOVEMENT_TYPE"].map(color_map).fillna("gray")

    # legend handles — only for types actually present in the data
    from matplotlib.lines import Line2D
    present_types = df["EYE_MOVEMENT_TYPE"].unique()
    legend_handles = [
        Line2D([0], [0], marker='o', color='w', markerfacecolor=color_map.get(em_type, 'gray'),
               markersize=7, label=em_type)
        for em_type in sorted(present_types)
    ]

    fig, axes = plt.subplots(2, 1, figsize=(12, 6), sharex=True)

    axes[0].scatter(df["time"], df["x"], c=colors, s=5)
    axes[0].set_ylabel("gaze x (px)")
    axes[0].set_title("Eye movements - X")
    axes[0].legend(handles=legend_handles, title="Eye movement", loc="upper right", fontsize=8)

    axes[1].scatter(df["time"], df["y"], c=colors, s=5)
    axes[1].set_ylabel("gaze y (px)")
    axes[1].set_xlabel("time (µs)")
    axes[1].set_title("Eye movements - Y")

    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    args = parse_args()
    main(args.input_arff)