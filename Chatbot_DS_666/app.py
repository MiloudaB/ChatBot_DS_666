#dependencies
from flask import Flask, jsonify, request,Response
import requests 
from configFile import *
from utils import *
from database import DataBaseInitiator
import logging

##setting up the logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s,%(message)s')
log_file = logging.FileHandler("dingdingBot.log")
log_file.setFormatter(formatter)
logger.addHandler(log_file)

## initiate the necessary connections of dingdingBot
app = Flask("dingdingBot")
database = DataBaseInitiator()
#database.setup()
connecter = database.connector
listOfCodes = [88,56,12548]
cursor=connecter.cursor()
for index, elements in enumerate(listOfCodes) :
    cursor.execute("insert into Tracking values (?, ?)",(index, elements))
cursor.close()

@app.route("/",methods=["POST", "GET"])
def index():
    if request.method == "POST":
        message = request.get_json()
        message_id, message_txt = message_parser(message)
        file=open('tracked.json','r')
        tracked=json.load(file)
        response = response_message(message_txt)
        logger.info(f"message recived : {message_txt}, response : {response}")
        if tracked['tracked_code']:
            tracked_code = message["message"]["text"]
            check_code = database.check(tracked_code)
            if check_code[0]==1:
                response = "Your code is on the system! Try with these commands \n /track to track another code \n . /menu to return to the main menu. \n /end to end the conversation."
                send_message(message_id, response)
                logger.info(f"message sent : {response}")
            else:
                response = "This code does not exist in the database! \n To try with another code use /track. \n Use /menu to return to the main menu \n Or use /end to end the conversation." 
                send_message(message_id, response)
            tracked["tracked_code"] = False
            file=open('tracked.json','w')
            json.dump(tracked, file)
        
        elif message_txt == '/track':
            tracked_code = message["message"]["text"]
            response='Please enter the code to be tracked!!'
            send_message(message_id, response)
            tracked["tracked_code"] = True
            file=open('tracked.json','w')
            json.dump(tracked, file)
        else :
            send_message(message_id, response)
            logger.info(f"message sent : {response}")
        return jsonify({'work_completed' : 'Ok!','STATUS' : 200})
    else:
        return jsonify({"STATUS" : "Waiting..."})


@app.route("/setwebhook/")
def setwebhook():
    response = requests.get(f"{API_URL}/bot{TOKEN}/setwebhook?url={URL}")
    if response.status_code == 200:
        return jsonify({'STATUS' : 'Ok'})
    else:
        return jsonify({'STATUS' : 'Error'})


if __name__ == '__main__':
    app.run(debug=True)