import os

from dotenv import load_dotenv

# Load environment variables from a .env file
load_dotenv()

# Get the Telegram token from the environment variables
# This token is used to authenticate the bot with the Telegram API
TOKEN_TELEGRAM = os.getenv("TOKEN_TELEGRAM")

# Get the MongoDB connection URL from the environment variables
# This URL is used to connect to the MongoDB database
MONGO_URL = os.getenv("MONGO_URL")