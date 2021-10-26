import datetime
import re

import telegram.utils.request
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils import executor
from states import RegisterStates

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
button_register_back = 'Назад'
button_register_cancel = 'Отменить'

bot = Bot(token=TG_TOKEN, )
dp = Dispatcher(bot)

@dp.message_handler(commands=['help', button_help])
async def button_help_handler(message: types.Message):
    await message.se(
        text='Добрый день, вас приветствует бот. Для управления ботом требуется использовать клавиатуру',
    )


@dp.message_handler(commands=['start'])
async def start_user_handler(message: types.Message):
    username = message.from_user.username
    first_name = message.from_user.first_name
    last_name = message.from_user.last_name
    tg_user_id = message.from_user.id
    tg_chat_id = message.chat.id
    if first_name is None:
        first_name = ""
    if last_name is None:
        last_name = ""

    new_user(user_full_name=first_name + ' ' + last_name,
             tg_username=username,
             tg_user_id=tg_user_id,
             tg_chat_id=tg_chat_id)


@dp.message_handler()
async def message_handler(message: types.Message):
    text = message.text
    contact = message.contact
    tg_user_id = message.from_user.id
    print(f'User with username: {message.from_user.username} and chatid: {message.chat.id} requested: {text}')
    if text == 'test':
        await message.reply(
            text='Hello, this was test',
        )
        return
    reply_markup = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text=button_register, ),
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
    await bot.send_message(
        chat_id=message.chat.id,
        text='Hello, press button below',
        reply_markup=reply_markup,)



# def register_handler(update: Update, context: CallbackContext):
#     reply_markup = ReplyKeyboardMarkup(
#         keyboard=[
#             [
#                 KeyboardButton(text=button_register_back),
#                 KeyboardButton(text=button_register_cancel)
#             ],
#         ],
#         resize_keyboard=True,
#     )
#     if update.message.text == button_register:
#         update.message.reply_text(text="Напишите свои фамилию имя и отчество", reply_markup=reply_markup)
#         return FULLNAME



# def set_full_name(update: Update, context: CallbackContext):
#     text = update.message.text
#     while not re.fullmatch(r'[А-ЯЁ][а-яё]+\s+[А-ЯЁ][а-яё]+(?:\s+[А-ЯЁ][а-яё]+)?', text):
#         update.message.reply_text(text="Напишите свои ФИО по русски")
#         return FULLNAME
#     print(f"User fullname: {text}")
#     update.message.reply_text(text="Напишите свою дату рождения")
#     return DATEBIRTH
#
#
# def set_birth_date(update: Update, context: CallbackContext):
#     text = update.message.text
#     print(f"User datebirth: {text}")
#     update.message.reply_text(text="Напишите свое место проживания")
#     return PLACEOFRESIDENCE
#
#
# def set_res_place(update: Update, context: CallbackContext):
#     text = update.message.text
#     print(f"User place of residence: {text}")
#     update.message.reply_text(text="Напишите свой номер телефона")
#     return PHONENUM
#
#
# def set_phone_num(update: Update, context: CallbackContext):
#     text = update.message.text
#     print(f"User phone number: {text}")
#     update.message.reply_text(text="Напишите свою серию паспорта")
#     return PASSSERIES
#
#
# def set_pass_series(update: Update, context: CallbackContext):
#     text = update.message.text
#     print(f"User passport series: {text}")
#     update.message.reply_text(text="Напишите свой номер паспорта")
#     return PASSNUM
#
#
# def set_pass_number(update: Update, context: CallbackContext):
#     text = update.message.text
#     print(f"User passport number: {text}")
#     update.message.reply_text(text="Напишите свою дату выдачи паспорта")
#     return PASSDATEOFISSUE
#
#
# def set_pass_date_of_issue(update: Update, context: CallbackContext):
#     text = update.message.text
#     print(f"User passport date of issue: {text}")
#     update.message.reply_text(text="Напишите кем выдан ваш паспорт")
#     return PASSISSUEDBY
#
#
# def set_pass_issued_by(update: Update, context: CallbackContext):
#     text = update.message.text
#     print(f"User passport issued by: {text}")
#     update.message.reply_text(text="Напишите свой адрес регистрации из паспорта")
#     return REGISTRADDR
#
#
# def set_reg_address(update: Update, context: CallbackContext):
#     text = update.message.text
#     print(f"User register address: {text}")
#     update.message.reply_text(text="Напишите свою email")
#     return EMAIL
#
#
# def set_email(update: Update, context: CallbackContext):
#     text = update.message.text
#     print(f"User email: {text}")
#     update.message.reply_text(text="Напишите свою специальность")
#     return MAJOR
#
#
# def set_major(update: Update, context: CallbackContext):
#     text = update.message.text
#     print(f"User major: {text}")
#     update.message.reply_text(text="Спасибо, Вы успешно зарегистрированы")
#     return ConversationHandler.END
#
#
# def cancel(update: Update, context: CallbackContext):
#     if update.message.text == button_register_cancel:
#         user = update.message.from_user
#         print(f"User {user.first_name} canceled the conversation.")
#
#         return ConversationHandler.END


@log_errors
def main():
    print(RegisterStates.all())
    print('Program is started')

    print(f'Info about bot: {bot.get_webhook_info()}')
    executor.start_polling(dp)
    print('Finish')


if __name__ == '__main__':
    main()
