# ТГ бот для рассылки сообщений и с функционалом сниппетов

## Описание
Этот проект представляет собой Telegram-бота, который позволяет отправлять сообщения в чаты и управлять сниппетами. Бот поддерживает команды для добавления и удаления чатов, а также отправки новостей и получения сниппетов.

## Установка

1. Клонируйте репозиторий:
   ```bash
   git clone <URL_репозитория>
   cd <имя_папки>
   ```

2. Убедитесь, что у вас установлен Docker и Docker Compose.

3. Создайте файл `.env` в корневой директории проекта и заполните его следующими переменными окружения:
   ```env
   # Telegram
   TELEGRAM_TOKEN=<ваш_токен_бота>
   TELEGRAM_ADMIN_IDS=<id_админов_через_запятую>

   # Pocketbase
   DB_CHOICE=pocketbase  # или fakepb для использования локального хранилища
   PB_URL=<URL_вашего_Pocketbase>
   PB_ADMIN_EMAIL=<ваш_админ_емейл>
   PB_ADMIN_PASSWORD=<ваш_админ_пароль>

   # Tables
   PB_CHATS_TABLENAME=tgbot_chats
   PB_CHATS_TABLEID=fwwayu3bobzjqzh
   PB_LOGS_TABLENAME=tgbot_logs
   PB_LOGS_TABLEID=bp86l9r6d95asfv
   PB_SNIPPETS_TABLENAME=tgbot_snippets
   PB_SNIPPETS_TABLEID=fs1hwbt2cemscgt
   ```

4. Соберите и запустите контейнеры:
   ```bash
   docker-compose up -d --build
   ```

## Использование

- Команды бота:
  - `/start` - Начать работу с ботом.
  - `/add_chat` - Добавить текущий чат.
  - `/remove_chat` - Удалить текущий чат.
  - `/all_guides` - Показать все доступные сниппеты.
  - `/send_news <сообщение>` - Отправить новость во все чаты.
  - `/sync_pb` - Синхронизировать команды и сниппеты.

## Логирование
Логи приложения сохраняются в файл `logs/app.log`. Вы можете изменить уровень логирования в файле `main.py`.

## Вклад
Если вы хотите внести свой вклад в проект, пожалуйста, создайте pull request или откройте issue.

## Лицензия
Этот проект лицензирован под MIT License.



