import random
from datetime import datetime
import os

def generate_random_color():
    return f"#{random.randint(0, 255):02x}{random.randint(0, 255):02x}{random.randint(0, 255):02x}"

def create_log_file(room_name):
    if not os.path.exists("app/logs"):
        os.makedirs("app/logs")
    file = open(f"app/logs/{room_name}-log.txt", "w")
    file.close()

def log(room_name, username, message):
    file = open(f"app/logs/{room_name}-log.txt", "a")
    file.write(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {username}: {message}\n")
    file.close()