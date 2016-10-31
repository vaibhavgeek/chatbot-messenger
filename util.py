import json
import requests
from random import randint
import random
import xml.etree.ElementTree
import math

def send_typing_status(recipient):
  """Send the message text to recipient with id recipient.
  """
  r = requests.post(SEND_MESSAGE_URL,
    params={"access_token": token},
      data=json.dumps({
          "recipient": {"id": recipient},
      "sender_action": "typing_on"
    }),
      headers={'Content-type': 'application/json'})
  if r.status_code != requests.codes.ok:
    print r.text

def get_solution_from_wolfarmAlpha(question):
    url = "http://api.wolframalpha.com/v2/query"
    params = {"input" : question, "appid" : "Q7K5HX-2Y24EKLAQW", "format" : 'image,plaintext'}
    r = requests.get(url, params = params)
    root = xml.etree.ElementTree.fromstring(r.text)
    response = []
    count = 0
    for f in root:
        if count == 0:
            count = count + 1
            continue
        temp = {}
        temp["title"] = f.attrib['title']
        temp["img"] = f[0][0].attrib['src']
        response.append(temp)
    return response

def send_text_message(recipient, text):
  """Send the message text to recipient with id recipient.
  """

  r = requests.post(SEND_MESSAGE_URL,
    params={"access_token": token},
      data=json.dumps({
          "recipient": {"id": recipient},
      "message": {"text": text.decode('unicode_escape')},
    }),
      headers={'Content-type': 'application/json'})
  if r.status_code != requests.codes.ok:
    print r.text

def send_button_template_message(recipient, text, buttons):
    r = requests.post(SEND_MESSAGE_URL,
          params={'access_token': token},
          data=json.dumps({
              "recipient": {"id": recipient},
              "message": {
                  "attachment": {
                  "type": "template",
                  "payload": {
                      "template_type": "button",
                      "text": text,
                      "buttons": buttons
                  }
              }}
          }),
          headers={'Content-type': 'application/json'})
    print r.text


def send_image(recipent, item, type="image"):
    r = requests.post(SEND_MESSAGE_URL, params = {'access_token' : token},
            data = json.dumps({
                "recipient" : {"id" : recipent},
                "message" : {
                    "attachment" : {
                        "type" : type,
                        "payload" : {
                            "url" : item
                        }
                    }
                }
            }),
            headers = {'Content-type' : 'application/json'}
        )
    print r.text

def send_carasol_items(recipient, items):
    r = requests.post(SEND_MESSAGE_URL,
          params={'access_token': token},
          data=json.dumps({
              "recipient": {"id": recipient},
              "message": {"attachment":
                    {
                        "type": "template",
                        "payload": {
                          "template_type": "generic",
                          "elements": items
                      }
                 }
            }
        }),
        headers={'Content-type': 'application/json'})
    print r.text


def generate_carasol_items(text, image_url, payload = None, showbtns = True):
    if showbtns:
        return {
            "title": text,
            "image_url": image_url,
            "buttons": [
                {
                    "type": "postback",
                    "title": "Learn This",
                    "payload": payload
                }
            ]
        }
    else:
        return {
            "title": text,
            "image_url": image_url,
        }



def generate_button(text, payload=None, type="text", url=None):
    if type == "url":
        return {
            "type": "web_url",
            "url": url,
            "title": text
        }
    else:
        return {
            "type": "postback",
            "title": text,
            "payload": payload
        }


def messaging_events(payload):
    """Generate tuples of (sender_id, message_text) from the
    provided payload.
    """
    data = json.loads(payload)
    messaging_events = data["entry"][0]["messaging"]
    for event in messaging_events:
        if "message" in event and "text" in event["message"]:
            return (event["sender"]["id"], event["message"]
                ["text"].encode('unicode_escape'))
        elif "postback" in event and "payload" in event["postback"]:
            return (event["sender"]["id"], event["postback"]["payload"])
