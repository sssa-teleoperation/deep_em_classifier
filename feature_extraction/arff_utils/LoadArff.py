import numpy as np

from .GetNomAttValue import GetNomAttValue
from .IsNomAttribute import IsNomAttribute


def _to_number(value):
    try:
        return float(value)
    except ValueError:
        return float('nan')


def LoadArff(arffFile):
    data = []
    metadata = {
        'width_px': -1,
        'height_px': -1,
        'width_mm': -1,
        'height_mm': -1,
        'distance_mm': -1,
        'extra': [],
    }
    attributes = []
    relation = ''
    comments = []

    nomMat = []
    nomMaps = []

    with open(arffFile, 'r', encoding='utf-8') as fid:
        header_complete = False
        for raw_line in fid:
            fline = raw_line.rstrip('\n')
            stripped = fline.strip()
            words = stripped.split(' ')
            words = [word for word in words if word != '']

            if len(words) > 1 and words[0].lower() == '@relation':
                relation = words[1].lower()
            elif len(words) > 2 and words[0].lower() == '%@metadata' and words[1].lower() == 'width_px':
                metadata['width_px'] = _to_number(words[2])
            elif len(words) > 2 and words[0].lower() == '%@metadata' and words[1].lower() == 'height_px':
                metadata['height_px'] = _to_number(words[2])
            elif len(words) > 2 and words[0].lower() == '%@metadata' and words[1].lower() == 'width_mm':
                metadata['width_mm'] = _to_number(words[2])
            elif len(words) > 2 and words[0].lower() == '%@metadata' and words[1].lower() == 'height_mm':
                metadata['height_mm'] = _to_number(words[2])
            elif len(words) > 2 and words[0].lower() == '%@metadata' and words[1].lower() == 'distance_mm':
                metadata['distance_mm'] = _to_number(words[2])
            elif len(words) > 2 and words[0].lower() == '%@metadata':
                metadata['extra'].append((words[1], words[2]))
            elif len(words) > 2 and words[0].lower() == '@attribute':
                name = words[1].lower()
                datatype = words[2]
                isNom, nominalMap, _ = IsNomAttribute(fline)
                if isNom:
                    datatype = GetNomAttValue(fline)
                    nomMaps.append(nominalMap)
                else:
                    nomMaps.append({})
                attributes.append((name, datatype))
                nomMat.append(isNom)
            elif len(fline) > 0 and fline[0] == '%':
                comments.append(fline)
            elif len(words) > 0 and words[0].lower() == '@data':
                header_complete = True
                break

        if not header_complete:
            return np.empty((0, len(attributes))), metadata, attributes, relation, comments

        for raw_line in fid:
            line = raw_line.strip()
            if not line:
                continue
            if line.startswith('%'):
                continue

            values = [token.strip() for token in line.split(',')]
            if len(values) != len(attributes):
                continue

            row = []
            for index, value in enumerate(values):
                if nomMat[index]:
                    row.append(nomMaps[index][value])
                else:
                    row.append(_to_number(value))
            data.append(row)

    if len(data) == 0:
        return np.empty((0, len(attributes))), metadata, attributes, relation, comments

    return np.asarray(data, dtype=float), metadata, attributes, relation, comments
