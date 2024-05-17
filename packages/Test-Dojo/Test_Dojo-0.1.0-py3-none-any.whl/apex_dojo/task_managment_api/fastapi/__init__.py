from dataclasses import dataclass

from fastapi import FastAPI

from apex_dojo.task_managment_api.fastapi.api import api


@dataclass
class FastApiConfig:
    def setup(self) -> FastAPI:
        app = FastAPI()
        app.include_router(api, prefix="/tasks")

        return app
