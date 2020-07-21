#! /usr/bin/env python3

from flask import Flask, request
from logic import get_devo_chunks
import configparser
import telegram

def read_from_config_file(config):
    parser = configparser.ConfigParser()
    parser.read(config)
    return (parser.get('creds', 'token'), parser.get('creds', 'url'))

TOKEN, URL = read_from_config_file('config.cfg')
bot = telegram.Bot(token=TOKEN)

def reply_command(command):
    if "/getentry" in command:
        return get_devo_chunks()
    else:
        return ["Please enter a valid command."]

def reply_message(message):
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
    s = bot.setWebhook(URL + TOKEN)
    if s:
        return "webhook setup ok"
    else:
        return "webhook setup failed"

@app.route('/deletewebhook', methods=['GET', 'POST'])
def delete_webhook():
    s = bot.deleteWebhook()
    if s:
        return "webhook deletion ok"
    else:
        return "webhook deletion failed"

@app.route('/')
def index():
    return '40day bot backend running.'

if __name__ == '__main__':
    #app.run(host='127.0.0.1', port=443, debug=True)
    app.run(threaded=True)