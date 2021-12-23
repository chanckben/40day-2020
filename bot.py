#! /usr/bin/env python3

from logic import get_devo_chunks, get_parse_mode
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import os

pending_users = set()

TOKEN = os.environ.get('TOKEN')
PORT = int(os.environ.get('PORT', '8443'))

# Commands

def get_entry(update, context):
    for chunk in get_devo_chunks():
        update.message.reply_text(chunk, parse_mode=get_parse_mode())

def get_date_entry(update, context):
    pending_users.add(update.message.from_user.id)
    update.message.reply_text("Please enter the date of the desired prayer entry in the format <month> <day>, spelling the month in full, e.g. July 20. The acceptable date range is July 1 to August 9.")

def get_command_default(update, context):
    update.message.reply_text("Please enter a valid command")

# Messages

def reply_date(update, context):
    if update.message.from_user.id in pending_users:
        try:
            devo = get_devo_chunks(date=update.message.text)
            for chunk in devo:
                update.message.reply_text(chunk, parse_mode=get_parse_mode())
        except ValueError:
            update.message.reply_text("Please enter a valid date. Enter the date in the format <month> <day>, spelling the month in full, e.g. July 20. The acceptable date range is July 1 to August 9.")
        pending_users.remove(update.message.from_user.id)
    else:
        update.message.reply_text("Hello!")

def main():
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary
    updater = Updater(TOKEN)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # Add handlers for commands
    dp.add_handler(CommandHandler("getdateentry", get_date_entry))
    dp.add_handler(CommandHandler("getentry", get_entry))
    dp.add_handler(MessageHandler(Filters.command, get_command_default))

    # Add handlers for messages
    dp.add_handler(MessageHandler(Filters.text, reply_date))

    # Start the Bot
    updater.start_webhook(listen='0.0.0.0', port=PORT, url_path=TOKEN, webhook_url='https://fortyday.herokuapp.com/' + TOKEN)

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()

if __name__ == '__main__':
    main()