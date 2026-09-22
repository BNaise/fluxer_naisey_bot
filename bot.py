import os
import random
import io
import psycopg2

import aiohttp

import fluxer

from dotenv import load_dotenv

import funcs

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

debug = False
# debug = True

if not debug:
    funcs.init_db_start()

if not debug:
    bot = fluxer.Bot(command_prefix=funcs.get_bot_prefix, intents=fluxer.Intents.all())
else:
    bot = fluxer.Bot(command_prefix="!", intents=fluxer.Intents.all())

@bot.event
async def on_ready():
    print(f"Bot is online! Logged in as {bot.user.username}")

# Commands
@bot.command()
async def naiseyhelp(ctx):

    prefux = funcs.get_prefix(ctx.guild.id)

    embed = fluxer.Embed(
        title="Naisey's commands",
        description="Here's everything I can do right now :P",
        color=0x52F0EF
    )
    embed.add_field(name=f"{prefux}naiseyhelp", value="Sends this help message", inline=False)
    embed.add_field(name=f"{prefux}hug (user)", value="Sends a hug to the mentioned user by you :3", inline=False)
    embed.add_field(name=f"{prefux}permahug (user)", value="Sends a permanent hug to the mentioned user by you ^w^", inline=False)
    embed.add_field(name=f"{prefux}kiss (user)", value="Kiss the mentioned user", inline=False)
    embed.add_field(name=f"{prefux}cheekkiss (user)", value="Kiss the mentioned user on the cheek :3", inline=False)
    embed.add_field(name=f"{prefux}silly (user [optional])", value="Silly :P", inline=False)
    embed.add_field(name=f"{prefux}deltarot", value="Says Deltarots -_-", inline=False)
    embed.add_field(name=f"{prefux}gamble", value="Let's go gambling!!", inline=False)
    embed.add_field(name=f"{prefux}roll (Finishing number) (Starting number [Optional, Default is 1])", value="Rolls a random number between the Starting number and Finishing number.", inline=False)
    embed.add_field(name=f"{prefux}calc (equation)", value="Calculator! (type \"list\" as an equation to get a list of functions)", inline=False)
    embed.add_field(name=f"{prefux}avatar (user)", value="Get a user's avatar.", inline=False)
    embed.add_field(name=f"{prefux}pet (user) (speed (the higher the number the slower the speed, default is 30))", value="Pets a user :3 (Warning: It takes some time to output the gif so be patient and don't overload it)", inline=False)
    embed.add_field(name=f"{prefux}flowery (file name [optional, type \"list\" for list of files])", value="Flowery :3", inline=False)
    embed.add_field(name=f"{prefux}prefixset (prefix)", value="Set the bots prefix (Admin only)", inline=False)

    embed.set_footer(text="(That's it for right now, other commands will be added in the future enjoy! :3)")

    await ctx.reply(embed=embed)

@bot.command()
async def hug(ctx, *, who: str = None):
    user = ctx.author.mention

    target = who

    if who in ("@everyone", "@here"):
        await ctx.reply("You can't just do that!")
        return

    messages = \
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

    choice = random.choice(messages)

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

    if who in ("@everyone", "@here"):
        await ctx.reply("You can't just do that!")
        return

    messages = \
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

    choice = random.choice(messages)

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

    if who in ("@everyone", "@here"):
        await ctx.reply("You can't just do that!")
        return

    messages = \
    [
        f"{user} permanently hugs {target} 🫂",
        f"{user} hugs {target} permanently 🫂",
        f"{user} hugs {target} and they won't let go, ever 🫂🫂",
        f"{user} hugs {target} and never let's go until the end of time and beyond 🫂",
        f"{user} has trapped {target} with an eternal hug 🫂"
    ]

    choice = random.choice(messages)

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

    if who in ("@everyone", "@here"):
        await ctx.reply("You can't just do that!")
        return

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

    messages = \
    [
        f"{user} kissed {target}! They're so cute!",
        f"OMG- GUYS- {user} JUST KISSED {target}!!!!",
        f"{user} **VIOLENTLY** pulled {target} to them and **SMOOCHED** them on the **LIPS**, not letting **ANYONE ELSE** in",
        f"Hehehehe, {user} gave {target} a little smooooch!"
    ]

    choice = random.choice(messages)

    if who == user:
        await ctx.reply(f"{user} kissed themselves? ...how?")
    elif who:
        await ctx.reply(choice)
    else:
        await ctx.reply(f"{user} kissed themselves? ...how?")

@bot.command()
async def cheekkiss(ctx, *, who: str = None):
    user = ctx.author.mention

    target = who

    if who in ("@everyone", "@here"):
        await ctx.reply("You can't just do that!")
        return

    messages = \
    [
        f"{user} gave {target} a cute kiss on the cheek! Awwhh! :3",
        f"{user} gave {target} a little cheek smooch! ^^",
        f"{user} not so violently pulled {target} to them and pekced them on the cheek, letting everyone else in ^w^",
        f"Hey guys, {user} gave {target} a little cheek smooch!!! :3",
        f"Hehehe {user} is so cute, they just kissed {target} on the cheek ^^",
        f"Hehehe- {user} gave {target} a peck on the cheek!!!! :3"
    ]

    choice = random.choice(messages)

    if who == user:
        await ctx.reply(f"{user} kissed themselves on the cheek? ...how?")
    elif who:
        await ctx.reply(choice)
    else:
        await ctx.reply(f"{user} kissed themselves on the cheek? ...how?")

@bot.command()
async def calc(ctx, *, equation: str):

    bruh = ""
    result = funcs.calculate(equation)

    if result == 67:
        bruh = " (Seriously bruh? -_-)"
    elif result == 69:
        bruh = " (Seriously bruh? -_-)"

    if equation == "9+10":
        await ctx.reply(f"{equation} =\n21")
    elif equation == "9 + 10":
        await ctx.reply(f"{equation} =\n21")
    else:
        try:
          await ctx.reply(f"{equation} =\n{result}{bruh}")

        except Exception as e:
          await ctx.reply(f"Error: {e}")

@bot.command()
async def pet(ctx, *, args: str = None):
    speed_ms = 30
    text = args

    user = ctx.author.mention

    status = await ctx.reply("Uploading...")

    if args:
        parts = args.rsplit(" ", 1)
        if len(parts) == 2 and parts[1].isdigit():
            text, speed_ms = parts[0], int(parts[1])
        elif args.isdigit():
            text, speed_ms = None, int(args)

    if ctx.mentions:
        target = ctx.mentions[0]
    else:
        target = ctx.author

    async with aiohttp.ClientSession() as session:
        async with session.get(target.avatar_url) as resp:
            avatar_bytes = io.BytesIO(await resp.read())

    gif_bytes = io.BytesIO()
    funcs.make_pet_gif(avatar_bytes, gif_bytes, speed_ms=speed_ms)
    gif_bytes.seek(0)

    await ctx.reply(f"{user} has pet {target.mention} :3", file=fluxer.File(gif_bytes, filename="pet.gif"))
    await status.delete

@bot.command()
async def avatar(ctx, *, who: str = None):
    if ctx.mentions:
        target = ctx.mentions[0]
    else:
        target = ctx.author

    embed = fluxer.Embed(
        title=f"{target.display_name}'s avatar",
        color=0xFFC0CB,
    )
    embed.set_image(url=target.avatar_url)
    await ctx.reply(embed=embed)

flowery_folder = "files/audio/flowery_voice_clips/"

@bot.command()
async def flowery(ctx, *, filename: str = None):
    files = os.listdir(flowery_folder)
    if not files:
        await ctx.reply("No files in the folder!")
        return

    if filename and filename.lower() == "list":
        embed = fluxer.Embed(
            title="Flowery clips",
            description="\n".join(f"- {f}" for f in files),
            color=0x52F0EF,
        )
        await ctx.reply(embed=embed)
        return

    if filename:
        search = filename.lower()
        matches = [
            f for f in files
            if f.lower() == search or os.path.splitext(f)[0].lower() == search
        ]

        if not matches:
            await ctx.reply(f"Couldn't find `{filename}` in the folder.")
            return

        choice = matches[0]
    else:
        choice = random.choice(files)

    path = os.path.join(flowery_folder, choice)

    status = await ctx.reply("uploading... 🌸")

    await ctx.reply(file=fluxer.File(path, filename=choice))
    await status.delete()

@bot.command()
async def prefixset(ctx, new_prefix: str = None):
    if ctx.guild is None:
        await ctx.reply("This only works in a server, not DMs.")
        return

    ADMINISTRATOR = 0x8

    member = await ctx.guild.fetch_member(ctx.author.id)
    roles = await ctx.guild.fetch_roles()

    is_admin = any(
        (role.permissions & ADMINISTRATOR) == ADMINISTRATOR
        for role in roles
        if role.id in member.roles
    )

    if not is_admin:
        await ctx.reply("You need to be an admin to change the prefix.")
        return

    if not new_prefix:
        current_prefix = funcs.get_prefix(ctx.guild.id)
        await ctx.reply(f"Current prefix is: `{current_prefix}`")
        return

    funcs.set_prefix(ctx.guild.id, new_prefix)

    await ctx.reply(f"Prefix changed to: `{new_prefix}`")

if not debug:
    funcs.keep_alive()

# 4. Run the bot using your Fluxer token
if __name__ == "__main__":
    if not debug:
        TOKEN = os.getenv('TOKEN')
    else:
        TOKEN = os.getenv('TOKEN2')
    bot.run(TOKEN)