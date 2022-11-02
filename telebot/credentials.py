import os
from pathlib import Path
import dotenv

# base app directory
BASE_DIR = Path(__file__).resolve().parent.parent

# obtain evironment variables if the exist
BOT_TOKEN = os.getenv('MYCHATBOT_TOKEN')
BOT_USERNAME = os.getenv('MYCHATBOT_USERNAME')
BOT_URL = os.getenv('MYCHATBOT_URL')
REDIS_HOST = os.getenv('REDIS_HOST')
REDIS_DB = os.getenv('REDIS_DB')
REDIS_PORT = os.getenv('REDIS_PORT')
REDIS_PASSWORD = os.getenv('REDIS_PASSWORD')
VIDEO_URL = os.getenv('VIDEO_URL')
VIDEO_NAME = os.getenv('VIDEO_NAME')
TOTAL_FRAMES = os.getenv('TOTAL_FRAMES')

# read configuration file with variables
config = dotenv.dotenv_values(BASE_DIR / '.env')

BOT_TOKEN = config['MYCHATBOT_TOKEN'] if BOT_TOKEN is None else BOT_TOKEN
BOT_USERNAME = config['MYCHATBOT_USERNAME'] if BOT_USERNAME is None else BOT_USERNAME
BOT_URL = config['MYCHATBOT_URL'] if BOT_URL is None else BOT_URL
REDIS_HOST = config['REDIS_HOST'] if REDIS_HOST is None else REDIS_HOST
REDIS_DB = config['REDIS_DB'] if REDIS_DB is None else REDIS_DB
REDIS_PORT = config['REDIS_PORT'] if REDIS_PORT is None else REDIS_PORT
REDIS_PASSWORD = config['REDIS_PASSWORD'] if REDIS_PASSWORD is None else REDIS_PASSWORD
VIDEO_URL = config['VIDEO_URL'] if VIDEO_URL is None else VIDEO_URL
VIDEO_NAME = config['VIDEO_NAME'] if VIDEO_NAME is None else VIDEO_NAME
TOTAL_FRAMES = int(config['TOTAL_FRAMES']) if TOTAL_FRAMES is None else int(TOTAL_FRAMES)

AFFIRMATIVE = 'yes'
NEGATIVE = 'no'