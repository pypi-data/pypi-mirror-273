from elemental_tools.api.orm.device import TableDevice
from elemental_tools.db.controller import Controller


class DeviceController(Controller):
	__orm__ = TableDevice


