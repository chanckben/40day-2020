#! /usr/bin/env python3

from logic import get_devo_chunks
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import os

switches = {"getdateentry": False}

TOKEN = os.environ.get('TOKEN')
PORT = int(os.environ.get('PORT', '8443'))

# Commands

def get_entry(update, context):
    for chunk in get_devo_chunks():
        update.message.reply_text(chunk)

def get_date_entry(update, context):
    #switches["getdateentry"] = True
    update.message.reply_text("Please enter the date of the desired prayer entry in the format <month> <day>, spelling the month in full, e.g. July 20. The acceptable date range is July 1 to August 9.")

def get_command_default(update, context):
    update.message.reply_text("Please enter a valid command")

# Messages

def reply_date(update, context):
    update.message.reply(update.text)

def greet(update, context):
    update.message.reply_text("Hello!")

'''def reply_command(command):
    if "/getentry" in command:
        return get_devo_chunks()
    elif "/getdateentry" in command:
        switches["getdateentry"] = True
        return ["Please enter the date of the desired prayer entry in the format <month> <day>, spelling the month in full, e.g. July 20. The acceptable date range is July 1 to August 9."]
    else:
        return ["Please enter a valid command."]

def reply_message(message):
    if switches["getdateentry"]:
        try:
            devo = get_devo_chunks(date=message)
        except ValueError:
            return ["Please enter a valid date. Enter the date in the format <month> <day>, spelling the month in full, e.g. July 20. The acceptable date range is July 1 to August 9."]
        switches["getdateentry"] = False
        return devo
    else:
        return ["Hello!"]

def make_reply(msg):
    if msg[0] == "/":
        return reply_command(msg)
    else:
        return reply_message(msg)'''

def main():
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary
    updater = Updater(TOKEN)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("getdateentry", get_date_entry))
    dp.add_handler(CommandHandler("getentry", get_entry))
    dp.add_handler(MessageHandler(Filters.command, get_command_default))

    # on noncommand i.e message - echo the message on Telegram
    dp.add_handler(MessageHandler(Filters.text, reply_date))

    # Start the Bot
    updater.start_webhook(listen='0.0.0.0', port=PORT, url_path=TOKEN, webhook_url='https://fortyday.herokuapp.com/' + TOKEN)

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()

if __name__ == '__main__':
    #app.run(host='127.0.0.1', port=443, debug=True)
    #app.run(threaded=True)
    main()