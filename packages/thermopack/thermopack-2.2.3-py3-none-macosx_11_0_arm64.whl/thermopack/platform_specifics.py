# Module for platform specific stuff. Automatically generated.
# Timestamp : 2024-05-15T10:56:35.338904


import os
DIFFERENTIAL_RETURN_MODE = 'v2'


def get_platform_specifics():
    pf_specifics = {}
    pf_specifics["os_id"] = "darwin"
    pf_specifics["prefix"] = "__"
    pf_specifics["module"] = "_MOD_"
    pf_specifics["postfix"] = ""
    pf_specifics["postfix_no_module"] = "_"
    pf_specifics["dyn_lib"] = "libthermopack.dynlib"
    pf_specifics["diff_return_mode"] = "v2"

    files = os.listdir(os.path.dirname(__file__))
    if not (pf_specifics['dyn_lib'] in files):
        if f'{pf_specifics["dyn_lib"]}.icloud' in files:
            pf_specifics['dyn_lib'] = f'{pf_specifics["dyn_lib"]}.icloud'
        else:
            raise FileNotFoundError(f'ThermoPack binary {pf_specifics["dyn_lib"]} not found in directory {os.path.dirname(__file__)}')

    return pf_specifics
