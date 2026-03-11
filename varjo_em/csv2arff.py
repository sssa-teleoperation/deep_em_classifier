import pandas as pd
from decimal import Decimal
import argparse


DIST_CAMERA_UNITY = 7000
WIDTH_UNITY = 9600
HEIGHT_UNITY = 5400


def varjo2pixel(gx_varjo, gy_varjo, gz_varjo, dist_camera_unity, width_unity, height_unity):
    if gz_varjo == 0:
        return int(0), int(0)  # center pixel if gaze_z is zero to avoid division by zero
    # from Varjo coordinates to Unity coordinates
    gx_unity = (-dist_camera_unity) * (gx_varjo/ gz_varjo)
    gz_unity = (dist_camera_unity) * (gy_varjo/ gz_varjo)
    # from Unity coordinates to pixel coordinates
    gx_px = (-gx_unity + (width_unity / 2)) / 10
    gy_px = (-gz_unity + (height_unity / 2)) / 10

    return int(gx_px), int(gy_px)


def status2confidence(status):
    if status == "Valid":
        return 1
    else:
        return 0


def parse_args():
    parser = argparse.ArgumentParser(description="Convert Varjo CSV gaze data to ARFF format")
    parser.add_argument("input_csv", help="Path to input CSV file")
    parser.add_argument("output_arff", help="Path to output ARFF file")
    return parser.parse_args()


def main(input_csv, output_arff):

    # reads the CSV file into a pandas DataFrame
    df = pd.read_csv(
        input_csv,
        sep=";",
        decimal=","
    )

    with open(output_arff, "w") as fid:

        # metadata
        fid.write("%@METADATA width_px 960.0\n")
        fid.write("%@METADATA height_px 540.0\n")
        fid.write("%@METADATA width_mm 1100.8\n")
        fid.write("%@METADATA height_mm 619.2\n")
        fid.write("%@METADATA distance_mm 802.667\n")

        fid.write("\n")

        # relation
        fid.write("@RELATION gaze_labels\n\n")

        # attributi
        fid.write("@ATTRIBUTE time INTEGER\n")
        fid.write("@ATTRIBUTE unity_frame INTEGER\n")
        fid.write("@ATTRIBUTE x NUMERIC\n")
        fid.write("@ATTRIBUTE y NUMERIC\n")
        fid.write("@ATTRIBUTE confidence NUMERIC\n")

        fid.write("\n@DATA\n")

        for _, row in df.iterrows():

            # convert time from nanoseconds to microseconds
            time_ns = Decimal(row["captureTime"])
            time_us = int(time_ns / Decimal(1000))

            # unity frame number 
            frame = int(row["frameNumber"])

            # convert gaze vector in pixel coordinates
            gx = row["gaze_forward_x"]
            gy = row["gaze_forward_y"]
            gz = row["gaze_forward_z"]

            x, y = varjo2pixel(gx, gy, gz, DIST_CAMERA_UNITY, WIDTH_UNITY, HEIGHT_UNITY)

            # convert gaze status to confidence
            conf = status2confidence(row["gaze_status"])

            # handle missing data
            if x is None or y is None:
                print(f"Warning: missing gaze data at time {time_us} us, frame {frame}")
                x_str = "?"
                y_str = "?"
                conf = 0
            else:
                x_str = f"{float(x):.6f}"
                y_str = f"{float(y):.6f}"
            
            # write data to ARFF file
            fid.write(
                f"{time_us},{frame},{x_str},{y_str},{conf}\n"
            )


if __name__ == "__main__":
    args = parse_args()
    main(args.input_csv, args.output_arff)