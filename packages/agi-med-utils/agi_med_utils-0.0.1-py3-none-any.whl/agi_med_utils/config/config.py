import yaml
import codecs
from .singleton import singleton


@singleton
class ConfigSingleton:
    def __init__(self, common_config_dir, branch_config_dir):
        with codecs.open(f'{common_config_dir}/config.yaml', encoding='utf-8') as file:
            common = yaml.load(file, yaml.Loader)
        with codecs.open(f'{branch_config_dir}/config.yaml', encoding='utf-8') as file:
            branch = yaml.load(file, yaml.Loader)
        self.config = {**common, **branch}

    def get(self):
        return self.config
