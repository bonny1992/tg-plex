import pyombi
import requests
import json

from utils import set_logger

logger = set_logger('ombi')

def get_all_users(config):
    headers = {
        'accept': 'application/json',
        'apiKey': config.ombi_token
        }

    url = 'http%s://%s:%s%sapi/v1/Identity/Users' % (
        's' if config.ombi_ssl else '',
        config.ombi_host,
        config.ombi_port,
        config.ombi_path
    )

    r = requests.get(url, headers)
    return r.json()


def check_if_user_is_in_ombi(config, username):
    users = get_all_users(config)
    for user in users:
        if username == user['userName']:
            logger.debug('Utente %s trovato!', user['userName'])
            return True
    logger.debug('Utente %s NON trovato :(', username)
    return False