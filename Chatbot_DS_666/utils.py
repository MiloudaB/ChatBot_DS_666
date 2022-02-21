#depemdenciesw
import requests
import json
from configFile import *

# function used to get the message'text and its ID
def message_parser(message):
    message_txt = message["message"]["text"]
    message_id = message["message"]["chat"]["id"]

    return message_id, message_txt

##define the bot responses to the given commands
def response_message(message_txt):
    commands = {"/start":"Hello! I am given the name CHATBOT-DS-666, I will be happy if I can help you, use these commands to achieve your goals : \n/track : If you want to track your code \n/end : To end the conversation.",
    "/track" : "You are in the track menu, please type the code you want to track, or  use /menu to return to the main menu", 
    "/menu" : "You are in the main menu, please use one of the following commands: \n/track : To track your code \n/end : To end the conversation.", 
    "/end" : "I am happy if I can help you again, see you later!"}
    if message_txt in commands.keys():
        return commands[message_txt]
    else:
        return "Oups!!! I could not find your command, if you mean track then use /track To track your code or use /end to end the conversation."

#define a function that return the state of the response
def send_message(message_id, message_txt):
    url = "{}/bot{}/sendMessage".format(API_URL,TOKEN)
    payload = {
        "text":message_txt,
        "chat_id":message_id
        }
    response = requests.post(url, json=payload)
    return response

## write the results to a json file
def write_json(data, filename="responseFile.json"):
    with open(filename, 'w') as file:
        json.dump(data, file, indent=4, ensure_ascii=True)

