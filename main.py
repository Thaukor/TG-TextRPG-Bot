from os import name, stat
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

def create_or_connect() -> sql.Connection:
    con: sql.Connection = None
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

def create_stats(id: int, pj_class: int, cur: sql.Cursor, con: sql.Connection) -> None:
    cur.execute(f'SELECT hp, base_damage, base_armour, resources, resource_regen FROM starter_stats WHERE class_id = {pj_class}')
    stats = cur.fetchone()
    cmd = f"""
    INSERT INTO pjs_stats VALUES
    (
        {id},
        1,
        0,
        {stats[0]},
        {stats[1]},
        {stats[2]},
        {stats[3]},
        {stats[4]}
    )
    """
    cur.execute(cmd)
    con.commit()

    con.close()

def create_warrior(update: Update, context: CallbackContext) -> None:
    context.bot.send_message(chat_id = get_chat_id(update, context), text="Creando guerrero de nombre: " + context.args[0])

    con = create_or_connect()
    cur = con.cursor()

    cur.execute("INSERT INTO pjs (name, class_id, user_id) VALUES (?, 1, ?)", [context.args[0], update.effective_message.from_user.id])
    cur.execute('SELECT last_insert_rowid()')
    con.commit()
    create_stats(cur.fetchone()[0], 1, cur, con)

def create_mage(update: Update, context: CallbackContext) -> None:
    pass

def create_archer(update: Update, context: CallbackContext) -> None:
    pass

def stats(update: Update, context: CallbackContext) -> None:
    con = create_or_connect()
    cur = con.cursor()

    cur.execute(f"SELECT id, name, class_id FROM pjs WHERE user_id = {update.effective_message.from_user.id}")

    pjs = cur.fetchall()
    
    msg = "Tus personajes son\n"
    
    for pj in pjs:
        cur.execute(f"SELECT level FROM pjs_stats WHERE pj_id = {pj[0]}")
        level = cur.fetchone()[0]

        cur.execute(f"SELECT name FROM classes where id = {pj[2]}")
        pj_class = cur.fetchone()[0]
        msg += f" - {pj_class} {pj[1]}, nivel {level}"
    
    context.bot.send_message(chat_id = get_chat_id(update, context), text = msg)

def get_chat_id(update: Update, context: CallbackContext) -> int:
    chat_id = -1

    if update.message is not None:
        chat_id = update.message.chat.id
    elif update.callback_query is not None:
        chat_id = update.callback_query.message.chat.id
    elif update.poll is not None:
        chat_id = context.bot_data[update.poll.id]

    return chat_id

def main():
    pass

create_warrior_handler = CommandHandler('new_warrior', create_warrior)
dispatcher.add_handler(create_warrior_handler)

help_handler = CommandHandler('help', help)
dispatcher.add_handler(help_handler)

stats_handler = CommandHandler('stats', stats)
dispatcher.add_handler(stats_handler)

updater.start_polling()

# Para escuchar por señales, por ejemplo CTRL + C
updater.idle()
