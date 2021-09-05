import requests
import json
import configparser as cfg


class telegram_chatbot():
    def __init__(self, config):
        """Initializes bot and saves bot token into variable"""
        self.token = self.read_token_from_config_file(config)
        self.base = "https://api.telegram.org/bot{}/".format(self.token)
    
    def get_updates(self, offset=None):
        """Requests updates repeatedly each request lasting 200secs"""
        url = self.base + "getUpdates?timeout=200"
        if offset:
            url = url + "&offset={}".format(offset + 1)
        r = requests.get(url)
        return json.loads(r.content)
    
    def send_message(self, msg, chat_id, parse_mode=None):
        url = self.base + "sendMessage?chat_id={}&text={}&parse_mode={}".format(chat_id, msg, parse_mode)
        if msg is not None:
            requests.get(url)
    
    def get_chatmember(self, user_id, chat_id):
        url = self.base + "getChatMember?chat_id={}&user_id={}".format(chat_id, user_id)
        r = requests.get(url)
        return json.loads(r.content)
    
    def read_token_from_config_file(self, config):
        """Reads token from config file"""
        parser = cfg.ConfigParser()
        parser.read(config)
        return parser.get('creds', 'token')