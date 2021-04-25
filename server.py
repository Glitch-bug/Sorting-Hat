#_*_ coding: utf-8 _*_
from sorting_bot import telegram_chatbot

bot = telegram_chatbot(r"\Users\t\Desktop\CodeFiles\Python\Sorting Hat Bot\config.cfg")
update_id = None

def make_reply(msg):
    """Provides a reply when messages are recieved"""
    if msg:
        reply = "Functional"
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