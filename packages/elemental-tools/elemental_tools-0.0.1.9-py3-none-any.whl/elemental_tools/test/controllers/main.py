from elemental_tools.api import TaskController

task_controller = TaskController()

print(list(task_controller.query_not_processed_tasks()))

