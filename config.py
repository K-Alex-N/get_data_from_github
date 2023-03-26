from dataclasses import dataclass
import yaml


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


def setup_config(app, config_path: str):
    print(config_path)
    with open(config_path) as f:
        raw_config = yaml.safe_load(f)
        print(raw_config)

    app.config = Config(database=DatabaseConfig(**raw_config["database"]))

# здесь должны сохраняться настройки для каждого пользователя
# настройки сохранять в БД
# пример:   пользователь 1: основной сайт(озон), настройки (в JSON файле)
#           пользователь 1: основной сайт(гитхаб), настройки (в JSON файле)
#           пользователь 2: основной сайт(гитхаб), настройки (в JSON файле)
