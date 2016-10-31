from util import *
import json
import requests
from constants import SEND_MESSAGE_URL, PAT as token
from random import randint
import random
import xml.etree.ElementTree
import math

def help_menu:
	send_text_message(sender , "You can choose topic you would like to learn and practice from the menu on left. For more information you can drop us a message and we will reply back to you shortly. ")
