import yaml
import os.path


class UserConfig:

    def __init__(self, configFile = "~/.tradingbot.yaml"):
        fullPath = os.path.expanduser(configFile)

        with open(fullPath) as f:
            c = yaml.load(f, Loader=yaml.FullLoader)
            for key in c:
                setattr(self, key, c[key])