import pathlib
import yaml

BASE_DIR = pathlib.Path(__file__).parent.parent
config_path = BASE_DIR / 'config.yaml'


def get_config(path):
    with open(path) as f:
        conf = yaml.safe_load(f)
        conf["http_real_address"] = f"http://{conf['http_real_host']}:{conf['http_real_host_port']}"
    return conf


config = get_config(config_path)
