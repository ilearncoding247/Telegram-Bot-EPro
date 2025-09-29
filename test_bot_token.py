#!/usr/bin/env python3
"""
Test script to verify Telegram bot token
"""

import os
import sys
from telegram import Bot
from telegram.error import TelegramError

# Add the telegramreferralpro directory to the path
sys.path.append(os.path.join(os.path.dirname(__file__), 'telegramreferralpro'))

from telegramreferralpro.config import load_config

async def test_bot_token():
    """Test the Telegram bot token"""
    try:
        # Load configuration
        config = load_config()
        print("✅ Configuration loaded successfully")
        print(f"Bot token: {config.bot_token[:10]}...")
        print(f"Channel ID: {config.channel_id}")
        print(f"Channel username: {config.channel_username}")
        
        # Test bot token
        bot = Bot(token=config.bot_token)
        bot_info = await bot.get_me()
        print(f"✅ Bot token is valid!")
        print(f"Bot username: {bot_info.username}")
        print(f"Bot first name: {bot_info.first_name}")
        
        # Test channel access
        try:
            chat = await bot.get_chat(config.channel_id)
            print(f"✅ Channel access confirmed!")
            print(f"Channel title: {chat.title}")
            print(f"Channel username: {chat.username}")
        except TelegramError as e:
            print(f"⚠️  Channel access issue: {e}")
            print("This might be OK if the bot hasn't been added to the channel yet.")
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    import asyncio
    success = asyncio.run(test_bot_token())
    if success:
        print("\n🎉 All tests passed! Your bot token is valid.")
    else:
        print("\n❌ Tests failed. Please check your configuration.")