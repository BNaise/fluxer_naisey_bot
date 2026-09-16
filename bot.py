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

    embed = fluxer.Embed(
        title="Naisey's commands",
        description="Here's everything I can do right now :P",
        color=0x52F0EF
    )
    embed.add_field(name="!naiseyhelp", value="Sends this help message", inline=False)
    embed.add_field(name="!hug (user)", value="Sends a hug to the mentioned user by you :3", inline=False)
    embed.add_field(name="!permahug (user)", value="Sends a permanent hug to the mentioned user by you ^w^", inline=False)
    embed.add_field(name="!praise (user)", value="Praises the mentioned user", inline=False)

    embed.set_footer(text="(That's it for right now, other commands will be added in the future enjoy! :3)")

    # await ctx.reply("These are the commands you can use:\n\n"
    #                 "!naiseyhelp # Sends this help message\n\n"
    #                 "!hug (user) # Sends a hug to the mentioned user by you :3\n\n"
    #                 "!permahug (user) # Sends a permanent hug to the mentioned user by you ^w^\n\n"
    #                 "!praise (user) # Praises the mentioned user\n\n"
    #                 "(That's it for right now, other commands will be added in the future enjoy! :3)")

    await ctx.reply(embed=embed)

@bot.command()
async def hug(ctx, *, who: str = None):
    user = ctx.author.mention

    target = who

    # if who in ("@everyone", "@here"):
    #     await ctx.reply("You can't just do that!")
    #     return

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

    # if who in ("@everyone", "@here"):
    #     await ctx.reply("You can't just do that!")
    #     return

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

    # if who in ("@everyone", "@here"):
    #     await ctx.reply("You can't just do that!")
    #     return

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

@bot.command()
async def silly(ctx, *, who: str = None):
    user = ctx.author.mention

    target = who

    if not who:
        messages = \
            [
              "Bleh",
              "Meow :3",
              "Mrewwww :3",
              "Nyaaaaa~",
              "Nyon!",
              "Ueueleuleuleue!"
            ]
    else:
        messages = \
            [
              f"Ummmm {target}! {user} is purring at you ^w^",
              f"Hehe {target}! {user} is meowing at you :3 ",
              f"{user} is meowing at {target}! ~ ^w^ ~",
              f"{target} is getting nuzzled by {user} ^^",
              f"{user} is gently patting {target}'s head :3",
              f"{target}! {user} tackles you with a hug :3"
            ]

    choice = random.choice(messages)

    await ctx.reply(choice)

@bot.command()
async def deltarot(ctx):

    messages = \
        [
            "JARONA!",
            "Freedom’s just a penumbra phantasm for big shots with black knives about the world revolving around the hammer of justice sealed away with cutie mew mew magic at the pirate dojo in my castle town during the sunset of seven suns.",
            "FREEDOM",
            "FRIEND",
            "GASTER",
            "PENUMBRA PHANTASM",
            "Friend inside me!",
            "BIG SHOT",
            "Papyrus is the roaring knight trust",
            "Always bet on papyrus knight!",
            "DECEMBER",
            "Yeah... the WORLD is kinda REVOLVING...",
            "Mike...",
            "1997",
            "1225",
            "Rip Onion :'(",
            "HERE I COME SANFRANDISCOOOOOOOO!",
            "SUSTINGUS",
            "Hey guys, I think I found a glue!",
            "Mysterious wind",
            "Hey i think this kinda took a weird route.",
            "Human... I remember... You're genocides...",
            "Hey undyne!\nHow many human souls do we need to break the barrier?",
            f"CHAOS CHAOS!"
        ]

    choice = random.choice(messages)

    if choice == "Hey undyne!\nHow many human souls do we need to break the barrier?":
        file = fluxer.File("files/undyne-seven.webp")
        await ctx.reply(choice, file=file)
    else:
        await ctx.reply(choice)

@bot.command()
async def gamble(ctx):

    messages = ["Aww dang it!",
                "I can't stop winning!"]

    await ctx.reply(random.choice(messages))

@bot.command()
async def roll(ctx, finish: int = None, start: int = 1):

    if finish:
        if finish >= start:
            random_number = random.randint(start, finish)
            await ctx.reply(str(random_number))
        elif finish < start:
            await ctx.reply("Finishing number should be bigger then starting number.")
    else:
        await ctx.reply("Please enter a number")

@bot.command()
async def kiss(ctx, *, who: str = None):
    user = ctx.author.mention

    target = who

    hug_messages = \
    [
        f"{user} kissed {target}! They're so cute!",
        f"OMG- GUYS- {user} JUST KISSED {target}!!!!",
        f"{user} **VIOLENTLY** pulled {target} to them and **SMOOCHED** them on the **LIPS**, not letting **ANYONE ELSE** in",
        f"Hehehehe, {user} gave {target} a little smooooch!"
    ]

    choice = random.choice(hug_messages)

    if who == user:
        await ctx.reply(f"{user} kissed themselves? ...how?")
    elif who:
        await ctx.reply(choice)
    else:
        await ctx.reply(f"{user} kissed themselves? ...how?")

keep_alive.keep_alive()

# 4. Run the bot using your Fluxer token
if __name__ == "__main__":
    TOKEN = os.getenv('TOKEN')
    bot.run(TOKEN)