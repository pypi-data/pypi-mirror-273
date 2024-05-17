
from elemental_tools.db import select, update, insert
from elemental_tools.api.schemas.user import UserSchema
from elemental_tools.api.schemas.templates import TemplateSchema

from elemental_tools.api.controllers.user import UserController
from elemental_tools.api.controllers.template import TemplateController


class Templates:

    this_template = None
    user_templates = None
    _user = None
    _sub = None

    def __init__(self, sub: str, template_ref: str = None):

        self._template_controller = TemplateController()
        self._user_controller = UserController()

        self._sub = sub

        _this_user = self._user_controller.query(select(self._user_controller.__orm__).filter_by(ref=sub))
        
        if _this_user is not None:
            self._user = UserSchema(**_this_user)
            self.user_templates = self._template_controller.query_all(select(self._template_controller.__orm__).filter_by(sub=sub))
            
            if template_ref is not None:
                self.this_template = self._template_controller.query(select(self._template_controller.__orm__).filter_by(ref=template_ref))
                self.this_template = TemplateSchema(**self.this_template)
                
    def reload_all_templates(self):

        _this_user = self._user_controller.query(select(self._user_controller.__orm__).filter_by(ref=self._sub))

        if _this_user is not None:
            self._user = UserSchema(**_this_user)
            self.user_templates = self._template_controller.query_all(select(self._template_controller.__orm__).filter_by(sub=self._sub))

    def load_variables(self, template_ref: str):

        _this_template = self._template_controller.query(select(self._template_controller.__orm__).filter_by(ref=template_ref, sub=self._user._ref))

        if _this_template is not None:
            _model = TemplateSchema(**_this_template)
            self.variables = _model.variables
            return _model.variables

        return False

    def check(self, modifiers: list, variables: dict):

        if self.this_template is not None:
            if all([mod in self.this_template.modifiers.keys() for mod in modifiers]):
                return self.this_template

        invalid_modifiers = [mod not in self.this_template.modifiers.keys() for mod in modifiers]
        raise Exception(f"Invalid modifier's: {invalid_modifiers}")

    def load(self, modifiers: list, variables: dict):

        _this_template = self.check(modifiers, variables)
        _content = ""

        if _this_template.content is not None:
            _content += _this_template.content

        for modifier in modifiers:
            if modifier in _this_template.modifiers.keys():
                _content += _this_template.modifiers[modifier]

        for variable in variables.keys():
            _replace_ = "$" + "{" + variable + "}"
            _content = _content.replace(_replace_, variables[variable])

        return str(_content)

