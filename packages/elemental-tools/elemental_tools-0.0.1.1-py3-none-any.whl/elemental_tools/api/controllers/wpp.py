from elemental_tools.config import config_initializer
from elemental_tools.db import Index
from elemental_tools.logger import Logger

config = config_initializer()


class WppController:
	table_name = f'wpp'
	__logger__ = Logger(app_name=config.app_name, owner=table_name, destination=config.log_path).log

	indexes = [
		Index(['cellphone', 'msg_id'], unique=True, sparse=True),
		Index(['wpp_user_id', 'msg_id'], unique=True, sparse=True),
	]
