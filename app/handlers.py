from telegram import Update
from telegram.ext import ContextTypes
from loguru import logger
import dotenv, os
from telegram.error import BadRequest

dotenv.load_dotenv()

DB_CHOICE = os.getenv("DB_CHOICE")
if DB_CHOICE == "pocketbase":
    from app.pb import init_commands_and_snippets, get_all_chats, create_group_chat_id, remove_group_chat_id, create_log, get_snippet_by_name
elif DB_CHOICE == "sqlite":
    from app.sqlitedb import init_commands_and_snippets, get_all_chats, create_group_chat_id, remove_group_chat_id, create_log, get_snippet_by_name
elif DB_CHOICE == "jsondb":
    from app.jsondb import init_commands_and_snippets, get_all_chats, create_group_chat_id, remove_group_chat_id, create_log, get_snippet_by_name
else:
    logger.error(f"Неизвестный тип базы данных: {DB_CHOICE}")
    raise ValueError(f"Неизвестный тип базы данных: {DB_CHOICE}")

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    from app.bot import commands
    logger.debug(f"Вызвана команда /start от пользователя с ID: {update.effective_user.id}")
    await update.message.reply_text(
        commands.get("start", "default start message"),
        parse_mode='MarkdownV2'
    )
    
async def add_chat_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    from app.bot import commands
    logger.debug(f"Добавление чата с ID: {update.effective_chat.id}")
    create_group_chat_id(update.effective_chat.id)
    await update.message.reply_text(
        commands.get("add_chat", "default add chat message"),
        parse_mode='MarkdownV2'
    )
    
async def remove_chat_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    from app.bot import commands
    logger.debug(f"Удаление чата с ID: {update.effective_chat.id}")
    remove_group_chat_id(update.effective_chat.id)
    await update.message.reply_text(
        commands.get("remove_chat", "default remove chat message"),
        parse_mode='MarkdownV2'
    )
    
async def snippet_response_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.debug("Обработка сниппета")
    snippet_text = get_snippet_by_name(update.message.text.split()[0][1:])
    await update.message.reply_text(
        snippet_text,
        parse_mode='MarkdownV2'
    )
    
def escape_markdown(text: str) -> str:
    """Экранирует специальные символы Markdown V2"""
    SPECIAL_CHARS = ['_', '*', '[', ']', '(', ')', '~', '`', '>', '#', '+', '-', '=', '|', '{', '}', '.', '!']
    for char in SPECIAL_CHARS:
        text = text.replace(char, f'\\{char}')
    return text

async def all_guides_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    from app.bot import commands
    logger.debug("Запрос всех руководств")
    __commands, snippets = init_commands_and_snippets()
    
    # Экранируем специальные символы в списке команд и в тексте сообщения
    escaped_commands = [f"\\/{escape_markdown(key)}" for key, value in snippets.items()]
    guides_text = commands.get("all_guides", "default all guides message")
    
    await update.message.reply_text(
        guides_text + "\n" + "\n".join(escaped_commands),
        parse_mode='MarkdownV2'
    )
    
async def send_news_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_ids = get_all_chats()
    await do_news_to_one_or_many(chat_ids, update, context)

async def presend_news_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_ids = [update.effective_chat.id]
    await do_news_to_one_or_many(chat_ids, update, context)

async def do_news_to_one_or_many(chat_ids: list, update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.debug("Отправка новостей во все чаты")
    # Проверяем, есть ли текст сообщения
    if len(update.message.text.split(" ", 1)) < 2:
        await update.message.reply_text("Ошибка: сообщение пустое. Пожалуйста, введите текст новости.")
        return
    
    message = update.message.text.split(" ", 1)[1]
    
    for chat_id in chat_ids:
        try:
            await context.bot.send_message(chat_id=chat_id, text=message, parse_mode='MarkdownV2')
        except BadRequest as e:
            if str(e) == "Chat not found":
                logger.warning(f"Чат с ID {chat_id} не найден. Удаляем из PocketBase.")
                remove_group_chat_id(chat_id)
    
    from app.bot import commands
    await update.message.reply_text(
        commands.get("send_news", "default send news message"),
        parse_mode='MarkdownV2'
    )