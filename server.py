#_*_ coding: utf-8 _*_
import os
import re

from sorting_bot import telegram_chatbot
from dbmanager import datamanager

#File paths
config_path = os.path.abspath('.\config.cfg')
db_path = os.path.abspath('.\database.sql')

#Class calls
bot = telegram_chatbot(config_path)
db = datamanager(db_path)

#Variable definitions
update_id = None
reply = None 

#Commands and Reponses tuples
messages = ('/synthesize tables', '/Houses')
responses = (('...', '...', 'Tables systhesized', 'Tables already in existense'),)

#Tuples of Houses
houses = ('Gryffindor', 'Hufflepuff', 'Slytherin', 'Ravenclaw')

def make_reply(msg):
    """Provides a reply when messages are recieved"""
    reply = None 

    if msg is not None:
        for i in range(len(messages)):
            if msg == messages[i] and i == 0:
                tables = db.create_tables(houses)
                print(tables)
                if tables == True:
                    for j in range(len(responses[i]) - 1):
                        #can use join and split functions to create softer code?? at least in future instances
                        bot.send_message(responses[i][j], from_)
                else:
                    reply = responses[i][(len(responses[i])-1)]
                break
            elif msg == messages[i] and i == 1:
                house_info = db.house_info()
                reply = 'House ID | HOUSE  | SCORE \n'
                for house in house_info:
                    reply += f'{house[0]} | {house[1]} | {house[2]}\n'
    return reply

#Checks for updates to messages and passes re to make reply function
while True:
    print('...')
    updates = bot.get_updates(offset=update_id)
    updates = updates['result']
    if updates:
        for item in updates:
            update_id = item["update_id"]
        try:
            #Identifies situations where bot has just been add to a group and replies as directed
            if "my_chat_member" in item:
                message = item["my_chat_member"]["chat"]["title"]
                reply = "Sup"
                from_ = item["my_chat_member"]["chat"]["id"]
            #Identifies if message was sent from group to the make reply function
            elif item["message"]["chat"]["type"] == "supergroup" or "group":
                message = item["message"]["text"]
                from_ = item["message"]["chat"]["id"]
                reply = make_reply(message)
            else:
            #Identifies messages and sends results to the make reply function
                message = item["message"]["text"]
                from_ = item["message"]["from"]["id"]
                reply = make_reply(message)
        except KeyError:
            message = None
            from_ = None
        bot.send_message(reply, from_) 