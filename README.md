# Telegram Admin Bot

This is a Telegram bot designed to help administrators manage their Telegram groups or channels efficiently. The bot provides various administrative tools, such as user management, automated responses, scheduled messages, and more.

## Features

- **User Management**: Kick, ban, or mute users from the group.
- **Job Scheduling**: Run periodic tasks using the built-in job queue.

## Getting Started

### Prerequisites

- **Python 3.11.9+**
- **Poetry**: A dependency manager for Python.

### Installation

1. **Clone the repository**:

    ```bash
    git clone git@github.com:itanc-com/itelebot.git
    cd TeleBot
    ```

2. **Install Poetry**:

    If you don't have Poetry installed, you can install it via the following command:

    ```bash
    curl -sSL https://install.python-poetry.org | python3 -
    ```

    Or via pipx:

    ```bash
    pipx install poetry
    ```

3. **Activate the virtual environment**:

    Activate the virtual environment created by Poetry:

    ```bash
    poetry shell
    ```

4. **Install dependencies**:

    Use Poetry to install the project dependencies:

    ```bash
    poetry install
    ```

5. **Set up environment variables**:

    Create a env folder in that folder create `.env` file in the root directory and add your Telegram bot token and other configuration settings:

    ```env
    TOKEN=your-telegram-bot-token
    BOT_USERNAME="@your bot user name "
    CHAT_ID="-xxxxxx"
    POOL_SIZE =x
    TIMEOUT=x
    RATE_LIMIT_REQUESTS=xx
    RATE_LIMIT_PERIOD=x
    ```

    Replace `your-telegram-bot-token` and `your bot username` with the actual token provided by the BotFather.

6. **Run the bot**:

    Start the bot by running the main script:

    ```bash
    python3 main.py
    ```
