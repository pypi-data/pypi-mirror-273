# my_bot_package/db.py

import json
import os

USER_DATA_FILE = 'users.json'
CHAT_LOGS_DIR = 'chat_logs'

def load_users():
    if not os.path.exists(USER_DATA_FILE):
        return {}
    with open(USER_DATA_FILE, 'r') as file:
        return json.load(file)

def save_users(users):
    with open(USER_DATA_FILE, 'w') as file:
        json.dump(users, file, indent=4)

def load_chat_logs(username):
    chat_file = os.path.join(CHAT_LOGS_DIR, f'{username}.json')
    if not os.path.exists(chat_file):
        return []
    with open(chat_file, 'r') as file:
        return json.load(file)

def save_chat_log(username, chat_log):
    if not os.path.exists(CHAT_LOGS_DIR):
        os.makedirs(CHAT_LOGS_DIR)
    chat_file = os.path.join(CHAT_LOGS_DIR, f'{username}.json')
    with open(chat_file, 'w') as file:
        json.dump(chat_log, file, indent=4)
