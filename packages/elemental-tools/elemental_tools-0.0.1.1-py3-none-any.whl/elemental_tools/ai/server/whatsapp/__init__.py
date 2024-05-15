from time import sleep

from elemental_tools.tools import get_package_name
from elemental_tools.asserts import root_ref
from elemental_tools.logger import Logger

from elemental_tools.ai.brainiac import NewRequest
from elemental_tools.ai.brainiac import Brainiac

from elemental_tools.ai.exceptions import Unauthorized, InvalidOption, Error

from elemental_tools.ai.server.basic import Server
from elemental_tools.ai.server.whatsapp.api import WhatsappOfficialAPI

from elemental_tools.api.schemas.user import UserSchema

from elemental_tools.api.controllers.user import UserController
from elemental_tools.api.controllers.notification import NotificationController

from elemental_tools.api.controllers.wpp import WppController

from elemental_tools.config import config_initializer

from elemental_tools.ai.tools import Tools, extract_and_remove_quoted_content



class WhatsappOfficialServer(Server):

	_cache = []
	tools = Tools()

	def __init__(self, brainiac: Brainiac, phone_number_id: str, token_wpp_api: str, timeout: float,
				 bypass_translator: bool = False):

		from elemental_tools.settings import SettingController

		config = config_initializer()
		self.__logger__ = Logger(app_name="ai", owner=get_package_name(__name__), destination=config.log_path).log
		super().__init__(brainiac, bypass_translator)

		if config.webhook_db_url is not None:
			from elemental_tools.api.controllers.webhook import WebhookController
			self.webhook_db = WebhookController()

		self.wpp_db = WppController()
		self.notification_db = NotificationController()
		self.user_db = UserController()
		self.settings_db = SettingController()

		self.timeout = timeout

		self.bypass_translator = bypass_translator

		self.brainiac = brainiac
		self.brainiac.bypass_translator = bypass_translator

		self.__logger__('info', f'Health Checking Wpp Official Server...')

		try:
			self.wpp_api = WhatsappOfficialAPI(phone_number_id, token_wpp_api)
			self.__logger__('success', f'Wpp Official API is up and running!')
		except:
			error_message = f'Unable to connect to Whatsapp official server, check your .env file or compose.\nMake sure to configure WPP_PHONE_NUMBER_ID and the WPP_API_TOKEN env variables.'
			self.__logger__('critical-error', error_message)
			raise Exception(error_message)

		self.__logger__('info', f'Whatsapp phone connected is {self.wpp_api.health.phone_number}')
		self.__logger__('alert', f'Whatsapp code verification status is: {self.wpp_api.health.code_verification_status}')

		self.__logger__('info', f'Checking Webhook Database...')
		new_messages = self.webhook_db.get_unprocessed_wpp_messages()

		self._start()

	def send_message(self, request: NewRequest):
		destination_phone, message = request.cellphone, request.skill.result

		_header = self.settings_db.attendant_default_response_header.get(root_ref())
		if _header is None:
			_header = self.settings_db.company_name.get(root_ref())

		message = f"*{_header}*\n\n{message}"

		self.__logger__('info', f'Sending Message Destination: {str(destination_phone)} Message: {str(message)}')
		self.wpp_api.send_message(destination=destination_phone, message=str(message))
		self.__logger__('success', f"Message has been sent!")

	def _start(self, timeout=5):
		self.__logger__('start', f"Initializing Whatsapp Official Server with Brainiac!")

		while True:
			self.__logger__('info', f"Checking for new messages on your webhook...")
			new_messages = self.webhook_db.get_unprocessed_wpp_messages()
			_gen_list = list(new_messages)
			if len(_gen_list[0]):
				self.__logger__('info', f"New messages found! Processing...")

				for current_index, incoming_message in enumerate(_gen_list):
					for message in incoming_message:
						user_ids = message.get('user_ids', [])
						messages = message.get('messages', [])

						for user_id, current_message in zip(user_ids, messages):
							wpp_user_id = user_id
							not_processed_id = current_message['id']
							incoming_phone = current_message['from']
							message_content = current_message['text']['body']

							_doc = {'msg_id': not_processed_id, 'cellphone': str(incoming_phone), 'wpp_user_id': str(wpp_user_id)}

							if self.wpp_db.add(_doc):
								self.__logger__('info', f'Processing message: id {not_processed_id}, contact {incoming_phone}, message {message_content}')
								user = self.user_db.query(selector={"wpp_user_id": wpp_user_id})

								if user is None:
									user = UserSchema()
									user.language = self.get_lang_from_country_code(incoming_phone)
									user.cellphone = incoming_phone
									user.wpp_user_id = str(wpp_user_id)
									_user_dict = user.model_dump()
									user.id = str(self.user_db.add(_user_dict)['ref'])
								else:
									user["id"] = user["ref"]
									user = UserSchema(**user)

								processable_text = self.translate_input(message=message_content, language=user.language)

								try:
									processable_text, quoted_content = extract_and_remove_quoted_content(processable_text)
								except:
									quoted_content = []

								if user.is_human_attendance:

									try:

										_pipeline_attendant_waiting_for_response = [
											{
												'$match': {"$and": [{"customer_ref": user.ref},
																	{"responser_id": {'$exists': True}}]}
											},
											{
												'$sort': {
													'creation_date': 1
												}
											}
										]

										_agg = self.notification_db.collection.aggregate(_pipeline_attendant_waiting_for_response)

										_current_protocol = next(_agg)

										_current_attendant = self.user_db.query(
											{"ref": _current_protocol['responser_id']})

										_attendant_request = NewRequest(
											message='',
											cellphone=_current_attendant['cellphone'],
											wpp_user_id=wpp_user_id
										)

										_requester_title = incoming_phone

										if user.name is not None:
											_requester_title += f" - {user.name}"

										_attendant_request_content = f"Protocol: \n{str(_current_protocol['ref'])}\n[{_requester_title}] "
										
										_attendant_request_content += f"{message_content}"
										
										_attendant_request.skill.result = _attendant_request_content
										
										self.send_message(_attendant_request)

									except:
										
										self.user_db.update({"ref": user.id}, {"is_human_attendance": False})
										user.is_human_attendance = False

								if not user.is_human_attendance:

									_brainiac_request = NewRequest(
										message=processable_text,
										cellphone=incoming_phone,
										wpp_user_id=wpp_user_id,
										user=user
									)

									_brainiac_request.quoted_content = quoted_content
									_brainiac_request.last_subject = user.last_subject

									try:
										_brainiac_request.skill.result = self.brainiac.process_message(
											_brainiac_request
										)

									except Unauthorized as er:

										print("Raised Unauthorized")

										_brainiac_request.skill.result = str(er)

									except (InvalidOption, Error) as er:

										print("Raised InvalidOption")

										if user.last_subject and user.last_subject is not None:
											processable_text += f"\n{str(user.last_subject)}"

											_brainiac_request = NewRequest(
												message=processable_text,
												cellphone=incoming_phone,
												user=user,
												quoted_content=quoted_content
											)

											_brainiac_request.skill.result = self.brainiac.process_message(
												_brainiac_request
											)

										else:
											_brainiac_request.skill.result = str(er)

									_brainiac_request.skill.result = self.translate_output(_brainiac_request.skill.result, user.language)
									self.send_message(_brainiac_request)

					self.webhook_db.remove(incoming_message[current_index]['ref'])

			else:
				self.__logger__('alert', f"No new messages, skipping...")

			self.verify_notifications()
			sleep(self.timeout)

