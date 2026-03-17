import pandas as pd
import argparse
import os


def load_arff(arff_path):
    data = []
    columns = []

    with open(arff_path, "r") as f:
        in_data = False
        for line in f:
            line = line.strip()
            if line.lower().startswith("@attribute"):
                parts = line.split()
                columns.append(parts[1])
            elif line.lower().startswith("@data"):
                in_data = True
                continue
            elif in_data and line and not line.startswith("%"):
                values = line.split(",")
                data.append(values)
    df = pd.DataFrame(data, columns=columns)

    # convert types
    df["unity_frame"] = df["unity_frame"].astype(int)
    df["x"] = df["x"].astype(float)
    df["y"] = df["y"].astype(float)

    return df


def load_csv(csv_path):
    # CSV with ; as separator and , as decimal
    df = pd.read_csv(csv_path, sep=";", decimal=",")
    df["frameNumber"] = df["frameNumber"].astype(int)
    return df


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("input_csv", help="Path to input CSV file")
    parser.add_argument("input_arff", help="Path to input ARFF file")
    parser.add_argument("output_csv", help="Path to output CSV file", default=None)

    args = parser.parse_args()

    csv_path = args.input_csv
    arff_path = args.input_arff
    output_csv = args.output_csv

    print("Loading CSV...")
    csv_df = load_csv(csv_path)

    print("Loading ARFF...")
    arff_df = load_arff(arff_path)

    # get only relevant columns from arff
    arff_df = arff_df[["unity_frame", "x", "y", "EYE_MOVEMENT_TYPE"]]

    # rename columns
    arff_df = arff_df.rename(columns={
        "x": "gaze_pixel_x",
        "y": "gaze_pixel_y",
        "EYE_MOVEMENT_TYPE": "eye_movement_type"
    })

    print("Merging...")
    merged_df = csv_df.merge(
        arff_df,
        left_on="frameNumber",
        right_on="unity_frame",
        how="left"
    )

    # drop unity_frame as it's the same as frameNumber
    merged_df = merged_df.drop(columns=["unity_frame"])

    # check how many rows have missing eye movement labels
    missing_em = merged_df["eye_movement_type"].isna().sum()
    total_rows = len(merged_df)
    print(f"Missing eye movement labels: {missing_em} out of {total_rows} ({missing_em/total_rows:.2%})")

    print(f"Saving: {output_csv}")
    merged_df.to_csv(output_csv, sep=";", index=False)

    print("Done!")


if __name__ == "__main__":
    main()