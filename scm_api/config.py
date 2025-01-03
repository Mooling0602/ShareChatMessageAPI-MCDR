from mcdreforged.api.all import *


default_config = {
    "enable": {
        "test": False,
        "listen_only": False
    }
}

def load_config(server: PluginServerInterface):
    server.logger.info("For developers, please enable test option in config.enable_test, then you can debug.")
    config = server.load_config_simple('config', default_config)
    return config
