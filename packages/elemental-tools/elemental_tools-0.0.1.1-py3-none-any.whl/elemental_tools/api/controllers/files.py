from datetime import datetime

from elemental_tools.api.orm.files import TableFiles
from elemental_tools.db import insert, select
from elemental_tools.db.controller import Controller
from elemental_tools.system import current_timestamp


class FilesController(Controller):
	__orm__ = TableFiles

	sub = None
	institution_ref = None

	def __init__(self, sub, institution_ref):
		super().__init__()
		self.sub = sub
		self.institution_ref = institution_ref

	def save_processed_csv(self, filename):

		stmt = insert(self.__orm__).values(
			date=current_timestamp(),
			filename=filename,
			sub=self.sub,
			institution_ref=self.institution_ref
		)

		try:
			insert_result = self.insert(stmt)
			if insert_result is not None:
				return insert_result[0]["ref"]

		except:
			self.__logger__("critical", "Cannot save processed csv")

		return False

	def retrieve_processed_csv(self, filename):

		try:
			self.__logger__("info", f"Looking for processed file: {filename} ")

			_result = self.query_all(select(self.__orm__).filter_by(filename=filename, sub=self.sub, ref=self.institution_ref))

			return _result

		except:
			self.__logger__("alert", "File already processed!")

