import logging
import variables_binance
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, Update
from telegram.ext import (
    Updater,
    CommandHandler,
    MessageHandler,
    Filters,
    ConversationHandler,
    CallbackContext,
)
# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)


CURR, VAL, CURR_to, BIO = range(4)

def start(update: Update, context: CallbackContext) -> int:
    """Starts the conversation and asks the user about their gender."""
    reply_keyboard = [['USD', 'EUR', 'RUB']]

    update.message.reply_text(

        'What currency do you need to convert from?',
        reply_markup=ReplyKeyboardMarkup(
            reply_keyboard, one_time_keyboard=True, input_field_placeholder='Currency from:'
        ),
    )

    return CURR

def currency_from(update: Update, context: CallbackContext) -> int:
    """Stores the selected currency and asks for a value."""
    user = update.message.from_user
    #stores the information extracted from previous function
    logger.info("Currency from: %s",  update.message.text)
    update.message.reply_text(
        'Print the value ',
        reply_markup=ReplyKeyboardRemove(),
    )
    with open ("/Users/Evgenia/Desktop/data.txt", 'w') as f:
        f.write(update.message.text + " ")

    return VAL


def get_value(update: Update, context: CallbackContext) -> int:
    """Stores the value and asks for a currency to."""
    user = update.message.from_user

    logger.info("Value is: %s",  update.message.text)
    with open ("/Users/Evgenia/Desktop/data.txt", 'a') as f:
        f.write(update.message.text + " ")
    reply_keyboard = [['BTC', 'SAT', 'ETH']]

    update.message.reply_text(
        'What crypto currency to convert to',
        reply_markup=ReplyKeyboardMarkup(
            reply_keyboard, one_time_keyboard=True, input_field_placeholder='Currency to:'
        ),
    )
    return CURR_to



def currency_to(update: Update, context: CallbackContext) -> str:
    """Stores the photo and asks for a location."""
    user = update.message.from_user
    logger.info("Currency to: %s",  update.message.text)
    with open ("/Users/Evgenia/Desktop/data.txt", 'a') as f:
        f.write(update.message.text)
    update.message.reply_text(
        'Give me a sec, counting'
    )

    answer = variables_binance.create_ans()
    update.message.reply_text(answer)

    update.message.reply_text('Would you like to continue? press /start If no, you can press /cancel ')

    return BIO


def cancel(update: Update, context: CallbackContext) -> int:
    """Cancels and ends the conversation."""
    user = update.message.from_user
    logger.info("User %s canceled the conversation.", user.first_name)
    update.message.reply_text(
        'Bye! I hope we can talk again some day.', reply_markup=ReplyKeyboardRemove()
    )
    return ConversationHandler.END

'''''
def continue_the_bot(update: Update, context: CallbackContext) -> int:
    return main()
'''''


def main() -> None:
    """Run the bot."""
    # Create the Updater and pass it your bot's token.
    updater = Updater("5217668236:AAFrXXnyH8GiKmJv016bqMl38dH94RlSMaQ")

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # Add conversation handler with the states GENDER, PHOTO, LOCATION and BIO
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            CURR: [MessageHandler(Filters.regex('^(USD|EUR|RUB)$'), currency_from)],
            VAL: [MessageHandler(Filters.text & ~Filters.command, get_value)],
            CURR_to:[MessageHandler(Filters.regex('^(BTC|SAT|ETH)$'), currency_to)],
            BIO: [MessageHandler(Filters.text & ~Filters.command,  cancel)],

        },
        fallbacks=[CommandHandler('cancel', cancel)],
        allow_reentry = True


    )

    dispatcher.add_handler(conv_handler)


    # Start the Bot
    updater.start_polling()


    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()




