variables = {}


def var(v_type: str, name: str = None, value: str = None):
    if v_type == 'set':
        variables[name] = value
        return True
    elif v_type == 'list':
        return variables
    elif v_type == 'query':
        return variables[name]
    elif v_type == 'gkey':
        return [key for key, value in variables.items() if value == value]
