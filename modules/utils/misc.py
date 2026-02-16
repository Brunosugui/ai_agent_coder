import json
import argparse

from pathlib import Path
from dataclasses import asdict

from hyperpyyaml import load_hyperpyyaml


color_dict = {
    "red": "\033[0;31m",
    "green": "\033[0;32m",
    "cyan": "\033[0;36m",
    "reset": "\033[0m"

}


def c(in_str, color):
    return f"{color_dict[color]}{in_str}{color_dict['reset']}"


def get_args():
    parser = argparse.ArgumentParser(description="Coder AI agent script args.")

    parser.add_argument("-c", "--config", default="configs/default.yaml",
        help="The path to the config file.")

    args = parser.parse_args()
    args_dict = vars(args)

    return args_dict


def load_config(config_path):
    config_path = Path(config_path)

    if not config_path.exists():
        raise FileNotFoundError(f"Could not find \'{config_path}\'")

    config = load_hyperpyyaml(config_path)

    return config


def save_state(state, path):
    with open(path, "a") as f:
        f.write(json.dumps(asdict(state)) + "\n")

def load_state(path):
    with open(path, 'r') as f:
        lines = f.readlines()
    last_line = lines[-1].strip()
    return json.loads(last_line)
