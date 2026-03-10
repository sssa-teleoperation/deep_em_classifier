from pathlib import Path

from AnnotateData import AnnotateData


def AnnotateDataAll(arffBasepath='../data/inputs/GazeCom_ground_truth', outBasepath='../data/inputs/GazeCom_features'):
    base_path = Path(arffBasepath)
    out_base_path = Path(outBasepath)

    for item in sorted(base_path.glob('*')):
        if not item.is_dir():
            continue

        name = item.name
        outputDir = out_base_path / name
        outputDir.mkdir(parents=True, exist_ok=True)

        arffFiles = sorted((base_path / name).glob('*.arff'))
        for arffFile in arffFiles:
            outputFile = outputDir / f'{arffFile.stem}.arff'
            print(f'Processing {arffFile}')
            AnnotateData(str(arffFile), str(outputFile))


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description='Annotate all ARFF files in subfolders with features.')
    parser.add_argument('arffBasepath', nargs='?', default='../data/inputs/GazeCom_ground_truth')
    parser.add_argument('outBasepath', nargs='?', default='../data/inputs/GazeCom_features')
    args = parser.parse_args()
    AnnotateDataAll(args.arffBasepath, args.outBasepath)
