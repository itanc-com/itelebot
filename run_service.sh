#!/bin/bash

# Navigate to the directory where your Telegram bot code is located
cd  /root/TeleBot
# Pull the latest changes from the main branch
git pull origin main

# Restart your bot's systemd service
sudo systemctl restart  telegrambot.service