import datetime

import telegram.utils.request
from telegram import Update, ReplyKeyboardRemove, Bot, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import Updater, CallbackContext, Filters, MessageHandler
from telegram.utils.request import Request

from mysql_func import new_user, find_user
from settings import TG_TOKEN


def log_errors(f):
    def inner(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except Exception as e:
            print(f'Error: {e}')
            raise e

    return inner


button_help = 'Помощь'
button_register = 'Зарегистрироваться'


def button_help_handler(update: Update, context: CallbackContext):
    update.message.reply_text(
        text='Добрый день, вас приветствует бот. Для управления ботом требуется использовать клавиатуру',
    )


def button_register_handler(update: Update, context: CallbackContext):
    username = update.message.from_user.username
    first_name = update.message.from_user.first_name
    last_name = update.message.from_user.last_name
    phone = update.message.contact.phone_number
    if first_name is None:
        first_name = "Pass"
    if last_name is None:
        last_name = "Pass"
    user_id = update.message.from_user.id
    new_user(user_full_name=first_name + ' ' + last_name, tg_username=username, tg_user_id=user_id)
    update.message.reply_text(
        text=f'Добрый день, вы занесены в базу данных, с именем пользователя: {username} и телефоном {phone}',
    )


def message_handler(update: Update, context: CallbackContext):
    text = update.message.text
    contact = update.message.contact
    tg_user_id = update.message.from_user.id
    print(f'User with tg_id: {tg_user_id} requested: {text}')
    if text == button_help:
        return button_help_handler(update=update, context=context)
    if text == 'test':
        update.message.reply_text(
            text='Hello, this was test',
        )
        return
    reply_markup = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text=button_register, request_contact=True, ),
            ],
            [
                KeyboardButton(text=button_help),
            ],
            [
                KeyboardButton(text='test'),
            ],
        ],
        resize_keyboard=True,
    )
    if contact is not None:
        reply_markup.keyboard.remove([KeyboardButton(text=button_register, request_contact=True, )])
        update.message.reply_text(text='Регистрация', reply_markup=reply_markup, )
        return button_register_handler(update=update, context=context)
    if find_user(tg_user_id=tg_user_id):
        reply_markup.keyboard.remove([KeyboardButton(text=button_register, request_contact=True, )])
    update.message.reply_text(
        text='Hello, press button below',
        reply_markup=reply_markup,
    )


@log_errors
def main():
    print('Program is started')
    req = Request(
        connect_timeout=9,
        con_pool_size=8
    )
    bot = Bot(
        request=req,
        token=TG_TOKEN,
    )
    updater = Updater(
        bot=bot,
        use_context=True,
    )
    print(f'Info about bot: {updater.bot.get_me()}')
    updater.dispatcher.add_handler(MessageHandler(filters=Filters.all, callback=message_handler))
    updater.start_polling()
    updater.idle()

    print('Finish')


if __name__ == '__main__':
    main()
