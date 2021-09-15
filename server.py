#_*_ coding: utf-8 _*_
import os
import re

from sorting_bot import telegram_chatbot
from dbmanager import datamanager

#File paths
if os.path.isfile(os.path.abspath(r'.\config.cfg')):
    config_path = os.path.abspath(r'.\config.cfg')
    db_path = os.path.abspath(r'.\database.sql')
else:
    config_path = r'/app/config.cfg'
    db_path = r'/app/database.sql'
        

#Class calls
bot = telegram_chatbot(config_path)
db = datamanager(db_path)

#Variable definitions
update_id = None
reply = ''
parse_mode = None

#Commands and Reponses tuples
commands = ('/synthesize tables', '/Houses', '/award ', '/sort me',  '/member list', '/about me', '/appoint me', '/commands list')
messages = ()
m_responses = ()
c_responses = (('...', '...', 'Tables systhesized', 'Tables already in existense'),)

#Tuples of Houses
houses = ('Gryffindor', 'Hufflepuff', 'Slytherin', 'Ravenclaw')


def exec_commands(com):
    """Handles and replies any recieved commands"""
    reply = ''
    if com is not None:
        if com == commands[0]:
            tables = db.create_tables(houses, from_)
            if tables == True:
                for j in range(len(c_responses[0]) - 1):
# can use join and split functions to create softer code?? at least in future instances
                    bot.send_message(c_responses[0][j], from_)
            else:
                reply = c_responses[0][(len(c_responses[0])-1)]
        elif com == commands[1]:
            house_info = db.house_info(from_)
            # Add feautures to find highest scoring house and return number of members
            reply = "Houses:\n"
            for house in house_info:
                reply += house[1] + "\n"
                if house[2] != None:
                    reply += f"Score: {house[2]}pts\n\n"
                else:
                    reply += f"Score: 0pts\n\n"
        elif com.startswith(commands[2]):
            instructions = com.split()
            id = 0
            info = user_query()
            user_id = info['user']['id']
            check = db.check_admin(from_, user_id)
            if check and check != 'not sorted':
                for house in houses:
                    id += 1
                    if house == instructions[1]:
                        score = db.update_house_score(id, instructions[2], from_)
                        reply = f"{instructions[1]} new score is {score}"
            else:
                reply = "You have no power over me! PS:(if you are an admin use the /appoint me command to be recognised as such)"


        elif com == commands[3]:
            username = item['message']['from']['username']
            user_id = item['message']['from']['id']
            num = db.add_member_info(username, from_, user_id)
            if num[1]:
                reply = f"Better be... {houses[num[0]-1]}"
            else:
                print(num[0][0])
                reply = f"I stand by my decision, {houses[num[0][0]-1]} will help you on the way to greatness!"
        elif com == commands[4]:
            m_list = db.member_info(from_)
            reply = str(m_list)
        elif com == commands[5]:
            info = user_query()
            username = info['user']['username']
            m_info = db.member_info(from_, username)
            reply = f"""
            Username: {m_info[2]}\nHouse: {houses[m_info[3]]}\nStatus: {m_info[4]}\nScore: {m_info[5]}\n
            """
        elif com == commands[6]:
            info = user_query()
            username = info['user']['username']
            user_id = info['user']['id']
            status_info = info['status']
            if status_info == 'creator':
                verify = db.check_admin(from_, user_id)
                if  not verify:
                    db.update_member_status(from_, info['user']['id'], 'Headmaster')
                    reply = f"Rise Headmaster {username}"
                elif verify == 'not sorted':
                    reply = "Don't be hasty! if tables have already been created use the '/sort me' command to get yourself sorted first"
                else:
                    reply = "We've already done this Headmaster"
            elif status_info == 'administrator':
                verify = db.check_admin(from_, user_id)
                if not verify:
                    db.update_member_status(from_, info['user']['id'], 'Professor')
                    reply = f"Hence forth you shall be known as Professor {username}"
                elif verify == 'not sorted':
                    reply = "Don't be hasty! if tables have already been created use the '/sort me' command to get yourself sorted first"
                else:
                    reply = "We've already done this Professor"
            else:
                reply = 'Desist pretender! Only the entitled may command me so!'
        elif com == commands[7]:
            for command in commands:
                reply += f'{command}\n'
            print(reply)
            
    return reply

def user_query():
    user_id = item['message']['from']['id']
    data = bot.get_chatmember(user_id, from_)
    user_info = data['result']
    return user_info

def make_reply(msg):
    """Provides a reply when messages are recieved"""
    reply = ''
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
                message = item["my_chat_member"]["chat"]["title"]
                reply = "Mmmmmmm so this is " + message + ".\nInteresting...\nTo begin create a unique database for your group using the '/synthesize tables' command"
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