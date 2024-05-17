import os
import json
from pathlib import Path

def get_config():
    config_file = os.path.join(os.path.expanduser('~'), '.oncosplice_setup', 'config.json')
    if Path(config_file).exists():
        config_setup = {k: Path(p) for k, p in json.loads(open(config_file).read()).items()}

    else:
        print("Database not set up.")
        config_setup = {}

    return config_setup