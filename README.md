It's a silly little fluxer bot for silly little things like hugging, cuddling, petting etc.
[Invite it from here](https://web.canary.fluxer.app/oauth2/authorize?client_id=1548951710439833600&scope=bot&permissions=247880)

Privacy policy: [PRIVACY.md](PRIVACY.md)

## Deploying

This bot is built to run on [Render](https://render.com) (free tier works fine, with the usual caveat that free instances spin down after inactivity and take ~50s to wake back up, I recommend setting up uptimerobot for that which pings it every 5 minutes or so). The database runs on [Neon](https://console.neon.tech), a permanent free Postgres host.

### 1. Fork/clone this repo

### 2. Create a Neon database
- Go to console.neon.tech and sign up
- Create a new project
- Copy the connection string it gives you — looks like:
  postgresql://user:password@ep-xxxx.region.aws.neon.tech/dbname?sslmode=require

### 3. Create a Web Service on Render
- **New → Web Service**, connect this repo
- **Build Command:** `pip install -r requirements.txt`
- **Start Command:** `python bot.py`

### 4. Set environment variables
In the service's **Environment** tab:
| Key | Value |
|---|---|
| `TOKEN` | Your Fluxer bot token |
| `DATABASE_URL` | The Postgres URL from step 2 |

### 5. Deploy
Render will auto-build and start the bot. Check the **Logs** tab for:
Bot is online! Logged in as <your bot's username>

### Running locally instead

pip install -r requirements.txt

Create a `.env` file:

TOKEN=your_bot_token

TOKEN2=your_debug_bot_token (only if you're debugging)

DATABASE_URL=your_postgres_url (Put external link to debug locally)

Then:
python bot.py
