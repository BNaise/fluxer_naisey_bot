import os
import random

import fluxer

from dotenv import load_dotenv

load_dotenv()

# 1. Initialize the bot with a command prefix and default intents
bot = fluxer.Bot(command_prefix="!", intents=fluxer.Intents.default())
# 2. Event listener for when the bot successfully logs in

@bot.event
async def on_ready():
    print(f"Bot is online! Logged in as {bot.user.username}")

# 3. Simple text command
@bot.command()
async def ping(ctx):
    await ctx.reply("Pong!")

@bot.command()
async def test(ctx):
    await ctx.reply("Test!")

@bot.command()
async def echo(ctx, *, message: str):
    await ctx.reply(message)

@bot.command()
async def hug(ctx, *, who: str = None):
    user = ctx.author.mention
    target = who

    hug_messages = \
    [
        f"{user} tightly hugs {target} 🫂",
        f"{target} got absolutely loved and hugged by {user} 🫂",
        f"{user} hugs {target} so much that they won't let go 🫂",
        f"Hey {target}! {user} just sent you a ton of hugs! ^^ 🤗",
        f"{user} gives {target} a big warm hug! 🤗",
        f"{user} wraps their arms around {target}! 🫂",
        f"{user} gives {target} a much-needed hug! 🫂",
        f"{user} hugs {target} with all their might! 🫂",
        f"{user} pulls {target} into a cozy hug! 🤗",
        f"{user} gives {target} a wholesome hug! 🤗🫂",
        f"{user} hugs {target}. Awwww! 🤗",
        f"{user} has hugged {target}. They are now legally required to be happy. 🤗",
        f"HUG DETECTED! {user} has hugged {target}! 🤗",
        f"{user} launches themselves at {target} with a hug! 🤗🫂",
        f"{user} and {target} are temporarily trapped in a hug. 🤗",
        f"{user} sends a hug directly to {target}'s soul. 🤗🫂",
        f"{user} hugs {target}. No escape. 🫂"
    ]

    choice = random.choice(hug_messages)
    if who == user:
        await ctx.reply(f"{user} gave themselves a hug 🫂🥺")
    elif who:
        await ctx.reply(choice)
    else:
        await ctx.reply(f"{user} gave themselves a hug 🫂🥺")

# 4. Run the bot using your Fluxer token
if __name__ == "__main__":
    # Replace with your actual Fluxer bot token
    TOKEN = os.getenv('TOKEN')
    bot.run(TOKEN)
