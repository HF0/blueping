import logging

import dependency_injector.containers as containers
import dependency_injector.providers as providers

from dummyscanner import DummyScanner
from filepresenceproccesor import FilePresenceProcessor


class Core(containers.DeclarativeContainer):

    config = providers.Configuration('config')

    logger = providers.Singleton(logging.Logger, name='log')

    presence_logger = providers.Singleton(logging.Logger, name='presence_logger')


class Services(containers.DeclarativeContainer):

    identity_scanner = providers.Singleton(DummyScanner, logger=Core.logger)

    presence_processor = providers.Singleton(FilePresenceProcessor, logger=Core.logger,
                                           presence_logger=Core.presence_logger,
                                           target=Core.config.target,
                                           max_disconnect_pings=Core.config.max_disconnect_pings)


