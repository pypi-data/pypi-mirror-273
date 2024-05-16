from typing import Any

from xposer.api.base.base_kafka_service import BaseKafkaService
from xposer.core.abstract_xpcontroller import AbstractFacade
from xposer.core.configure import Configurator
from xposer.core.context import Context
from xposer.api.base.base_kafka_service_config_model import BaseKafkaServiceConfigModel


class FacadeBaseClass(AbstractFacade):
    name: str
    config: BaseKafkaServiceConfigModel | Any
    config_prefix: str
    kafka_router: BaseKafkaService
    socket_router: BaseKafkaService
    http_router: BaseKafkaService

    def __init__(self, ctx: Context):
        super().__init__(ctx)
        self.name = "FacadeBaseClass"
        self.config = None
        self.config_prefix = ''
        self.kafka_router = None
        self.socket_router = None
        self.http_router = None
        self.mergeConfigurationFromPrefix()
        self.initializeRouters()

    def constructConfigModel(self) -> BaseKafkaServiceConfigModel:
        return self.config.model_construct(_validate=False)

    def mergeConfigurationFromPrefix(self):
        worker_config_defaults = self.constructConfigModel()
        # Merge default parameters from global config
        worker_config_merged = Configurator.mergePrefixedAttributes(worker_config_defaults,
                                                                    self.ctx.config,
                                                                    '')
        # Merge facade specific configuration parameters
        worker_config_prefix_merged = Configurator.mergePrefixedAttributes(worker_config_merged,
                                                                           self.ctx.config,
                                                                           self.config_prefix,
                                                                           allow_extra=True)
        worker_config_prefix_merged.model_validate(worker_config_prefix_merged)
        self.config = worker_config_prefix_merged

    """Built-in kafka router"""

    def kafkaRouterInboundHandler(self, data):
        raise NotImplementedError

    def initializeKafkaRouter(self, handlerFunc, start_immediately: bool = True):
        # Initialize workers
        consumer_config = {
            'bootstrap.servers': self.config.router_kafka_server_string,
            'group.id': self.config.router_kafka_group_id
        }
        producer_config = {
            'bootstrap.servers': self.config.router_kafka_server_string
        }
        router = BaseKafkaService(consumer_config,
                                  producer_config,
                                 'input_topic',
                                 'output_topic',
                                 'exception_topic',
                                  handlerFunc)
        self.kafka_router = router
        if start_immediately:
            self.kafka_router.start()
        return router

    def initializeRouters(self):
        raise NotImplementedError

    def start(self):
        raise NotImplementedError
