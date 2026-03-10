def GetAttPositionArff(arffAttributes, attribute, check=True):
    attIndex = -1
    for index, (att_name, _) in enumerate(arffAttributes):
        if att_name.lower() == attribute.lower():
            attIndex = index

    if check and attIndex < 0:
        raise AssertionError(f'Attribute "{attribute}" not found')

    return attIndex
