import inspect

RULESET_MODULE = "pywrparser.rulesets"

def get_rulesets(rm=RULESET_MODULE):
    import pywrparser.rulesets
    mods = inspect.getmembers(pywrparser.rulesets, inspect.ismodule)
    modules = {}
    for mod in mods:
        modules[mod[1].__name__] = {
            "modpath": mod[0],
            "version": mod[1].__version__,
            "description": mod[1].__description__
        }

    return modules


def describe_rulesets():
    modules = get_rulesets()

    output = f"Available Rulesets:\n"
    for idx, (name, mod) in enumerate(modules.items(),1):
        output += f"[{idx}]\tName: '{name}'  Version: {mod['version']}\n\t{mod['description']}\n"

    return output


def identify_types(module):
    pass
