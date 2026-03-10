from pathlib import Path

from arff_utils.AddAttArff import AddAttArff
from arff_utils.GetAcceleration import GetAcceleration
from arff_utils.GetVelocity import GetVelocity
from arff_utils.LoadArff import LoadArff
from arff_utils.SaveArff import SaveArff


def AnnotateData(arffFile, outputFile):
    windowsSize = [1, 2, 4, 8, 16]

    data, metadata, attributes, relation, comments = LoadArff(arffFile)
    comments.append('The number after speed, direction denotes the step size that was used for the calculation.')
    comments.append('Acceleration was calculated between two adjacent samples of the already low pass filtered velocity')

    for step in windowsSize:
        speed, direction = GetVelocity(data, attributes, step)

        speedAttName = f'speed_{step}'
        data, attributes = AddAttArff(data, attributes, speed, speedAttName, 'numeric')

        dirAttName = f'direction_{step}'
        data, attributes = AddAttArff(data, attributes, direction, dirAttName, 'numeric')

        acceleration = GetAcceleration(data, attributes, speedAttName, dirAttName, 1)
        accAttName = f'acceleration_{step}'
        data, attributes = AddAttArff(data, attributes, acceleration, accAttName, 'numeric')

    output_path = Path(outputFile)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    SaveArff(str(output_path), data, metadata, attributes, relation, comments)


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description='Annotate ARFF data with speed, direction and acceleration features.')
    parser.add_argument('arffFile', help='Input ARFF file')
    parser.add_argument('outputFile', help='Output ARFF file')
    args = parser.parse_args()
    AnnotateData(args.arffFile, args.outputFile)
