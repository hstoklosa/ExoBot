from .cogs import *
from .managers import *
from .utils import *


env = read_env_file('exobot/config/.env')
config = read_json_file('exobot/config/config.json')