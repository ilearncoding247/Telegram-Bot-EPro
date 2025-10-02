## Quick Start: Telegram-Bot-EPro

### ✅ Current Status
- **API Server**: Running on http://localhost:8080 ✅
- **Bot Token**: Valid (@eprobot_bot) ✅
- **Referral API**: Working (tested with user_id=123456789) ✅

### Required environment variables
Set these before running the bot (PowerShell shown). Open a new terminal after setting.

```
setx BOT_TOKEN "<your_token>"
setx CHANNEL_ID "-100xxxxxxxxxx"
setx CHANNEL_USERNAME "YourChannelUsername"
setx ADMIN_USER_IDS "123456789,987654321"
```

Optional (Supabase + integration):
```
setx SUPABASE_URL "https://<project-ref>.supabase.co"
setx SUPABASE_KEY "<service_or_anon_key>"
setx SUPABASE_WEBHOOK_URL "https://<project-ref>.functions.supabase.co/telegram-task-update"
setx SUPABASE_WEBHOOK_SECRET "<same-secret-as-in-edge-function>"
```

Vite frontend base (if applicable):
```
VITE_TG_BOT_API_BASE=http://localhost:8080   # development
# or
VITE_TG_BOT_API_BASE=https://api.earnpro.org  # production
```

### Start the bot (polling)
```
python -m telegramreferralpro.main
```

### Start the referral API (for frontend)
```
python api_server.py
# Test
curl "http://localhost:8080/api/health"
```

### Webhook mode (optional)
```
setx WEBHOOK_URL "https://your-domain.example.com/<bot_token>"
setx PORT "8000"
python -m telegramreferralpro.main
```

### Supabase Edge Function secret
- Set in Supabase: `TELEGRAM_WEBHOOK_SECRET`
- Set in bot env: `SUPABASE_WEBHOOK_SECRET`
- Values must match.

### Notes
- Restart terminal after `setx`.
- Never commit secrets.

