from telegram import Update, ReplyKeyboardRemove, Bot, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import Updater, CallbackContext, Filters, MessageHandler
from telegram.utils.request import Request
from settings import TG_TOKEN

button_help = 'Помощь'


def button_help_handler(update: Update, context: CallbackContext):
    update.message.reply_text(
        text='Ты думал я кнопки обрабатываю? Наивный',
        reply_markup=ReplyKeyboardRemove(),
    )


def message_handler(update: Update, context: CallbackContext):
    text = update.message.text
    if text == button_help:
        return button_help_handler(update=update, context=context)
    reply_markup = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text=button_help),
            ],
            [
                KeyboardButton(text="Хеллоу"),
            ],
            [
                KeyboardButton(text=button_help),
            ],
        ],
        resize_keyboard=True,
    )

    update.message.reply_text(
        text='Hello, press button below',
        reply_markup=reply_markup,
    )


def log_errors(f):
    def inner(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except Exception as e:
            print(f'Error: {e}')
            raise e

    return inner


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
