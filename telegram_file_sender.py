import os
import logging
import asyncio
from telegram import Bot
from telegram.error import TelegramError, BadRequest, NetworkError
import sys

NameProduct = sys.argv[1]

# Ваш токен бота
telegram_token = '7117726988:AAFJFXz3rF7XyNXK23vtcy6MQG1E9x3DmRc'

# ID чата, в который будет отправлено сообщение
chat_id = '-1002167629740'

# Путь к файлу для отправки
file_path = r'D:\Identificators\log\ConfigurationComparison.png'

# Настройка логирования
logging.basicConfig(level=logging.INFO)

async def send_file():
    bot = Bot(token=telegram_token)
    
    if not os.path.exists(file_path):
        logging.error(f"File not found: {file_path}")
        return

    try:
        with open(file_path, 'rb') as file:
            # Отправка файла с текстом в caption
            message = await bot.send_document(chat_id=chat_id, document=file, caption=f"Сверка продукта {NameProduct}")
            logging.info(f"File {file_path} with caption 'Сверка продукта {NameProduct}' successfully sent to chat ID {chat_id}. Message ID: {message.message_id}")

        # Проверка, что файл успешно отправлен
        if message.document:
            # Небольшая задержка перед удалением файла
            await asyncio.sleep(5)  # Увеличьте время ожидания при необходимости
            try:
                os.remove(file_path)
                logging.info(f"File {file_path} deleted from local storage.")
            except Exception as e:
                logging.error(f"Error deleting file {file_path}: {e}")
        else:
            logging.error(f"File was not properly sent. No document found in the sent message.")
    
    except BadRequest as e:
        logging.error(f"Bad request: {e}. There might be an issue with the chat ID or the file.")
    except NetworkError as e:
        logging.error(f"Network error: {e}. There could be a connection problem.")
    except TelegramError as e:
        logging.error(f"Telegram error: {e}.")
    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")

# Запуск асинхронной функции
asyncio.run(send_file())
