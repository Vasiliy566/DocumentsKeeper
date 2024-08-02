import json
from io import BytesIO
from pprint import pprint

import telebot

from telebot.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton, InputFile, \
    Message, CallbackQuery

from file_storage import FileStorage

BOT_TOKEN = "BOT_TOKEN"

storage = FileStorage("saved_files")
bot = telebot.TeleBot(BOT_TOKEN)

USERS = [359297087]


def is_user_allowed(message: Message):
    return message.from_user.id in USERS


@bot.message_handler(commands=['start'])
def send_welcome(message: Message):
    if not is_user_allowed(message):
        return

    markup = ReplyKeyboardMarkup(resize_keyboard=True)

    upload_file_button = KeyboardButton('upload')
    download_file_button = KeyboardButton('download')

    markup.row(upload_file_button, download_file_button)

    bot.send_message(message.chat.id, "Добро пожаловать, выберите опцию:", reply_markup=markup)


@bot.message_handler(content_types=['document'])
def handle_file(message: Message):
    if not is_user_allowed(message):
        return

    bot.send_message(message.chat.id, "Получен файл.")
    file_info = bot.get_file(message.document.file_id)
    downloaded_file = bot.download_file(file_info.file_path)
    storage.upload_file(message.document.file_name, downloaded_file)


@bot.message_handler(content_types=['text'])
def handle_text(message):
    if not is_user_allowed(message):
        return

    if message.text == 'upload':
        bot.send_message(message.chat.id, "Отправьте файл.")
    elif message.text == 'download':
        markup = InlineKeyboardMarkup()

        for filename in storage.read_all_filenames():
            callback_button = InlineKeyboardButton(text=filename, callback_data=filename)
            markup.add(callback_button)

        bot.send_message(message.chat.id, "Выберите файл", reply_markup=markup)


@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call: CallbackQuery):
    filename = call.data
    chat_id = call.message.chat.id

    document_bytes = storage.get_file_by_name(filename)
    file_content = BytesIO(document_bytes)

    bot.send_document(
        chat_id,
        InputFile(file_content, filename),
        caption=filename
    )


bot.polling(none_stop=True)
