# 🚀 Deploying the Bot to Render

This guide explains how to deploy your Telegram Referral Bot to Render for 24/7 hosting, ensuring your SQLite database persists across restarts using a Render Disk.

## 📋 File-Based Configuration

Your project is already configured for Render using the following files:

### 1. `requirements.txt`
This file lists the Python dependencies for Render to install.

### 2. `render.yaml`
This "Infrastructure as Code" file tells Render exactly how to build and run your service. Here is its content:

```yaml
# render.yaml
# This file tells Render how to build and run your Telegram bot.

services:
  - type: web # 'web' type is used for long-running services, even non-HTTP ones.
    name: telegram-referral-bot
    env: python
    plan: free # Or 'starter' for better performance
    
    # A persistent disk to store the SQLite database.
    # The data will persist across deploys and restarts.
    disks:
      - name: bot-data
        mountPath: /var/data
        sizeGB: 1 # 1 GB is the smallest size and plenty for a SQLite DB.

    # Commands to run on build.
    buildCommand: "pip install -r requirements.txt"

    # Command to start the bot. Using the recommended simple runner.
    startCommand: "python run_bot_simple.py"

    # Environment variables can be set in the Render dashboard.
    # We will set DATABASE_PATH to point to our persistent disk.
```

---

## ⚙️ Deployment Steps on Render

1.  **Sign Up & Connect GitHub**:
    *   Go to dashboard.render.com and create an account.
    *   Connect your GitHub account where your bot's code is stored.

2.  **Create a New "Blueprint" Service**:
    *   On the dashboard, click **New +** and select **Blueprint**.
    *   Select the repository for your bot. Render will automatically detect and use the `render.yaml` file.

3.  **Approve the Plan**:
    *   Render will show you the service defined in `render.yaml` (`telegram-referral-bot`).
    *   Click **Approve** to confirm. The initial deployment will start but will likely fail until you set the environment variables.

4.  **Add Your Environment Variables**:
    *   After the service is created, go to its **Environment** tab.
    *   Add all the variables from your `.env` file (`BOT_TOKEN`, `CHANNEL_ID`, etc.).
    *   **Crucially, add the `DATABASE_PATH` variable to use the persistent disk**:
        *   **Key**: `DATABASE_PATH`
        *   **Value**: `/var/data/bot_database.db`

5.  **Deploy Manually**:
    *   Go to the top of your service page and click **Manual Deploy** > **Deploy latest commit**.
    *   Render will now build and launch your service with the correct environment variables. Your bot will be live and running 24/7!


    Run the initialization script after the database structure exists:
python initialize_referral_data.py