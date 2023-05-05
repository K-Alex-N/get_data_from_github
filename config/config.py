import os
import yaml

# ----------------------------------- #
# Path
# ----------------------------------- #

BASE_DIR = os.path.realpath('./')
PATH_TO_CONFIG_YML = os.path.join(BASE_DIR, 'config', 'config.yml')
JSON_DIR = os.path.join(BASE_DIR, 'app', 'store', 'json_files')


# ----------------------------------- #
# config
# ----------------------------------- #

with open(PATH_TO_CONFIG_YML) as f:
    raw_config = yaml.safe_load(f)

secret_key = raw_config["SECRET_KEY"]

db = 'dev_db' # change according to status (dev_db or prod_db)
user =      raw_config[db]['user']
password =  raw_config[db]['password']
host =      raw_config[db]['host']
port =      raw_config[db]['port']
database =  raw_config[db]['database']

if db == 'dev_db':
    debug = True
elif db == 'prod_db':
    debug = False




# https://flask.palletsprojects.com/en/2.3.x/config/
# class Config(object):
#     TESTING = False
#
# class ProductionConfig(Config):
#     DATABASE_URI = 'mysql://user@localhost/foo'
#
# class DevelopmentConfig(Config):
#     DATABASE_URI = "sqlite:////tmp/foo.db"
#
# class TestingConfig(Config):
#     DATABASE_URI = 'sqlite:///:memory:'
#     TESTING = True
#
# app.config.from_object('configmodule.ProductionConfig')