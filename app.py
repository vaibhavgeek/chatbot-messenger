import os
import sys
import json

import requests
from flask import Flask, request
from util import *
import traceback
import random
app = Flask(__name__)


@app.route('/', methods=['GET'])
def verify():
    # when the endpoint is registered as a webhook, it must echo back
    # the 'hub.challenge' value it receives in the query arguments
    if request.args.get("hub.mode") == "subscribe" and request.args.get("hub.challenge"):
        if not request.args.get("hub.verify_token") == os.environ["VERIFY_TOKEN"]:
            return "Verification token mismatch", 403
        return request.args["hub.challenge"], 200

    return "Hello world", 200


@app.route('/', methods=['POST'])
def webhook():
    data = request.get_json()
    try:
        if get_message(data):
            message_t , sender = get_message(data)
            if message_t.lower() == "help":
                send_text_message(sender , "You can choose topic you would like to learn and practice from the menu on left. For more information you can drop us a message and we will reply back to you shortly. ")
    except:
        pass            
    
    try:
        payload = request.get_data()
        sender, message = messaging_events(payload)
        if message == "help":
            send_text_message(sender , "You can choose topic you would like to learn and practice from the menu on left. For more information you can drop us a message and we will reply back to you shortly. ")
        elif message == "topics_to_learn":
            send_replies(
                sender, "Answer these questions"
                [
                    generate_carasol_items(
                        "Operation on numbers"
                        "ON"),
                    generate_carasol_items(
                        "Linear Equations in two varaibles",
                        "LINEAR"),
                    generate_carasol_items(
                        "Quadratic Equations",
                        "QUAD"),
                    generate_carasol_items(
                        "Basic Trignometry",
                        "BT")])
    except: 
        pass        
    return "ok"

def log(message):  # simple wrapper for logging to stdout on heroku
    print str(message)
    sys.stdout.flush()


if __name__ == '__main__':
    app.run(debug=True)
