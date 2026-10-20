It's a silly little fluxer bot for silly little things like hugging, cuddling, petting etc.
[Invite it from here](https://web.fluxer.app/oauth2/authorize?client_id=1548951710439833600&scope=bot&permissions=116736)

Privacy policy: [PRIVACY.md](PRIVACY.md)

## Deploying

This bot runs on [HeavenCloud](https://heavencloud.in), free 24/7 Discord/Fluxer bot hosting with no credit card required. The database runs on [Neon](https://console.neon.tech), a permanent free Postgres host.

### 1. Fork this repo
- Fork this repository to your own GitHub account

### 2. Create a Neon database
- Go to console.neon.tech and sign up
- Create a new project
- Copy the connection string it gives you — looks like:
  postgresql://user:password@ep-xxxx.region.aws.neon.tech/dbname?sslmode=require

### 3. Join the Discord and claim a free server
- Join HeavenCloud's Discord: https://discord.gg/getvps
- Follow their bot's instructions to claim your free bot-hosting server

### 4. Configure the Startup tab
In your server's panel, go to Startup and set:

| Variable | Value |
|---|---|
| Git Repo Address | https://github.com/YOUR_USERNAME/fluxer_naisey_bot |
| Git Branch | (leave blank to use the default branch) |
| User Uploaded Files | False |
| Auto Update | True |
| App.py File | bot.py |
| Additional Python Packages | (leave blank) |
| Git Username | (your GitHub username, only needed if the repo is private) |
| Git Access Token | (a GitHub personal access token, only needed if the repo is private) |
| Requirements File | requirements.txt |

Docker Image: Python 3.13

### 5. Upload a .env file
In the server's panel, go to Files and create a .env file with:

TOKEN=your_fluxer_bot_token
DATABASE_URL=your_neon_connection_string

### 6. Start the server
Click Start on the server dashboard. With Auto Update on, it'll pull the repo and install dependencies automatically.

### Running locally instead

pip install -r requirements.txt

Create a .env file:

TOKEN=your_bot_token
TOKEN2=your_debug_bot_token (only if you're debugging)
DATABASE_URL=your_neon_connection_string

Then:

python bot.py