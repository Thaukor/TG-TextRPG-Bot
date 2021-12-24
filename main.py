from os import name
import sqlite3 as sql
from sqlite3 import Error
import telegram
import telegram.ext
from telegram.ext import Updater, CallbackContext, CommandHandler, CallbackQueryHandler, ConversationHandler, Filters, JobQueue
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup

db = "world.db"
updater = None
with open('token', 'r') as token:
    updater = Updater(token=token.read(), use_context=True)
dispatcher = updater.dispatcher

def create_or_connect():
    con = None
    try:
        con = sql.connect(db)
        print("Connection successful")
    except Error as e:
        print(e)
    finally:
        return con

def start(update: Update, context: CallbackContext):
    context.bot.send_message(
        chat_id=update.effective_chat.id, text="I'm a bot, please talk to me!")

help_text = """Lista de comandos
/help: Muestra esta pantalla
/new_warrior name: Crea un personaje nuevo, con el nombre escrito en name. Ej: /create_warrior Williams
/dung: Inicia una nueva mazmorra
/stats: Muestra estadísticas de tus personajes"""

def help(update: Update, context: CallbackContext):
    context.bot.send_message(
        chat_id=update.effective_chat.id, text=help_text
    )


def create_warrior(update: Update, context: CallbackContext):
    pass

def get_chat_id(update: Update, context: CallbackContext):
    chat_id = -1

    if update.message is not None:
        chat_id = update.message.chat.id
    elif update.callback_query is not None:
        chat_id = update.callback_query.message.chat.id
    elif update.poll is not None:
        chat_id = context.bot_data[update.poll.id]

    return chat_id

def main():
    create_or_connect()

if __name__ == "__main__":
    create_or_connect()

create_warrior_handler = CommandHandler('create_warrior', create_warrior)
dispatcher.add_handler(create_warrior_handler)

help_handler = CommandHandler('help', help)
dispatcher.add_handler(help_handler)

updater.start_polling()

# Para escuchar por señales, por ejemplo CTRL + C
updater.idle()
