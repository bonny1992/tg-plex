from telegram import InlineKeyboardButton, InlineKeyboardMarkup

from time import sleep

from config import Config
from utils import set_logger, get_random_string
import database as db
from ombi import check_if_user_is_in_ombi

import requests

from furl import furl

config = Config()
logger = set_logger('commands', config.logging_level)

def start(update, context):
    user = db.get_user_by_chat_id(chat_id=update.effective_chat.id)
    if user is None:
        username = update.message.from_user.first_name
        client_id = get_random_string(32)

        logger.debug('Ottengo il pin...')

        headers = {'accept': 'application/json'}
        data = {
            'strong': True,
            'X-Plex-Product': config.plex_app_name,
            'X-Plex-Client-Identifier': client_id
        }
        
        r = requests.post('https://plex.tv/api/v2/pins', headers=headers, data=data)
        reply_json = r.json()
        logger.debug(reply_json)

        auth_id     = reply_json['id']
        auth_code   = reply_json['code']

        f = furl('https://app.plex.tv/auth')
        f.args['clientID'] = client_id
        f.args['code'] = auth_code
        f.args['context[device][product]'] = config.plex_app_name

        plex_url = f.url

        plex_url = plex_url[:24] + "#" + plex_url[24:]

        message = '''
Benvenuto %s.
Visto che è la tua prima volta con me, c'è bisogno che tu acceda a Plex.
Per favore, segui i passi qua sotto:
''' % (username)

        keyboard = [
            [ InlineKeyboardButton('1) Apri Plex.tv ed effettua il login', url=plex_url) ],
            [ InlineKeyboardButton('2) Verifica il login', callback_data='login_with_plex') ]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        logger.debug(reply_markup)

        context.user_data['user'] = {
            'username': username,
            'chat_id': update.message.from_user.id,
            'client_id': client_id,
            'auth_id': auth_id,
            'auth_code': auth_code,
            'handler': update.message.from_user.username,
        }

        context.bot.send_message(chat_id=update.effective_chat.id, text=message, reply_markup=reply_markup).message_id

    else:
        context.bot.send_message(chat_id=update.effective_chat.id, text="Bentornato/a, %s, per favore utilizza il comando /menu" % user.username)


def login_button(update, context):

    query = update.callback_query

    logger.info(query)

    check_url = 'https://plex.tv/api/v2/pins/%s' % context.user_data['user']['auth_id']
    headers = {'accept': 'application/json'}
    params = {
                'code': context.user_data['user']['auth_code'],
                'X-Plex-Client-Identifier': context.user_data['user']['client_id']
    }

    logger.debug(check_url)
    logger.debug(params)

    message = '''Perfetto, controllando l\'esito dell\'autenticazione sui server di Plex...\n(Massimo 2 minuti)'''
    query.answer()
    query.edit_message_text(text=message)

    i = 0

    auth_token = ''

    while i < 120:
        r = requests.get(
            check_url,
            headers=headers,
            params=params
        )
        reply = r.json()
        logger.debug(reply)
        try:
            auth_token = reply['authToken']
            if auth_token == None or auth_token == '':
                raise KeyError
            break
        except KeyError:
            i = i + 1
            logger.debug(auth_token)
            sleep(1)
    
    if i >= 120:
        message = '''Autenticazione fallita!\nPrego riutilizzare il comando /start!'''
        query.edit_message_text(text=message)
        return

    users_url = 'https://plex.tv/api/v2/user'
    params = {
        'X-Plex-Token': auth_token
    }
    r = requests.get(users_url, headers=headers, params=params)
    logger.debug(params)

    plex_username = r.json()['username']

    message = '''Autenticazione con Plex eseguita!\nOra controllo il database di Ombi...'''
    query.edit_message_text(text=message)

    if not check_if_user_is_in_ombi(config, plex_username):
        message = '''Autenticazione fallita!\nÈ possibile che tu non sia abilitato/a a questo server?'''
        query.edit_message_text(text=message)
        return
    else:
        db.User(
            username=context.user_data['user']['username'],
            chat_id=context.user_data['user']['chat_id'],
            client_id=context.user_data['user']['client_id'],
            handler=context.user_data['user']['handler'],
            auth_token=auth_token,
            plex_username = plex_username
        ).save()
        message = '''Benvenuto/a %s, per favore utilizza il comando /menu per cominciare!''' % (context.user_data['user']['username'])
        query.edit_message_text(text=message)



