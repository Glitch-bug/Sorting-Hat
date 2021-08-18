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
parse_mode = None

#Commands and Reponses tuples
commands = ('/synthesize tables', '/Houses', '/award ', '/sort me',  '/member list', '/about me')
messages = ()
m_responses = ()
c_responses = (('...', '...', 'Tables systhesized', 'Tables already in existense'),)

#Tuples of Houses
houses = ('Gryffindor', 'Hufflepuff', 'Slytherin', 'Ravenclaw')

def exec_commands(com):
    """Handles and replies any recieved commands"""
    reply = None
    if com is not None:
        for i in range(len(commands)):
            if com == commands[i] and i == 0:
                tables = db.create_tables(houses, from_)
                if tables == True:
                    for j in range(len(c_responses[i]) - 1):
# can use join and split functions to create softer code?? at least in future instances
                        bot.send_message(c_responses[i][j], from_)
                else:
                    reply = c_responses[i][(len(c_responses[i])-1)]
                break
            elif com == commands[i] and i == 1:
                house_info = db.house_info(from_)
                reply = '*__Houses__*'.center(20,)+' '*10+'\n'+'HOUSE'+ ' '*14+'SCORE'+'\n'
                for house in house_info:
                    if house[0] == 3:
                        reply += f'{house[1]}' + ' '*12 + f'{house[2]}'+'\n'
                    elif house[0] == 4:
                        reply += f'{house[1]}' + ' '*8 + f'{house[2]}'+'\n'
                    else:
                        reply += f'{house[1]}' + ' '*10 + f'{house[2]}'+'\n'
                        
            elif com.startswith(commands[i]) and i == 2:
                instructions = com.split()
                id = 0
                for house in houses:
                    id += 1
                    if house == instructions[1]:
                        score = db.update_house_score(id, instructions[2], from_)
                        reply = f"{instructions[1]} new score is {score} "
            elif com == commands[i] and i == 3:
                username = item['message']['from']['username']
                num = db.add_member_info(username, from_)
                reply = f"Better be... {houses[num-1]}"
            elif com == commands[i] and i == 4:
                m_list = db.member_info(from_)
                reply = str(m_list)
                print(reply)
    return reply

def make_reply(msg):
    """Provides a reply when messages are recieved"""
    reply = None 
    if msg is not None:
        for i in range(len(messages)):
            if msg == message[i]:
                reply = m_responses[i]
    return reply

#Checks for updates to messages and passes re to make reply function 
while True:
    print('...')
    updates = bot.get_updates(offset=update_id)
    updates = updates['result']
    parse_mode = None
    if updates:
        for item in updates:
            update_id = item["update_id"]
        try:
            #Identifies situations where bot has just been add to a group and replies as directed
            if "my_chat_member" in item:
                print('red')
                message = item["my_chat_member"]["chat"]["title"]
                reply = "Mmmmmmm so this is " + message + ".\nInteresting..."
                from_ = item["my_chat_member"]["chat"]["id"]
            #Identifies if message was sent from group to the make reply function
            elif item["message"]["chat"]["type"] == "supergroup" or "group":
                message = item["message"]["text"]
                from_ = item["message"]["chat"]["id"]
                if message.startswith('/'):
                    reply = exec_commands(message)
                    # parse_mode = 'MarkdownV2' (prevents certain texts from being recieved for unkown reason)
                else:
                    reply = make_reply(message)
            else:
            #Identifies messages and sends results to the make reply function
                message = item["message"]["text"]
                from_ = item["message"]["from"]["id"]
                if message.startswith("/"):
                    reply = exec_commands(message)
                    parse_mode = 'MarkdownV2'
                else:
                    reply = make_reply(message)
        except KeyError:
            message = None
            from_ = None
        
        bot.send_message(reply, from_, parse_mode)
        print(parse_mode)