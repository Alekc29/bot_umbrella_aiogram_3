import os

from dotenv import load_dotenv

load_dotenv()

API_KEY_WEATHER = os.getenv('API_KEY_WEATHER')
BOT_TOKEN = os.getenv('BOT_TOKEN')
DEV_ID = int(os.getenv('DEV_ID'))
BASE = str(os.getenv('BASE_NAME'))
