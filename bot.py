from pathlib import Path
import logging
from logging.handlers import RotatingFileHandler

import telebot
import fastapi

from constants import API_TOKEN, WELCOME_MESSAGE, ZIPFILE_DIR, TEMP_DIR, RESULT_DIR, DIRS_FOR_COPY, BASE_DIR, WRONG_FORMAT_MESSAGE, HANDLE_ZIP_MESSAGE
from convert import main, process_zip, zip_folder
from exceptions import EmptyIDError, HTMLFileNotFoundError, ZipFileError

formatter = logging.Formatter("%(name)s %(asctime)s %(levelname)s %(message)s")
logger = telebot.logger
handler = RotatingFileHandler('bot.log', maxBytes=50000000, backupCount=5)
handler.setFormatter(formatter)
logger.addHandler(handler)

bot = telebot.TeleBot(API_TOKEN)
app = fastapi.FastAPI()


@app.post('/secret_webhook/')
def process_webhook(update: dict):
    if update:
        update = telebot.types.Update.de_json(update)
        bot.process_new_updates([update])
    return
    

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(message.chat.id, WELCOME_MESSAGE)


@bot.message_handler(content_types=['document'])
def handle_zip(message: telebot.types.Message):
    if message.document.mime_type != 'application/zip':
        bot.send_message(message.chat.id, WRONG_FORMAT_MESSAGE)
        return
    
    bot.send_message(message.chat.id, HANDLE_ZIP_MESSAGE)
    try:
        file_info = bot.get_file(message.document.file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        file = ZIPFILE_DIR / 'downloaded_archive.zip'
        with open(file, 'wb') as f:
            f.write(downloaded_file)
        main(ZIPFILE_DIR, TEMP_DIR, RESULT_DIR, DIRS_FOR_COPY, process_zip)
        zip_folder(RESULT_DIR, 'result')
        with open('result.zip', 'rb') as zip_file:
            bot.send_document(message.chat.id, zip_file)
    except EmptyIDError as e:
        logger.error(f'Пользователь {message.from_user.username}-{message.chat.id}. {e}')
        bot.reply_to(message, f"Произошла ошибка: {e}")
        bot.send_photo(message.chat.id, open(BASE_DIR / 'id.jpg', 'rb'))
    except (HTMLFileNotFoundError, ZipFileError) as e:
        logger.error(f'Пользователь {message.from_user.username}-{message.chat.id}. {e}')
        bot.reply_to(message, f"Произошла ошибка: {e}")
    except Exception as e:
        logger.error(f'Пользователь {message.from_user.username}-{message.chat.id}. {e}')
        bot.reply_to(message, f"Произошла какая-то страшная ошибка. Отправил ее разработчику.")
    finally:
        Path(BASE_DIR /'result.zip').unlink()
        file.unlink()
    

if __name__ == '__main__':
    bot.infinity_polling()
