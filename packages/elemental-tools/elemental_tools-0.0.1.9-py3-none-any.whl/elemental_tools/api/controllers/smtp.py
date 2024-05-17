from elemental_tools.api.controllers.user import UserController
from elemental_tools.api.orm.smtp import TableSMTP
from elemental_tools.api.schemas.smtp import SMTPSchema
from elemental_tools.api.schemas.user import UserSchema
from elemental_tools.db.controller import Controller, select


user_controller = UserController()


class SMTPController(Controller):
	__orm__ = TableSMTP

	def retrieve_all_smtp_config_list(self, _user, sub, supress_sensitive_data: bool = True):
		all_owners_to_search = [_user._ref]

		_user_companies = user_controller.query_all(select(user_controller.__orm__).filter(
			user_controller.__orm__.ref.in_([company.company_ref for company in _user.companies if company.role in ['editor', 'owner']])
		))

		if _user_companies is not None:
			for company in _user_companies:
				_this_company = UserSchema(**company)
				all_owners_to_search.append(_this_company.ref)

		if sub is None:
			query = select(self.__orm__).filter(
				self.__orm__.sub.in_(all_owners_to_search)
			)
		else:
			query = select(self.__orm__).filter_by(sub=sub)

		all_user_smtp = self.query_all(query)

		for smtp in all_user_smtp:
			_current_smtp = SMTPSchema(**smtp)

			if not supress_sensitive_data:
				yield _current_smtp.model_dump()
			else:
				yield {"sub": _current_smtp.sub, "email": _current_smtp.email, "ref": _current_smtp.ref}



