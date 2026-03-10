def IsNomAttribute(attDatatype):
    openCurl = attDatatype.find('{')
    closeCurl = attDatatype.find('}')

    if openCurl == -1 and closeCurl == -1:
        return False, {}, {}

    if openCurl == -1 or closeCurl == -1:
        raise AssertionError(f'Invalid attribute datatype {attDatatype}')

    if attDatatype.find('{', openCurl + 1) != -1:
        raise AssertionError(f'Invalid attribute datatype {attDatatype}')
    if attDatatype.find('}', closeCurl + 1) != -1:
        raise AssertionError(f'Invalid attribute datatype {attDatatype}')

    value = attDatatype[openCurl + 1:closeCurl]
    value = ''.join(value.split())

    keys = value.split(',')
    nominalMap = {key: float(index) for index, key in enumerate(keys)}
    numericMap = {float(index): key for index, key in enumerate(keys)}
    return True, nominalMap, numericMap
