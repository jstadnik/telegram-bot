from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, DictPersistence
import logging
from bot.token import TOKEN
from bot.handlers import setup


per = DictPersistence()
updater = Updater(token=TOKEN, persistence=per, use_context=True)
setup(updater)

