import jsonschema, json
def checkSchema(original, target, schema):
    """
    OCPP 규격과 다른지 체크, 다를 경우 False Return
    :param original: 점검 대상 스키마 명
    :param target: 점검 대상 Json 본체
    :return: True : 규격 동일, False: 규격 다름
    """

    try:
        schema = open(f"./{schema}/schemas/" + original + ".json").read().encode('utf-8')
        jsonschema.validate(instance=target, schema=json.loads(schema))
    except jsonschema.exceptions.ValidationError as e:
        return False, e.message
    return True, None

def tc_render(adict, k, value):
    import datetime
    if isinstance(adict, dict):
        for key in adict.keys():
            if adict[key] == k:
                try:
                    adict[key] = value
                except ValueError:
                    pass  # do nothing if the timestamp is already in the correct format
            elif isinstance(adict[key], (dict, list)):
                tc_render(adict[key], k, value)
    elif isinstance(adict, list):
        for l in adict:
            tc_render(l, k, value)
