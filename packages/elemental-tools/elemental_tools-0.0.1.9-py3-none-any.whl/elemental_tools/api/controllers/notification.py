from datetime import datetime

from elemental_tools.api.orm.notification import TableNotification
from elemental_tools.api.schemas.notification import NotificationSchema
from elemental_tools.db import select, update
from elemental_tools.db.controller import Controller
from elemental_tools.system import current_timestamp


class NotificationController(Controller):
	__orm__ = TableNotification

	def __init__(self, responses_selector=None, default_selector=None):
		super().__init__()

		self.notification_selector = default_selector
		if self.notification_selector is None:
			self.notification_selector = select(self.__orm__).where((not self.__orm__.status) & (self.__orm__.content is not None))

		self.responses_selector = responses_selector
		if self.responses_selector is None:
			self.responses_selector = select(self.__orm__).filter_by(last_response_execution=None)

	def set_content(self, doc: NotificationSchema):
		result = None

		if all([doc.sub is None, doc.role is None]):
			raise Exception("You must specify at least one option: 'sub' or 'role' in order to add a notification.")

		_update_statement = update(self.__orm__).filter_by(id=doc.id).values(**doc.model_dump())
		_update_result = self.update(_update_statement)
		if _update_result is not None:
			result = self.query({"ref": next(_update_result)})

		return result

	def set_responses_status(self, filter_):
		_result = self.update(update(self.__orm__).where(self.__orm__.ref.in_([str(f) for f in filter_])).values(last_response_execution=current_timestamp()))
		return _result

	def set_response(self, who: str, protocol: str, content: str):

		_result = self.update(update(self.__orm__).filter_by(ref=protocol).values(responser_id=who, response=content, last_response_execution=None))

		return _result

	def is_there_notifications(self):
		return self.count_rows()

	def set_notifications_status(self, filter_):

		_result = update(self.__orm__).where(self.__orm__.ref.in_([f for f in filter_])).values(status=True)

		return _result

	def is_there_responses(self):
		return self.count_rows(self.responses_selector) > 0



