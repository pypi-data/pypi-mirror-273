#  Copyright (c) 2024. Aron Barocsi | All rights reserved.

import asyncio

from pydantic import Field, field_validator

from xposer.api.base.base_fastapi_service import BaseFastApiService
from xposer.api.base.base_fastapi_service_config_model import BaseFastApiRouterConfigModel
from xposer.api.base.xpcontroller_base_class import XPControllerBaseClass
from xposer.core.configure import Configurator
from xposer.core.context import Context
from xposer.sample_app.http_post_uvicorn_fastapi.routers.sample_app_http_service import SampleAppHTTPService


class SampleAppHttpControllerConfigModel(BaseFastApiRouterConfigModel):
    foo_param: str = Field(default='foo')
    uvicorn_host: str = Field(default='localhost')
    uvicorn_port: int = Field(default=8000)

    @field_validator("uvicorn_port")
    def convert_to_int(cls, value):
        return int(value)


class SampleAppHttpXPController(XPControllerBaseClass):
    config_prefix: str = "xpcontroller_"  # Class level

    def __init__(self, ctx: Context):
        super().__init__(ctx)
        self.api_prefix: str = "/api"
        self.uvicorn_server = None
        self.http_router: BaseFastApiService = None
        self.config: SampleAppHttpControllerConfigModel = self.config  # Type hint

    def mergeConfigurationFromPrefix(self) -> SampleAppHttpControllerConfigModel:
        return Configurator.mergeAttributesWithPrefix(
            SampleAppHttpControllerConfigModel,
            self.ctx.config,
            self.config_prefix,
            validate=True,
            strict=True
            )

    async def start_fastapi_service(self, callback):
        try:
            self.uvicorn_server = await self.http_router.startService(
                self.config.uvicorn_host,
                self.config.uvicorn_port,
                [SampleAppHTTPService.getRoute(self.ctx)],
                api_prefix=self.api_prefix,
                callback=callback,
                )
        except Exception as e:
            # Log the exception for debugging
            self.ctx.logger.exception(f"Error starting FastApi service: {e}")
            # Notify the future object about the failure
            raise

    async def tearDownXPController(self):
        self.ctx.logger.info("tearDownXPController called")
        if self.uvicorn_server:
            self.uvicorn_server.should_exit = True
        await asyncio.sleep(1)

    def handle_timeout_exception(self, task):
        try:
            task.result()
        except asyncio.TimeoutError:
            raise ValueError("The FastAPI service did not start within 10 seconds!")

    async def startXPController(self):
        # raise CompletedException(self.__class__.__name__)
        self.http_router = BaseFastApiService(self.ctx)
        future = asyncio.Future()
        fastapi_service_task = asyncio.create_task(self.start_fastapi_service(callback=future.set_result))
        fastapi_service_task.set_name("SampleAppHttpController:StartFastApiServiceTask")
        timeout_task = asyncio.create_task(asyncio.wait_for(future, timeout=10))
        timeout_task.set_name("SampleAppHttpXPController::FastApiServiceTimeoutTask")
        timeout_task.add_done_callback(self.handle_timeout_exception)
        await future
        self.ctx.logger.debug("Started")
