from datetime import datetime
from typing import Union, List

from elemental_tools.pydantic import BaseModel, Field, PrivateAttr, field_validator, UserRoles
from elemental_tools.api.controllers.template import TemplateController
from elemental_tools.db import select

template_controller = TemplateController()


class NotificationSchema(BaseModel, extra='allow'):
	role: Union[List[UserRoles], None] = Field(description='List of roles to notify. Check your admin to obtain more information about that.', default=None)
	status: Union[bool, None] = Field(description='Notification Status', default=False)
	status_email: Union[bool, None] = Field(description='Email Notification Status', default=False)
	smtp_ref: Union[str, None] = Field(description='The SMTP Configuration that notification must use to be sent.', default=None)
	status_wpp: Union[bool, None] = Field(description='Whatsapp Notification Status', default=False)
	content: Union[str, None] = Field(description='Notification Text or HTML Content', default=None)
	template_ref: Union[str, None] = Field(description='Template Id', default=None)
	customer_ref: Union[str, None] = Field(description='User or Users who the Notification is send', default=None)
	sub: Union[str, None] = Field(description='User who creates the Notification', default=None)
	modifiers: Union[list, None] = Field(description='Template Modifiers to be used in conjunction with the content (Will be placed content > modifiers)', default=None)
	variables: Union[dict, None] = Field(description="Here you can pass the variables that must be parsed to the template. To use a variable on a template you must enclouser the variable with ${}\nExample: 'This is a sample template for ${name}'.\n\nIn order to place a name inside this template you might use the example on this doc.", default=None, examples=[{"name": "John Doe"}])
	last_response_execution: Union[str, None] = None

	@classmethod
	@field_validator('template_ref')
	def valid_template(cls, template_ref):
		_this_template = template_controller.query(select(template_controller.__orm__).filter_by(ref=template_ref))
		if _this_template is not None:
			return template_ref

