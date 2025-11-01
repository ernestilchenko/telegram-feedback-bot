# Telegram Feedback Bot

<div align="center">
  <img src="https://telegram.org/img/t_logo.png" alt="Telegram Logo" width="120"/>
  
  A multi-language Telegram bot for collecting user feedback and forwarding it to administrators
  
  [![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://www.python.org/downloads/)
  [![aiogram](https://img.shields.io/badge/aiogram-3.x-blue.svg)](https://docs.aiogram.dev/)
  [![MongoDB](https://img.shields.io/badge/MongoDB-4.4+-green.svg)](https://www.mongodb.com/)
  [![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
</div>

## Features

- **User Feedback Collection**: Users can send text messages and media files to the bot
- **Admin Management**: Administrators receive all user messages with user ID tracking
- **Reply System**: Admins can reply directly to user messages
- **Ban System**: Block and unblock users from sending messages
- **Multi-language Support**: Built-in localization for English, Russian, Ukrainian, and Polish
- **Media Support**: Supports photos, videos, audio, documents, animations, and voice messages
- **User Information Lookup**: Get detailed user information by replying to their messages

## Tech Stack

- **aiogram 3.x**: Modern and async Telegram Bot framework
- **MongoDB**: Database for storing users, admins, and banned users
- **Fluent**: Localization system for multi-language support
- **Python 3.9+**: Modern Python with async/await support

## Prerequisites

- Python 3.9 or higher
- MongoDB instance
- Telegram Bot Token from [@BotFather](https://t.me/BotFather)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/ernestilchenko/telegram-feedback-bot.git
cd telegram-feedback-bot
```

2. Create a virtual environment and activate it:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create a `.env` file in the root directory:
```env
TOKEN_TELEGRAM=your_bot_token_here
MONGO_URL=mongodb://localhost:27017/
```

5. Add your admin user ID to MongoDB:
```python
# You can add this manually or create a script
# The bot will need at least one admin to function properly
```

## Usage

Start the bot:
```bash
python bot.py
```

### User Commands

- `/start` - Initialize the bot and start sending feedback

### Admin Commands

- `/who` - Reply to a user message to get their information (name, ID, username)
- `/users` - Get a list of all registered users
- `/ban` - Reply to a user message to ban them
- `/unban` - Reply to a user message to unban them
- **Reply to any message** - Send a reply directly to the user

## Project Structure

```
telegram-feedback-bot/
├── bot/
│   ├── admin/              # Admin command handlers
│   │   ├── admin_mode.py   # User info and list commands
│   │   └── bans.py         # Ban/unban and reply functionality
│   ├── filters/            # Custom filters
│   │   ├── admin.py        # Admin permission filter
│   │   └── supported_media.py  # Media type filter
│   ├── handlers/           # Message handlers
│   │   └── usermode.py     # User message handlers
│   ├── locales/            # Translation files
│   │   ├── en/            # English translations
│   │   ├── ru/            # Russian translations
│   │   ├── uk/            # Ukrainian translations
│   │   └── pl/            # Polish translations
│   ├── middlewares/        # Bot middlewares
│   │   └── I10n.py        # Localization middleware
│   └── utils/              # Utility functions
│       ├── fluent_helper.py  # Localization helper
│       └── utils.py        # Common utilities
├── db/
│   └── base.py            # Database operations
├── bot.py                 # Main bot entry point
└── config.py              # Configuration loader
```

## Localization

The bot supports multiple languages out of the box. The language is automatically detected based on the user's Telegram language settings. Supported languages:

- English (en) - Default
- Russian (ru)
- Ukrainian (uk)
- Polish (pl)

To add a new language, create a new directory in `bot/locales/` with the language code and add `strings.ftl` and `errors.ftl` files.

## Database Schema

### Collections

- **users**: Registered users
- **admin**: Administrator user IDs
- **ban**: Banned user IDs

Each document contains a `user_id` field with the Telegram user ID.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

If you encounter any issues or have questions, please open an issue on GitHub.