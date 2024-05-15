from elemental_tools.api.orm.user import TableUser
from elemental_tools.db import select, update
from elemental_tools.db.controller import Controller


class UserController(Controller):
    __orm__ = TableUser

    def set_last_subject(self, sub, subject):
        return self.update(update(self.__orm__).filter_by(ref=sub).values(last_subject=subject))

    def set_next_skill(self, sub, subject):
        return self.update(update(self.__orm__).filter_by(ref=sub).values(next_skill=subject))

    def get_next_skill(self, sub):

        _result = False

        try:
            _result = self.query(select(self.__orm__).filter_by(ref=sub))['next_skill']
        except KeyError:
            _result = None

        return _result

    def get_last_subject(self, sub):

        _result = False

        try:
            _result = self.query(select(self.__orm__).filter_by(ref=sub))['last_subject']
        except KeyError:
            _result = None

        return _result

    def remove_last_subject(self, sub):
        return self.update(update(self.__orm__).filter_by(ref=sub).values(last_subject=None))

