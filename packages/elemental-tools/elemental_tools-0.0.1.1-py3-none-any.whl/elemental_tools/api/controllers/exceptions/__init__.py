from elemental_tools.api.controllers.task import TaskController


task_controller = TaskController()


class TaskTimeoutException(Exception):

    def __init__(self, _id):
        print(f'Task Timeout Exceeded, Blocking Next Execution for Task ID: {_id}')
        task_controller.set_status(_id, False)


