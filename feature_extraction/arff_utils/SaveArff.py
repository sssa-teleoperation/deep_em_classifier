from .IsNomAttribute import IsNomAttribute


def SaveArff(arffFile, data, metadata, attributes, relation, comments=None):
    if comments is None:
        comments = []

    for field in ['width_px', 'height_px', 'width_mm', 'height_mm', 'distance_mm']:
        if field not in metadata:
            raise AssertionError(f'metadata should contain "{field}" field')

    if len(relation) == 0:
        raise AssertionError('relation should not be empty')

    if len(attributes) != data.shape[1]:
        raise AssertionError('attribute number should be the same with data')

    numAtts = len(attributes)
    attType = [-1] * numAtts
    numMaps = [None] * numAtts
    for i, (_, att_datatype) in enumerate(attributes):
        isNom, _, numericMap = IsNomAttribute(att_datatype)
        if att_datatype.lower() == 'integer':
            attType[i] = 1
        elif att_datatype.lower() == 'numeric':
            attType[i] = 2
        elif isNom:
            attType[i] = 3
            numMaps[i] = numericMap

    with open(arffFile, 'w', encoding='utf-8') as fid:
        fid.write(f'@RELATION {relation}\n\n')

        fid.write(f'%@METADATA width_px {int(metadata["width_px"])}\n')
        fid.write(f'%@METADATA height_px {int(metadata["height_px"])}\n')
        fid.write(f'%@METADATA width_mm {float(metadata["width_mm"]):.2f}\n')
        fid.write(f'%@METADATA height_mm {float(metadata["height_mm"]):.2f}\n')
        fid.write(f'%@METADATA distance_mm {float(metadata["distance_mm"]):.2f}\n\n')

        for key, value in metadata.get('extra', []):
            fid.write(f'%@METADATA {key} {value}\n')
        fid.write('\n')

        for name, att_datatype in attributes:
            fid.write(f'@ATTRIBUTE {name} {att_datatype}\n')

        if comments:
            fid.write('\n')
            for comment in comments:
                if len(comment) == 0 or comment[0] != '%':
                    comment = f'%{comment}'
                fid.write(f'{comment}\n')

        fid.write('\n@DATA\n')

        for row in data:
            parts = []
            for ind in range(numAtts):
                value = row[ind]
                if attType[ind] == 1:
                    parts.append(f'{int(value)}')
                elif attType[ind] == 2:
                    parts.append(f'{float(value):.2f}')
                elif attType[ind] == 3:
                    parts.append(numMaps[ind][float(value)])
                else:
                    raise RuntimeError(f'Attribute type "{attType[ind]}" is not recognised')
            fid.write(','.join(parts) + '\n')
