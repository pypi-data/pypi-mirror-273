from datetime import datetime

from dateutil.relativedelta import relativedelta

from elemental_tools.api.orm.transaction import TableTransaction
from elemental_tools.api.schemas.transaction import TransactionSchema
from elemental_tools.asserts import root_ref
from elemental_tools.db import update, delete, select, and_, func
from elemental_tools.db.controller import Controller
from elemental_tools.settings import SettingController
from elemental_tools.system import current_timestamp


def get_cooldown():
	settings = SettingController()

	return str(settings.transaction_cooldown.get(sub=root_ref(), default=5))


class TransactionController(Controller):
	__orm__ = TableTransaction

	def _remove_old_transactions(self, transaction: TransactionSchema):
		_user_old_transactions = self.query_all(select(self.__orm__).filter(and_(
			self.__orm__.sub == transaction.sub,
			not self.__orm__.status, not self.__orm__.processed, not self.__orm__.exported,
		)))

		_user_old_transactions = list(_user_old_transactions)
		to_remove_list = []

		if len(_user_old_transactions):
			for old_transaction in _user_old_transactions:
				to_remove_list += old_transaction["ref"]

			self.__logger__("info", f"Removing Old Pending Transactions...")
			self.delete(delete(self.__orm__).filter(self.__orm__.ref.in_(to_remove_list)))
			self.__logger__("success", f"Old Pending Transactions Removed!")
			return True

		self.__logger__("alert", f"Remove old transaction skipping, since no old transactions were found.")

	def close_transaction(self, transaction: TransactionSchema):
		fail_msg = "No Transaction Found!"
		_cooldown_date = datetime.now() - relativedelta(minutes=int(get_cooldown()))

		open_transactions_selector = select(self.__orm__).add_columns(
			transaction_type="open"
		).filter(
			self.__orm__.sub == transaction.sub,
			self.__orm__.status == False,
			self.__orm__.creation_date <= _cooldown_date
		).order_by(
			self.__orm__.creation_date.asc()
		)

		try:
			_current_transaction = self.query(open_transactions_selector)
			self.__logger__("info", f"user transaction: {_current_transaction}")

			if _current_transaction is not None:
				_now = current_timestamp()
				_result = self.update(update(self.__orm__).filter_by(ref=_current_transaction["ref"]).values(status=True, confirmation_date=func.now()))

				if _result:
					self.__logger__("success", f"Transaction Closed: {_current_transaction}")
					return _current_transaction

		except Exception as e:
			fail_msg = f'Cannot get transaction because of exception: {e}'

		self.__logger__("alert", fail_msg)
		return False

	def get_to_export_transactions(self, sub):
		fail_msg = "No Such Transaction To Export."

		try:
			to_export_transactions_selector = select(self.__orm__).filter(
				and_(
					self.__orm__.sub == sub,
					self.__orm__.exported == False,
					self.__orm__.status == True
				)
			)
			self.__logger__("info", f"Querying User Transactions Pending of Exportation...")
			_current_transaction_list = self.query_all(to_export_transactions_selector)
			yield _current_transaction_list

		except Exception as e:
			fail_msg = f"Cannot get transaction because of exception: {e}"

		self.__logger__("alert", fail_msg)
		return False

	def set_exportation_status(self, transaction_ids: list):

		self.__logger__("info", f"Setting Exportation Status To: {str(transaction_ids)}")
		_result = self.update(update(self.__orm__).filter(self.__orm__.ref.in_(transaction_ids)).values(exported=True))

		if _result:
			self.__logger__("success", f"Transaction Exportation Status Set!")
			return True

		self.__logger__("alert", f"No Transaction Found!")

