from datetime import datetime

from pymongo.errors import BulkWriteError

from elemental_tools.api.orm.statement import TableStatement
from elemental_tools.db.controller import Controller
from elemental_tools.db import Index, insert, select, update, and_


class StatementController(Controller):
	__orm__ = TableStatement()

	sub = None
	institution_ref = None

	def __init__(self, sub, institution_ref=None):
		super().__init__()
		self.sub = sub
		self.institution_ref = institution_ref

	def save_statement_from_df(self, df):
		_df = df
		self.__logger__('info', f"Saving statement from dataframe: {_df.head()}")
		_df.rename(columns={'Data': 'date', 'Descrição': 'name', 'Valor': 'value'}, inplace=True)

		_df = df.dropna()
		_df = _df.drop_duplicates()

		_df['institution_ref'] = self.institution_ref
		_df['sub'] = self.sub
		_df['type'] = df['value'].apply(lambda x: 'income' if x > 0 else 'outcome' if x < 0 else 'neutral')

		_update_result = False

		_df_dict = _df.to_dict(orient='records')

		try:
			insert(self.__orm__)

			_update_result = self.insert(_df_dict)
			# _update_result = self.insert_many(_df_dict, ordered=False)
		except BulkWriteError as e:
			_df_len = len(_df_dict)
			_n_errors = e.details['nInserted'] - _df_len

			if not e.details['nInserted']:
				self.__logger__('critical', f'No records were inserted!')

			self.__logger__('alert', f'Duplicate Found: {abs(_n_errors)}, Inserted: {e.details["nInserted"]}')

		if _update_result:
			self.__logger__('success', "Statements were saved successfully.")

	def retrieve_statement(self, _type='income', today=None, status=False, time_interval=None):
		self.__logger__('info', "Retrieving Statement...")

		selector = select(self.__orm__).where(and_(self.__orm__.sub == self.sub, self.__orm__.type == _type, self.__orm__.status == status))

		if self.institution_ref is not None:
			selector = select(self.__orm__).where(
				and_(self.__orm__.sub == self.sub, self.__orm__.type == _type, self.__orm__.status == status, self.__orm__.institution_ref == self.institution_ref))

		if today is not None:

			start_of_day = None
			end_of_day = None

			if today:
				# Get today's date
				today_date = datetime.today().date()
				# Calculate the start and end of the day
				start_of_day = f"{today_date}T00:00:00Z"
				end_of_day = f"{today_date}T23:59:59Z"

			elif time_interval is not None and len(time_interval) == 2:
				start_of_day, end_of_day = time_interval

			if start_of_day is not None and end_of_day is not None:
				selector = select(self.__orm__).where(
					and_(
						self.__orm__.sub == self.sub, self.__orm__.type == _type,
						self.__orm__.status == status,
						self.__orm__.institution_ref == self.institution_ref,
						self.__orm__.date > start_of_day,
						self.__orm__.date < end_of_day,
					)
				)

		try:
			self.__logger__("alert", f"Querying selector: {str(selector)}")
			result = self.query_all(selector)

			if result is None:
				self.__logger__("error", f"Could not find statement information for selector: {str(selector)}")

			self.__logger__("success", "Statements were successfully retrieved.")
			return result

		except Exception as e:
			self.__logger__("critical", f"Cannot retrieve statement! Exception: {str(e)}")

	def retrieve_institution_refs(self):

		_pipeline_institution_refs = [
			{
				'$match': {
					"sub": self.sub
				}
			},
			{
				'$group': {
					'ref': '$institution_ref'
				}
			}, {
				'$project': {
					'institution_ref': '$_id',
					'ref': 0
				}
			}
		]

		_result = self.query(select([self.__orm__.institution_ref]).filter(self.__orm__.sub == self.sub).group_by(self.__orm__.institution_ref))

		return list(_result)

