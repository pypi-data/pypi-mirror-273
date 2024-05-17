import yaml
from pyzjr.core.general import is_not_None

def yamlread(path, name=None):
    with open(path) as file:
        data = yaml.load(file, Loader=yaml.FullLoader)
    value = data[name] if is_not_None(name) else data

    return value