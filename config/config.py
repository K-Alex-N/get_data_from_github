from os import path, curdir
from dataclasses import dataclass
import yaml

# ----------------------------------- #
# constants
# ----------------------------------- #

# если запускать это файл то путь будет не верный, это нормально тк запускается main
PATH_TO_JSON = path.join(path.abspath(curdir), 'app', 'store', 'json_files')

# ----------------------------------- #
#
# ----------------------------------- #

@dataclass
class DatabaseConfig:
    host: str
    port: int
    user: str
    password: str
    database: str

@dataclass
class Config:
    database: DatabaseConfig = None


def setup_config(app):
    config_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "config.yml")
    with open(config_path) as f:
        raw_config = yaml.safe_load(f)

    app.config = Config(database=DatabaseConfig(**raw_config["database"]))

