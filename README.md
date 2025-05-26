
Built by https://www.blackbox.ai

---

# Blacklist Bot

## Project Overview
The Blacklist Bot is a Discord bot designed to manage a blacklist of users across multiple Discord servers. This bot allows server moderators to blacklist users, view blacklist entries, and manage cases for those blacklisted. It includes features like support for trusted moderators, webhooks for notifications, and a dashboard for monitoring activity.

## Features
- **Blacklist Management**: Add or remove users from a blacklist.
- **Case Management**: Create, view, and update cases related to user actions.
- **Trusted Moderators**: Designate certain users as trusted moderators with specific permissions.
- **Webhook Support**: Send notifications for various actions to specified webhook URLs.
- **Anti-Evasion System**: Automatically ban blacklisted users who attempt to rejoin.
- **Dashboard**: A web dashboard to view statistics, recent activity, and manage blacklist entries.

## Installation
To run the Blacklist Bot, ensure you have Python 3.8 or higher installed. You will also need MongoDB for data storage. After cloning this repository, you can install the required dependencies by running:

```bash
pip install -r requirements.txt
```

### Configuration
1. **MongoDB Setup**: Create a MongoDB cluster and obtain your connection string.
2. **Create `config.json`**: Create a `config.json` file in the project root with the following example structure:

```json
{
    "token": "<YOUR_DISCORD_BOT_TOKEN>",
    "mongodb_uri": "<YOUR_MONGODB_URI>",
    "allowed_role_ids": [<ROLE_IDS>],
    "developer_ids": [<DEVELOPER_IDS>],
    "prefix": "+",
    "log_channel": null,
    "appeal_channel": null,
    "anti_evasion": true,
    "dashboard": {
        "secret": "your-secret-key-change-this",
        "port": 8000,
        "allowed_ips": []
    }
}
```

Replace the placeholders with your actual data. 

## Usage
1. Start the bot by running:

```bash
python bot.py
```

2. Access the dashboard via: [http://localhost:8000](http://localhost:8000) after starting the bot.

3. Use commands via Discord:
   - `+blacklist <user_id> [reason]`: Add a user to the blacklist.
   - `+unblacklist <user_id>`: Remove a user from the blacklist.
   - `+checkblacklist <user_id>`: Check if a user is blacklisted.
   - `+blacklistview`: View all blacklisted users.
   - `+case create <case_id> [notes]`: Create a new case.

## Dependencies
The following dependencies are required for the project (found in `requirements.txt`):

```plaintext
discord.py
pymongo
quart
aiohttp
```

Make sure you install all of them before running the bot.

## Project Structure
```plaintext
.
├── bot.py                      # Main bot file where the Discord bot runs.
├── config.json                 # Configuration file for Discord token & MongoDB URI.
├── dashboard.py                # Dashboard web server implemented with Quart.
└── requirements.txt            # Python dependencies.
```

### Notable Files
- **`bot.py`**: Contains the main bot logic, command handling, database management, and background tasks for syncing blacklist data.
- **`dashboard.py`**: Provides a web dashboard using Quart for monitoring and managing blacklist activities.
- **`config.json`**: JSON file for configuration settings such as bot token, database connection details, and dashboard settings.

## Contributing
Contributions are welcome! Please submit an issue or a pull request if you would like to contribute to the project.

## License
This project is licensed under the MIT License. See the LICENSE file for more details.