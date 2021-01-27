from config import Config
from utils import set_logger

from peewee import SqliteDatabase
import database as db

from telegram.ext import Updater
from telegram.ext import CommandHandler, CallbackQueryHandler

from commands import *

config = Config()
logger = set_logger('bot', config.logging_level)

logger.debug('Configurazione caricata')

logger.debug('Imposto il db')

database = SqliteDatabase('bot.db')
db.proxy.initialize(database)
database.connect()
database.create_tables([db.User])

config.db = database

logger.info('Avviato il programma!')

logger.debug('Creo l\'updater per il bot')
updater = Updater(token=config.telegram_bot_token)

dispatcher = updater.dispatcher

logger.debug('Aggiungo i comandi')
handlers = [] 
handlers.append(CommandHandler('start', start))
handlers.append(CallbackQueryHandler(login_button))

for handler in handlers:
    dispatcher.add_handler(handler)

logger.debug('Inizio il polling')

try:
    updater.start_polling()
    updater.idle()
except KeyboardInterrupt:
    logger.info('Termino il programma')

    
