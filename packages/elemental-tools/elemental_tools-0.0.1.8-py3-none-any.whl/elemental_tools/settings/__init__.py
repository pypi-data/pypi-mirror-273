import os.path
from typing import Any, Union, Generator

from elemental_tools.tools import get_package_name
from elemental_tools.pydantic import BaseModel, Field, PrivateAttr
from elemental_tools.db import select, insert
from elemental_tools.db.controller import Controller
from elemental_tools.exceptions import SettingMissing
from elemental_tools.settings.orm import TableSetting
from elemental_tools.logger import Logger
from elemental_tools.system import generate_reference

from elemental_tools.config import config_initializer

config = config_initializer()


if "install" in __name__:
	__logger__ = Logger(app_name=f"{get_package_name(__name__)}", owner="installation", debug=config.debug).log
else:
	__logger__ = Logger(app_name=f"{get_package_name(__name__)}", owner="controller", debug=config.debug).log


class SettingSchema(BaseModel, extra="allow"):
	_controller_: Controller = PrivateAttr()
	_default_: Any = PrivateAttr(default=None)
	ref: str = Field(default_factory=generate_reference)
	name: str = Field(description="Setting Name")
	value: Union[Any, None, bytes] = Field(description="Setting Value", default=None)
	type: str = Field(description="Setting Type", default=None)
	visible: bool = Field(description="Indicates whenever user is allowed to see", default=True)

	"""
	Default setting class
	:param name: The name of the setting
	:param value: The value of the setting
	:param type: The type of the setting
	:param visible: Indicates whenever user is allowed to see
	"""

	def __init__(self, controller: Controller, name: str, default=None):
		super().__init__(name=name)
		self._default_ = default
		self._controller_ = controller

	def __apply_type__(self, default, ignore_default):
		if self.value is None and not ignore_default:
			if self._default_ is not None:
				self.value = self._default_

			if default is not None:
				self.value = default

		if self.value is None:
			raise SettingMissing(self.name)

		if self.type == 'str':
			self.value = self.value.decode('utf-8')
			return self.value
		elif self.type == 'int':
			self.value = int.from_bytes(self.value, byteorder='big')
			return self.value
		elif self.type == 'float':
			self.value = float.fromhex('0x' + self.value.hex())
			return self.value
		elif self.type == 'bool':
			self.value = bool.from_bytes(self.value, byteorder='big')
			return self.value
		elif self.type is None or self.type == "NoneType" or self.type == "bytes":
			return self.value

		raise ValueError(f"Unsupported Data Type: {self.type}")

	def set(self, sub, value, ref: str = None):

		self.type = type(value).__name__

		if value is not None:
			if isinstance(value, str):
				value = value.encode()
			else:
				value = bytes(value)

		if ref is not None:
			self.ref = ref

		self.status = True
		self.value = value
		self.sub = sub

		_doc = self.model_dump()
		query = insert(self._controller_.__orm__).values(**_doc)

		if not config.debug:
			try:
				_insert = self._controller_.insert(query, upsert=True, index_elements=["sub", "name"])
				return _insert

			except Exception as e:
				__logger__("error", f"Failed to store Setting because of exception: {str(e)}")

			return False

		__logger__("info", f"Applying Setting: {str(_doc)}")
		_insert = self._controller_.insert(query, upsert=True, index_elements=["sub", "name"])

		return _insert

	def get(self, sub, default=None, ignore_default: bool = False):
		self.value = None
		query_result = None

		__logger__("info", f"Loading Setting:\n\tName:{self.name}\n\tType:{self.type}\n\tValue:{self.value}")

		try:
			statement = select(self._controller_.__orm__).filter_by(name=self.name, sub=sub)
			query_result = self._controller_.query(statement)
		except:
			pass

		if query_result is not None:
			self.value = query_result["value"]
			for key, value in query_result.items():
				setattr(self, key, value)

		return self.__apply_type__(default, ignore_default)


class SettingController(Controller):
	"""
	Manipulates settings
	"""
	__orm__ = TableSetting
	__schema__ = SettingSchema

	def __init__(self):
		__logger__("info", "Initializing Setting Controller", origin="setting-controller", debug=config.debug)
		super().__init__()

		self.debug = config.debug

		self.test = SettingSchema(self, "test")
		self.database_version = SettingSchema(self, "database_version", default=0)

		self.root_ref = SettingSchema(self, "root_ref")

		self.developer = SettingSchema(self, "developer", default="Elemental")
		self.website = SettingSchema(self, "website", default="http://elemental.run/")
		self.company_name = SettingSchema(self, "company_name", default="Elemental")

		self.crypto_default_taxes = SettingSchema(self, "crypto_default_taxes", default=0.0065)
		self.transaction_cooldown = SettingSchema(self, "transaction_cooldown", default=5)

		self.attendant_default_response_header = SettingSchema(self, "attendant_default_response_header", default="[ $company_name - Self Attedance ]")
		self.attendant_default_response_request_attendance = SettingSchema(self, "attendant_default_response_request_attendance", default="""To obtain assistance from one of our attendants please type\nI want to talk with an attendant.\nAnd we will help you as fast as we can!""")
		self.attendant_default_response_attendance_time = SettingSchema(self,"attendant_default_response_attendance_time", default="""Remember that our attendance time is from: 9AM to 6PM.""")

		self.google_sheet_users_root_folder_id = SettingSchema(self, "google_sheet_users_root_folder_id", default="")
		self.google_sheet_default_permissions = SettingSchema(self, "google_sheet_default_permissions", default=[])
		self.google_api_credentials_json = SettingSchema(self, "google_api_credentials_json", default="")

	def get_all(self, sub, only_visible: bool = True) -> Union[Generator[SettingSchema, None, None], None]:
		stmt = select(self.__orm__).filter_by(sub=sub)
		if only_visible:
			stmt.filter_by(visible=True)

		query_result = self.query_all(stmt)

		if query_result is not None:
			for e in query_result:
				this_schema = SettingSchema(self, e["name"])

				this_schema.visible = e["visible"]
				this_schema.type = e["type"]
				this_schema.value = e["value"]
				this_schema.sub = e["sub"]
				this_schema.ref = e["ref"]
				this_schema.status = e["status"]

				yield this_schema

