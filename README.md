# Telegram Admin Bot

This is a Telegram bot designed to help administrators manage their Telegram groups or channels efficiently. The bot provides various administrative tools, such as user management, automated responses, scheduled messages, and more.

## Features

- **User Management**: Kick, ban, or mute users from the group.
- **Job Scheduling**: Run periodic tasks using the built-in job queue.

## Getting Started

### Prerequisites

- **Python 3.11.9+**
- **uv**: A dependency manager for Python.

### Installation

1. **Clone the repository**:

    ```bash
    git clone git@github.com:itanc-com/itelebot.git
    cd itelebot
    ```

2. **Install uv**:

    If you don't have uv installed, you can install it via the following command:

    ```bash
    curl -LsSf https://astral.sh/uv/install.sh | sh
    ```

    Or via pipx:

    ```bash
    pipx install uv
    ```

3. **Create the virtual environment**:

    Create virtual environment by uv:

    ```bash
    uv sync
    ```

    ```bash
    source .venv/bin/activate
    ```

4. **Set up environment variables**:

    Create a env folder in that folder create `.env` file in the root directory and add your Telegram bot token and other configuration settings:

    ```env
    TOKEN=your-telegram-bot-token
    BOT_USERNAME="@your bot username "
    CHAT_ID="-xxxxxx"
    POOL_SIZE =x
    TIMEOUT=x
    RATE_LIMIT_REQUESTS=xx
    RATE_LIMIT_PERIOD=x
    ```

    Replace `your-telegram-bot-token` and `your bot username` with the actual token provided by the BotFather.

5. **Run the bot**:

    Start the bot by running the main script:

    ```bash
    python3 main.py
    ```
