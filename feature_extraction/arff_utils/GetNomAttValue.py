def GetNomAttValue(attDatatype):
    openCurl = attDatatype.find('{')
    closeCurl = attDatatype.find('}')

    if openCurl == -1 and closeCurl == -1:
        return None

    if openCurl == -1 or closeCurl == -1:
        raise AssertionError(f'Invalid attribute datatype {attDatatype}')

    if attDatatype.find('{', openCurl + 1) != -1:
        raise AssertionError(f'Invalid attribute datatype {attDatatype}')
    if attDatatype.find('}', closeCurl + 1) != -1:
        raise AssertionError(f'Invalid attribute datatype {attDatatype}')

    attValue = attDatatype[openCurl:closeCurl + 1]
    return ''.join(attValue.split())
