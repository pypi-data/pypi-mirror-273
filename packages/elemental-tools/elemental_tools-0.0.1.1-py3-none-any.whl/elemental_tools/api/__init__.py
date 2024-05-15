from typing import Union

from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.routing import APIRouter
from pydantic import field_validator
from starlette.middleware.cors import CORSMiddleware

from elemental_tools.constants import path_post, path_task_post
from elemental_tools.constants import path_task_get

from elemental_tools.api.controllers.task import TaskController
from elemental_tools.api.controllers.user import UserController

from elemental_tools.api.endpoints import auth as auth_endpoint
from elemental_tools.api.endpoints import group as group_endpoint
from elemental_tools.api.endpoints import institution as institution_endpoint
from elemental_tools.api.endpoints import notification as notification_endpoint
from elemental_tools.api.endpoints import smtp as smtp_endpoint
from elemental_tools.api.endpoints import sons as sons_endpoint
from elemental_tools.api.endpoints import templates as template_endpoint
from elemental_tools.api.endpoints import user as user_endpoint

from elemental_tools.api.schemas.task import TaskSchema

from elemental_tools.asserts import root_ref
from elemental_tools.config import config_initializer
from elemental_tools.db import insert
from elemental_tools.exceptions import Invalid, NotFound, SaveException
from elemental_tools.exceptions import ParameterMissing
from elemental_tools.logger import Logger
from elemental_tools.pydantic import generate_script_information_from_pydantic_models
from elemental_tools.settings import SettingController
from elemental_tools.tools import get_package_name

router = APIRouter()

config = config_initializer()

__logger__ = Logger(app_name=config.app_name, owner=get_package_name(__name__), destination=config.log_path).log


class Api(FastAPI):

    UserController = UserController()
    TaskController = TaskController()

    script_pydantic_models = None
    root_ref = root_ref()

    def __init__(self, endpoints=None, script_pydantic_models: Union[dict, None] = None):
        super().__init__()

        self.settings_db = SettingController()

        self.openapi_tags = [
            {"name": f"""{self.settings_db.company_name.get(root_ref)} - API""", "description": "See the documentation for more information."},
        ]

        self.include_router(auth_endpoint.router)
        self.include_router(user_endpoint.router)
        self.include_router(institution_endpoint.router)
        self.include_router(notification_endpoint.router)
        self.include_router(template_endpoint.router)
        self.include_router(group_endpoint.router)
        self.include_router(smtp_endpoint.router)
        self.include_router(sons_endpoint.router)

        origins = ["*"]
        self.add_middleware(
            CORSMiddleware,
            allow_origins=origins,
            allow_credentials=True,
            allow_methods=["GET", "POST", "OPTIONS", "PATCH", "PUT", "DELETE"],
            allow_headers=["*"],
        )

        if endpoints is not None:
            self.include_router(**user_endpoint.router)

        if script_pydantic_models is not None:

            _user_controller = self.UserController
            _task_controller = self.TaskController

            script_router = APIRouter()
            scripts_information = generate_script_information_from_pydantic_models(script_pydantic_models)

            # Endpoint to schedule tasks
            class TaskRequestSchema(TaskSchema):

                @field_validator("task_name")
                def task_name_validator(cls, name):
                    cls._entrypoint = script_pydantic_models[name]
                    cls.parameters = script_pydantic_models[name]
                    return name

            def instant_run(func, args):

                def execute_function(func, args: dict = None):
                    if args is None:
                        return func()

                    try:
                        result = func(**args)
                    except TypeError:
                        try:
                            result = func(*args.values())
                        except TypeError as e:
                            raise ParameterMissing(str(e))

                    return result

                # try:
                result = execute_function(func, args)
                return result
                # except ParameterMissing as e:
#
                #    raise Invalid("User")HTTPException(detail=str(e), status_code=500)

            @script_router.post(path_task_post, tags=['Scripts/Tasks'])
            def schedule_task(body: TaskRequestSchema, run_test: bool = False):
                response = {"message": "Task processed successfully!"}

                __logger__("info", f"Searching for tasks by name: {body.task_name} in {script_pydantic_models}")

                # Store task data
                if body.task_name in script_pydantic_models.keys():
                    __logger__("info", f"Task {body.task_name} found in dict: {str(script_pydantic_models.keys())}")
                    if body.timer is None or run_test:
                        response["execution_result"] = instant_run(script_pydantic_models[body.task_name]['function'],
                                                                   body.parameters)
                        if not run_test:
                            return JSONResponse(content=str(response), status_code=200)

                    try:
                        _sub = body.sub
                    except:
                        raise Invalid("User")

                    _user = _user_controller.query({"ref": _sub})

                    if _user:
                        stmt = insert(_task_controller.__orm__).values(**body.model_dump())
                        _insert_result = _task_controller.insert(stmt)

                        if _insert_result:
                            return JSONResponse(content={"ref": str(_insert_result)}, status_code=200)
                        else:
                            raise SaveException("Task Schedule")
                    raise NotFound("Sub")
                else:
                    raise NotFound("Task")

            # Endpoint to list available tasks
            @script_router.get(path_task_get, tags=["Scripts/Tasks"])
            def list_tasks():
                return scripts_information

            self.include_router(script_router)

