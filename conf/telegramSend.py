import os
import logging
import asyncio
from telegram import Bot
from telegram.error import TelegramError, BadRequest, NetworkError
from telegram.request import HTTPXRequest   # ← добавили для прокси
import sys

NameProduct = sys.argv[1]

# ================== НАСТРОЙКИ ==================
telegram_token = '7117726988:AAEArlt130DMloEkDYI8Pvbl3gLl_SCFS9g'
chat_id = '-1002167629740'

# Путь к файлу
file_path = rf'Результаты сверки/ConfigurationComparison.png'

# ←←← ПРОКСИ (теперь по умолчанию) ←←←
PROXY_URL = "http://109.235.119.4:42587"

# Настройка HTTPXRequest с прокси
request = HTTPXRequest(
    proxy_url=PROXY_URL,
    connect_timeout=20.0,   # таймаут подключения
    read_timeout=20.0       # таймаут чтения ответа
)
# ===============================================

# Настройка логирования
logging.basicConfig(level=logging.INFO)


async def send_file():
    # Создаём бота с прокси
    bot = Bot(token=telegram_token, request=request)
   
    if not os.path.exists(file_path):
        logging.error(f"File not found: {file_path}")
        return

    try:
        with open(file_path, 'rb') as file:
            # Отправка файла
            message = await bot.send_document(
                chat_id=chat_id,
                document=file,
                caption=f"Сверка продукта {NameProduct}"
            )
            logging.info(f"File {file_path} with caption 'Сверка продукта {NameProduct}' "
                        f"successfully sent to chat ID {chat_id}. Message ID: {message.message_id}")

        # Проверка, что файл отправлен
        if message.document:
            await asyncio.sleep(5)
            try:
                os.remove(file_path)
                logging.info(f"File {file_path} deleted from local storage.")
            except Exception as e:
                logging.error(f"Error deleting file {file_path}: {e}")
        else:
            logging.error("File was not properly sent. No document found.")

    except BadRequest as e:
        logging.error(f"Bad request: {e}")
    except NetworkError as e:
        logging.error(f"Network error: {e}")
    except TelegramError as e:
        logging.error(f"Telegram error: {e}")
    except Exception as e:
        logging.error(f"Unexpected error: {e}")


# Запуск
if __name__ == "__main__":
    asyncio.run(send_file())