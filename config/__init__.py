import sys
import yaml

from utils import set_logger

class Config:

    def __str__(self):
        return str(self.__class__) + ": " + str(self.__dict__)

    _default_config = {
        'telegram_bot_token'    : None,
        'telegram_bot_admins'   : ['1234567890', '0987654321'],
        'plex_app_name'         : 'My awesome Plex app',
        'webhook_url'           : 'https://',
        'ombi_ssl'              : True,
        'ombi_host'             : None,
        'ombi_port'             : 443,
        'ombi_path'             : '/',
        'ombi_user'             : '',
        'ombi_token'            : '',
        'debug'                 : False
    }

    def __init__(self):
        config = {}
        try:
            with open('config.yaml', 'r') as configfile:
                config = yaml.load(configfile, Loader=yaml.FullLoader)
                logger = set_logger('config', 'INFO' if not config['debug'] else 'DEBUG')
                if not config.keys() == self._default_config.keys():
                    raise FileNotFoundError('Configurazione non valida!')
                for key, val in config.items():
                    setattr(self, key, config[key])
                    logger.debug('%s: %s', key, config[key])
        except (FileNotFoundError, AttributeError):
            with open('config.yaml', 'w') as configfile:
                yaml.dump(self._default_config, configfile)
            sys.exit('Configurazione di default salvata.')
        except KeyError:
            _updated_default_config = self._default_config
            for index, key in config.items():
                _updated_default_config[key] = config[key]
            with open('config.yaml', 'w') as configfile:
                yaml.dump(_updated_default_config, configfile)
            sys.exit('Configurazione di default salvata ed aggiornata.')

        if self.telegram_bot_token is None:
            sys.exit('Serve un token per Telegram. Ottienilo da @BotFather!')

        if self.webhook_url == '' or self.webhook_url == 'https://':
            self.use_webhooks = False
        else:
            self.use_webhooks = True

        if self.debug:
            self.logging_level = 'DEBUG'
        else:
            self.logging_level = 'INFO'

        self.db = None