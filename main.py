#! /usr/bin/env python3

from flask import Flask, request
from logic import get_devo_chunks
from telegram.ext import Updater
import configparser
import telegram
import os

switches = {"getdateentry": False}

def read_from_config_file(config):
    parser = configparser.ConfigParser()
    parser.read(config)
    return (parser.get('creds', 'token'), parser.get('creds', 'url'))

#TOKEN, URL = read_from_config_file('config.cfg')
TOKEN = os.environ.get('TOKEN')
PORT = int(os.environ.get('PORT', '8443'))
bot = telegram.Bot(token=TOKEN)
updater = Updater(TOKEN)

def reply_command(command):
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
        return reply_message(msg)

app = Flask(__name__)

@app.route('/{}'.format(TOKEN), methods=['GET', 'POST'])
def run():
    update = request.get_json(force=True)
    chat_id = update["message"]["chat"]["id"]
    message = str(update["message"]["text"])

    replies = make_reply(message)
    for reply in replies:
        try:
            bot.sendMessage(chat_id=chat_id, text=reply, parse_mode="Markdown")
        except Exception as e:
            # Ideally log the error
            pass

    return 'OK'

@app.route('/setwebhook', methods=['GET', 'POST'])
def set_webhook():
    updater.start_webhook(listen='0.0.0.0', port=PORT, url_path=TOKEN, webhook_url="https://fortyday.herokuapp.com/" + TOKEN)
    updater.idle()
    '''s = bot.setWebhook(URL + TOKEN)
    if s:
        return "webhook setup ok"
    else:
        return "webhook setup failed"'''

@app.route('/deletewebhook', methods=['GET', 'POST'])
def delete_webhook():
    updater.stop()
    '''s = bot.deleteWebhook()
    if s:
        return "webhook deletion ok"
    else:
        return "webhook deletion failed"'''

@app.route('/')
def index():
    return '40day bot backend running.'

if __name__ == '__main__':
    #app.run(host='127.0.0.1', port=443, debug=True)
    app.run(threaded=True)