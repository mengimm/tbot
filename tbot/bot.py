from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove,KeyboardButton
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters, RegexHandler,
                          ConversationHandler)
import config

import logging

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

PHONE = range(1)


def start(bot, update):
    contact_keyboard = KeyboardButton(text="передать свой номер телефона", request_contact=True)

    update.message.reply_text(
        'Отправьте свой номер телефона',
        reply_markup=ReplyKeyboardMarkup([[contact_keyboard]], one_time_keyboard=True))

    return PHONE


def get_phone(bot, update):
    contact_keyboard = KeyboardButton(text="передать свой номер телефона", request_contact=True)
    user = update.message.from_user
    contact=update.message.contact

    user_id1=user.id
    user_id2=contact.user_id


    if user_id1==user_id2:
        str='Уважаемый '+user.first_name+' Ваш номер '+contact.phone_number+' принят'
        update.message.reply_text(str,reply_markup=ReplyKeyboardRemove())
        logger.info(str)
        return ConversationHandler.END
    else:
        str='номер '+contact.phone_number+' не принадлежит пользователю '+user.first_name+' заново отправьте с помощью специальной кнопки'
        update.message.reply_text(str,
                                  reply_markup=ReplyKeyboardMarkup([[contact_keyboard]], one_time_keyboard=True))
        logger.info(str)
        return PHONE



def skip_phone(bot, update):
    user = update.message.from_user
    logger.info("User %s did not send a location.", user.first_name)
    update.message.reply_text('You seem a bit paranoid! '
                              'At last, tell me something about yourself.')

    return ConversationHandler.END


def cancel(bot, update):
    user = update.message.from_user
    logger.info("User %s canceled the conversation.", user.first_name,update.message.contact)
    update.message.reply_text('Bye! I hope we can talk again some day.',
                              reply_markup=ReplyKeyboardRemove())

    return ConversationHandler.END


def error(bot, update, error):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, error)


def main():
    # Create the EventHandler and pass it your bot's token.
    updater = Updater(config.token)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # Add conversation handler with the states GENDER, PHOTO, LOCATION and BIO
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],

        states={
            PHONE: [MessageHandler(Filters.contact, get_phone),
                    CommandHandler('skip', skip_phone)],

        },

        fallbacks=[CommandHandler('cancel', cancel)]
    )

    dp.add_handler(conv_handler)

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()