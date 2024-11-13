from loguru import logger
import dotenv, os

dotenv.load_dotenv()

import json

logger.warning("Используется fakepb!")

# Загрузка данных из JSON файла
def load_data(filename: str):
    with open(filename, 'r', encoding='utf-8') as file:
        return json.load(file)

def init_commands_and_snippets() -> tuple[dict, dict]:
    logger.debug(f"Получение полного списка сниппетов из файла: data.json")
    data = load_data('data/data.json')
    
    commands = {item['name']: item['snippet_text'] for item in data['tgbot_snippets'] if item['is_command']}
    snippets = {item['name']: item['snippet_text'] for item in data['tgbot_snippets'] if not item['is_command']}
    
    logger.debug(f"Команды и сниппеты инициализированы: {commands}")
    return commands, snippets

def get_all_chats() -> list[str]:
    logger.debug(f"Получение всех чатов из файла: data.json")
    data = load_data('data/data.json')
    chat_ids = [item['group_id'] for item in data['tgbot_chats']]
    logger.debug(f"Полученные ID чатов: {chat_ids}")
    return chat_ids

def create_group_chat_id(chat_id: str):
    logger.debug(f"Создание группы чата с ID: {chat_id}")
    data = load_data('data/data.json')
    data['tgbot_chats'].append({"group_id": chat_id})
    save_data('data/data.json', data)  # Сохранение изменений в файл

def remove_group_chat_id(chat_id: str):
    logger.debug(f"Удаление группы чата с ID: {chat_id}")
    data = load_data('data/data.json')
    data['tgbot_chats'] = [item for item in data['tgbot_chats'] if item['group_id'] != chat_id]
    save_data('data/data.json', data)  # Сохранение изменений в файл

def create_log(chat_id: str, logs: dict):
    logger.debug(f"Создание лога для чата с ID: {chat_id}")
    data = load_data('data/data.json')
    data['tgbot_logs'].append({"group_id": chat_id, "logs": logs})
    save_data('data/data.json', data)  # Сохранение изменений в файл

def get_snippet_by_name(name: str) -> str:
    logger.debug(f"Получение сниппета с названием: {name}")
    data = load_data('data/data.json')
    snippet = next((item['snippet_text'] for item in data['tgbot_snippets'] if item['name'] == name), "Сниппет не найден")
    return snippet

def save_data(filename: str, data):
    with open(filename, 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)
