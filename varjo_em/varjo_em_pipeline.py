import os
import subprocess
import argparse
import glob


BASE_DIR = "/ws/src/deep_em_classifier"


def run_command(cmd):
    print(f"\n[RUN] {cmd}")
    result = subprocess.run(cmd, shell=True)
    if result.returncode != 0:
        raise RuntimeError(f"Error doing: {cmd}")

def ensure_dir(path):
    os.makedirs(path, exist_ok=True)

def find_csv_file(trial):
    raw_csv_dir = os.path.join(BASE_DIR, "example_data/csv")
    pattern = os.path.join(raw_csv_dir, f"*trial_{trial}_*.csv")
    csv_files = glob.glob(pattern)
    if not csv_files:
        raise FileNotFoundError(f"No CSV file found for trial {trial} in {raw_csv_dir}")
    return csv_files[0]  # Return the first match

def main():
    parser = argparse.ArgumentParser(description="Pipeline raw CSV -> raw ARFF -> features ARFF -> em ARFF")
    parser.add_argument("--trial", required=True, help="Trial number")
    parser.add_argument("--show_plot", action="store_true", help="Generate plots")

    args = parser.parse_args()

    trial = args.trial
    csv_path = find_csv_file(trial)

    # Script paths
    csv2arff_script = os.path.join(BASE_DIR, "varjo_em/csv2arff.py")
    annotate_script = os.path.join(BASE_DIR, "feature_extraction/AnnotateData.py")
    model_script = os.path.join(BASE_DIR, "blstm_model_run.py")
    plot_script = os.path.join(BASE_DIR, "varjo_em/plot_em.py")
    model_path = os.path.join(BASE_DIR, "model/Conv_sample_windows_epochs_1000_without_doves_final_architecture.h5")

    # Output folders
    raw_dir = os.path.join(BASE_DIR, "example_data/arff_raw")
    feat_dir = os.path.join(BASE_DIR, "example_data/arff_features")
    em_dir = os.path.join(BASE_DIR, "example_data/arff_em")

    ensure_dir(raw_dir)
    ensure_dir(feat_dir)
    ensure_dir(em_dir)

    # Base filename
    filename = os.path.splitext(os.path.basename(csv_path))[0]

    raw_arff = os.path.join(raw_dir, f"{filename}.arff")
    feat_arff = os.path.join(feat_dir, f"{filename}_features.arff")
    em_arff = os.path.join(em_dir, f"{filename}_em.arff")

    # STEP 1: CSV -> ARFF raw
    cmd1 = f"python {csv2arff_script} {csv_path} {raw_arff}"
    run_command(cmd1)

    # STEP 2: ARFF raw -> ARFF with features
    cmd2 = f"python {annotate_script} {raw_arff} {feat_arff}"
    run_command(cmd2)

    # STEP 3: ARFF with features -> ARFF with EM classification
    cmd3 = (
        f"python {model_script} "
        f"--feat speed direction "
        f"--model {model_path} "
        f"--in {feat_arff} "
        f"--out {em_arff}"
    )
    run_command(cmd3)

    # STEP 4: Optional plotting
    if args.show_plot:
        cmd4 = f"python {plot_script} {em_arff}"
        run_command(cmd4)

    print("\n✅ Pipeline completed!")
    print(f"Raw ARFF: {raw_arff}")
    print(f"Feature ARFF: {feat_arff}")
    print(f"EM ARFF: {em_arff}")

if __name__ == "__main__":
    main()