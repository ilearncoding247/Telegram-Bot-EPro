# Group Join Feature - Setup Guide

## Overview

This bot now supports a **two-step join flow**:
1. User joins the **Channel**
2. Bot asks them to join the **Group**
3. Once they join the **Group**, bot sends them their referral link

This creates a better user experience and engagement flow.

---

## How It Works

### Flow Diagram

```
User joins Channel
        ↓
Bot sends DM asking to join Group
        ↓
User joins Group
        ↓
Bot automatically sends Referral Link & Welcome Message
```

---

## Configuration

To enable this feature, add these environment variables to your `.env` file:

```env
# Group Configuration
GROUP_ID=-1003802752780              # Your group's numeric ID
GROUP_USERNAME=your_group_username   # Your group's username (without @)
```

### Finding Your Group Information

#### 1. Get Your Group ID
- Open your group in Telegram
- Use a bot like [@userinfobot](https://t.me/userinfobot)
- Forward a message from the group to the bot
- It will provide your group's ID
- **Important:** Add `-100` prefix to the ID (e.g., `-1001234567890`)

#### 2. Get Your Group Username
- Open your group settings
- Go to "Manage group"
- Look for the public username (without the `@` symbol)
- Example: if your group is `@mygroup`, use `mygroup` in the config

---

## Environment Variables

| Variable | Required | Example | Description |
|----------|----------|---------|-------------|
| `GROUP_ID` | Optional | `-1003802752780` | Numeric group ID (with -100 prefix) |
| `GROUP_USERNAME` | Optional | `mygroup` | Group username without @ symbol |

---

## What Happens

### When Group is Configured ✅
1. User joins the **Channel**
2. Bot sends them a DM:
   ```
   ✅ Welcome to our channel!
   
   👥 **Next Step:** Please join our group to get started!
   
   [Join our group: mygroup](https://t.me/mygroup)
   
   Once you join the group, I'll send you your referral link and you can start earning rewards!
   ```
3. User clicks the link and joins the group
4. Bot detects they joined the group and automatically sends:
   ```
   ✅ Great! You've successfully joined [Channel Name]!
   
   Here's your unique referral link:
   [Referral Link]
   
   📋 **Your Mission:**
   Share this link with friends and get 5 people to join using your link to earn your reward!
   ```

### When Group is NOT Configured ❌
- Bot shows the referral link immediately after channel join
- Standard behavior (original flow)

---

## Important Notes

⚠️ **Remember to:**
- ✅ Add the bot as an admin to your group (at least with basic permissions)
- ✅ Set the GROUP_ID and GROUP_USERNAME in your .env file
- ✅ Test the flow with a test account before going live
- ✅ The group should be public (or the bot needs to be added directly)

---

## Troubleshooting

### 1. **Bot doesn't detect group joins**
   - Make sure bot is added to the group as an admin
   - Check that `GROUP_ID` matches exactly
   - Ensure `-100` prefix is included in the ID

### 2. **Group link not working**
   - Verify `GROUP_USERNAME` is correct (without @)
   - Check that group has a public username

### 3. **User never gets referral link**
   - Confirm bot is in the group's admin list
   - Check bot logs for errors
   - Test manually by joining the group

---

## Command Reference

All existing commands still work:

- `/start` - Register and get welcome message
- `/status` - Check referral progress
- `/claim` - Claim reward when target reached
- `/help` - Show help message
- `/language` - Change language
- `/admin_stats` - View bot statistics (admin only)

---

## Advanced: Disabling the Feature

To go back to the original flow (without group requirement):
- Simply remove or comment out `GROUP_ID` and `GROUP_USERNAME` from your `.env` file
- The bot will automatically switch to direct referral link delivery

---

Need help? Check the main [README.md](README.md) for more information!
