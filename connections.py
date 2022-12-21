from database.database import Database
from utils.utils import read_config


config = read_config('config.json')
DB = Database(
    host=config.get('db_host'),
    port=config.get('db_port'),
    user=config.get('db_user'),
    password=config.get('db_password'),
    dbname=config.get('db_database'),
    url=config.get('db_url'),
)
