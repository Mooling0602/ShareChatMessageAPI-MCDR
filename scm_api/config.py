from mcdreforged.api.all import *


default_config = {"enable_test": False}

config = None

def load_config(server: PluginServerInterface):
    global config
    server.logger.info("For developers, please enable test option in config.enable_test, then you can debug.")
    config = server.load_config_simple('config', default_config)
