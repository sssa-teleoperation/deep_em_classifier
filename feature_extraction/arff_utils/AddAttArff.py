import numpy as np


def AddAttArff(data, attributes, attData, attName, attType):
    if data.shape[0] != len(attData):
        raise AssertionError('Provided attribute does not have same number of entries as initial data')

    for existing_name, _ in attributes:
        if existing_name.lower() == attName.lower():
            raise RuntimeError(f'Attributes "{attName}" already exists. Cannot add it.')

    newAttributes = list(attributes)
    newAttributes.append((attName, attType))

    att_column = np.asarray(attData, dtype=float).reshape(-1, 1)
    newData = np.concatenate((data, att_column), axis=1)
    return newData, newAttributes
