from telegram import Update
from telegram.ext import ContextTypes
from loguru import logger
import dotenv, os
from telegram.error import BadRequest

dotenv.load_dotenv()

DB_CHOICE = os.getenv("DB_CHOICE") == "pocketbase"
if DB_CHOICE:
    from app.pb import init_commands_and_snippets, get_all_chats, create_group_chat_id, remove_group_chat_id, get_snippet_by_name
else:
    from app.fakepb import init_commands_and_snippets, get_all_chats, create_group_chat_id, remove_group_chat_id, get_snippet_by_name

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    from app.bot import commands
    logger.debug(f"Вызвана команда /start от пользователя с ID: {update.effective_user.id}")
    await update.message.reply_text(
        commands.get("start", "default start message"),
        parse_mode='Markdown'
    )
    
async def add_chat_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    from app.bot import commands
    logger.debug(f"Добавление чата с ID: {update.effective_chat.id}")
    create_group_chat_id(update.effective_chat.id)
    await update.message.reply_text(
        commands.get("add_chat", "default add chat message"),
        parse_mode='Markdown'
    )
    
async def remove_chat_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    from app.bot import commands
    logger.debug(f"Удаление чата с ID: {update.effective_chat.id}")
    remove_group_chat_id(update.effective_chat.id)
    await update.message.reply_text(
        commands.get("remove_chat", "default remove chat message"),
        parse_mode='Markdown'
    )
    
async def snippet_response_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.debug("Обработка сниппета")
    snippet_text = get_snippet_by_name(update.message.text.split()[0][1:])
    await update.message.reply_text(
        snippet_text,
        parse_mode='Markdown'
    )

async def all_guides_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    from app.bot import commands
    logger.debug("Запрос всех руководств")
    __commands, snippets = init_commands_and_snippets()
    await update.message.reply_text(
        commands.get("all_guides", "default all guides message") + "\n" + "\n".join([f"/{key}" for key, value in snippets.items()]),
        parse_mode='Markdown'
    )
    
async def send_news_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.debug("Отправка новостей во все чаты")
    # Проверяем, есть ли текст сообщения
    if len(update.message.text.split(" ", 1)) < 2:
        await update.message.reply_text("Ошибка: сообщение пустое. Пожалуйста, введите текст новости.")
        return
    
    message = update.message.text.split(" ", 1)[1]
    chat_ids = get_all_chats()
    
    for chat_id in chat_ids:
        try:
            await context.bot.send_message(chat_id=chat_id, text=message, parse_mode='Markdown')
        except BadRequest as e:
            if str(e) == "Chat not found":
                logger.warning(f"Чат с ID {chat_id} не найден. Удаляем из PocketBase.")
                remove_group_chat_id(chat_id)
    
    from app.bot import commands
    await update.message.reply_text(
        commands.get("send_news", "default send news message"),
        parse_mode='Markdown'
    )