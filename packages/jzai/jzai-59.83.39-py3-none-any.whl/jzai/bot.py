import os
import json
import re
import hashlib
import pyttsx3
import speech_recognition as sr
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from textblob import TextBlob
import nltk
import random

# Ensure necessary NLTK data is downloaded
nltk.download('punkt')
nltk.download('stopwords')


class Bot:
    def __init__(self, name):
        self.name = name
        self.engine = pyttsx3.init()
        self.users = {}
        self.current_user = None
        self.conversations = self.load_conversations("./conversations.json")

    def preprocess_text(self, text):
        # Correct spelling mistakes using TextBlob
        corrected_text = str(TextBlob(text).correct())

        # Tokenization
        tokens = word_tokenize(corrected_text)

        # Stopword removal and remove non-alphabetic characters
        stop_words = set(stopwords.words('english'))
        tokens = [re.sub(r'[^a-zA-Z]', '', token).lower() for token in tokens if token.lower() not in stop_words]

        # Remove empty tokens
        tokens = [token for token in tokens if token]

        return tokens

    def generate_response(self, user_input):
        max_similarity = 0
        best_response = None
        try:
            for entry in self.conversations:
                question = entry["question"]
                question_tokens = self.preprocess_text(question)
                user_input_tokens = self.preprocess_text(user_input)
                common_tokens = set(question_tokens) & set(user_input_tokens)

                # Check for division by zero
                if len(question_tokens) == 0 or len(user_input_tokens) == 0:
                    similarity = 0
                else:
                    similarity = len(common_tokens) / max(len(question_tokens), len(user_input_tokens))

                if similarity > max_similarity:
                    max_similarity = similarity
                    best_response = entry.get("answers", ["I'm sorry, I don't have a response for that."])

            if best_response:
                return random.choice(best_response)
            else:
                return "I'm sorry, I didn't understand your question."

        except BaseException as e:
            return f"Error: {e}"

    def speak(self, text):
        self.engine.say(text)
        self.engine.runAndWait()

    def load_users(self):
        try:
            with open("users.json", 'r') as file:
                self.users = json.load(file)
        except FileNotFoundError:
            pass

    def save_users(self):
        with open("users.json", 'w') as file:
            json.dump(self.users, file, indent=4)

    def is_admin(self, username):
        if username in self.users:
            return self.users[username].get('is_admin', False)
        return False

    def edit_username(self, username, new_name):
        if username in self.users:
            self.users[username]['username'] = new_name
            self.save_users()
            print(f"Username for {username} has been changed to {new_name}.")
        else:
            print("User not found.")

    def manage_chats(self, username):
        if self.is_admin(username):
            # Access all chat logs or perform other admin actions
            print("Admin access granted. You can manage chats here.")
        else:
            print("You do not have permission to manage chats.")

    def load_chat_logs(self, username):
        chat_log_file = os.path.join("chat_logs", f"{username}.json")
        if os.path.exists(chat_log_file):
            with open(chat_log_file, 'r') as file:
                try:
                    return json.load(file)
                except json.decoder.JSONDecodeError:
                    return []
        else:
            return []



    def save_chat_log(self, username, chat_log):
        chat_log_file = os.path.join("chat_logs", f"{username}.json")
        with open(chat_log_file, 'w') as file:
            json.dump(chat_log, file, indent=4)

    def view_chat(self, username):
        chat_log_file = os.path.join("chat_logs", f"{username}.json")
        if os.path.exists(chat_log_file):
            with open(chat_log_file, 'r') as file:
                chat_log = json.load(file)
                print(f"Chat log for {username}:")
                for entry in chat_log:
                    print(f"User: {entry['user']}")
                    print(f"Bot: {entry['bot']}")
                    print("-" * 20)
        else:
            print(f"No chat log found for {username}.")

    def process_input(self, user_input):
        user_input_lower = user_input.lower()
        if user_input_lower == "login":
            self.login()
        elif user_input_lower == "signup":
            self.signup()
        elif user_input_lower == "what's my name?":
            print(f"Your name is {self.get_user_name()}.")
        elif user_input_lower.startswith("change my name to "):
            new_name = user_input[17:].strip()
            self.edit_username(self.current_user, new_name)
        elif user_input_lower.startswith("view chat log for "):
            username = user_input[18:].strip()
            if self.is_admin(self.current_user):
                self.view_chat(username)
            else:
                print("You do not have permission to view chats.")
        else:
            bot_response = self.generate_response(user_input)
            print(f"{self.name}: {bot_response}")
            self.speak(bot_response)
            if self.current_user:
                chat_log = self.load_chat_logs(self.current_user)
                chat_log.append({'user': user_input, 'bot': bot_response})
                self.save_chat_log(self.current_user, chat_log)

    def login(self):
        username = input("Username: ")
        password = input("Password: ")
        password_hash = hashlib.sha256(password.encode()).hexdigest()

        if username in self.users and self.users[username]['password'] == password_hash:
            print(f"Welcome back, {username}!")
            self.current_user = username
        else:
            print("Invalid username or password.")

    def signup(self):
        username = input("Choose a username: ")
        password = input("Choose a password: ")
        password_hash = hashlib.sha256(password.encode()).hexdigest()

        if username not in self.users:
            self.users[username] = {'password': password_hash}
            self.save_users()
            print(f"Account created successfully for {username}.")
        else:
            print("Username already exists. Please choose another one.")

    def load_conversations(self, file_path):
        with open(file_path, 'r') as file:
            return json.load(file)


bot = Bot(name="JZ")
bot.load_users()

try:
    while True:
        if not bot.current_user:
            user_choice = input("Do you want to (login) or (signup)? ")
            if user_choice.lower() == "login":
                bot.login()
            elif user_choice.lower() == "signup":
                bot.signup()
            else:
                print("Invalid choice. Please enter 'login' or 'signup'.")
                continue

        user_input = input(f"{bot.current_user if bot.current_user else 'You'}: ")
        if user_input.lower() == 'exit':
            break
        else:
            bot.process_input(user_input)
except KeyboardInterrupt:
    print("\nExiting...")
finally:
    bot.engine.stop()