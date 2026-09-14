import os
import random

import fluxer

from dotenv import load_dotenv

import keep_alive

load_dotenv()

bot = fluxer.Bot(command_prefix="!", intents=fluxer.Intents.all())

@bot.event
async def on_ready():
    print(f"Bot is online! Logged in as {bot.user.username}")

# Commands
@bot.command()
async def naiseyhelp(ctx):
    await ctx.reply("These are the commands you can use:\n\n"
                    "!naiseyhelp # Sends this help message\n\n"
                    "!hug (user) # Sends a hug to the mentioned user by you :3\n\n"
                    "!permahug (user) # Sends a permanent hug to the mentioned user by you ^w^\n\n"
                    "!praise (user) # Praises the mentioned user\n\n"
                    "(That's it for right now, other commands will be added in the future enjoy! :3)")

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

@bot.command()
async def praise(ctx, *, who: str = None):
    user = ctx.author.mention

    target = who

    praise_messages = \
        [
            f"Hehe ^^\n{target} is such a cutie! ^^",
            f"Awwwww :3\n{target} is soooo cute! :33 ",
            f"{target}! you are so adorable! :3 ",
            f"{target}! you are sooo awesome! :3 ",
            f"Awwwww! :3 isn't {target} sooooo cute? ^?^",
            f"{target} is so cute! :3 >w<",
            f"{target} is so cute that I can hug them endlessly! ^w^",
            f"{target} is such a cutie patooti :3 ^~^"
        ]

    choice = random.choice(praise_messages)

    if who == user:
        await ctx.reply("You can't just do that!")
    elif who:
        await ctx.reply(choice)
    else:
        await ctx.reply("Mention a user or write someones name")

@bot.command()
async def permahug(ctx, *, who: str = None):
    user = ctx.author.mention

    target = who

    hug_messages = \
    [
        f"{user} permanently hugs {target} 🫂",
        f"{user} hugs {target} permanently 🫂",
        f"{user} hugs {target} and they won't let go, ever 🫂🫂",
        f"{user} hugs {target} and never let's go until the end of time and beyond 🫂",
        f"{user} has trapped {target} with an eternal hug 🫂"
    ]

    choice = random.choice(hug_messages)

    if who == user:
        await ctx.reply(f"{user} gave themselves a permanent hug 🫂🥺")
    elif who:
        await ctx.reply(choice)
    else:
        await ctx.reply(f"{user} gave themselves a permanent hug 🫂🥺")

keep_alive.keep_alive()

# 4. Run the bot using your Fluxer token
if __name__ == "__main__":
    TOKEN = os.getenv('TOKEN')
    bot.run(TOKEN)