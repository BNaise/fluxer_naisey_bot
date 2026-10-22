import os
import random
import io
import re

import aiohttp
import asyncio

import fluxer

from fluxer import utils

from dotenv import load_dotenv

from funtions import database, pet_gif, multi_pet_gif, calculator, keep_alive

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

# Debug the bot
debug = False
# debug = True

#Starts Database
database.init_db_start()

if not debug:
    #Sets the prefix
    bot = fluxer.Bot(command_prefix=database.get_bot_prefix, intents=fluxer.Intents.all())
else:
    bot = fluxer.Bot(command_prefix="!", intents=fluxer.Intents.all())

@bot.event
async def on_ready():
    print(f"Bot is online! Logged in as {bot.user.username}")

# "@everyone" or "@here" detection
def is_everyone_or_here(who):
    return who is not None and who.strip().lower() in ("@everyone", "@here")

# Commands
@bot.command()
async def help(ctx):
    if ctx.guild is None:
        prefux = "!"
    else:
        prefux = database.get_prefix(ctx.guild.id)

    commands_list = [
        (f"{prefux}help", "Sends this help message"),
        (f"{prefux}hug <user>", "Hug someone ^^"),
        (f"{prefux}permahug <user>", "Hug someone forever :3"),
        (f"{prefux}cuddle <user>", "Cuddle someone ^w^"),
        (f"{prefux}nuzzle <user>", "Nuzzle someone ~^w^~"),
        (f"{prefux}kiss <user>", "Kiss someone >w<"),
        (f"{prefux}cheekkiss <user>", "Kiss someone on the cheek >v<"),
        (f"{prefux}praise <user>", "Praise someone :D"),
        (f"{prefux}ship <user1> <user2>", "Mention two people to ship them ^^"),
        (f"{prefux}silly [user]", "Be silly, optionally at someone >:3"),
        (f"{prefux}murder <user>", "Murderrrr >:3"),
        (f"{prefux}revive <user>", "Revive the dead ^w^"),
        (f"{prefux}deltarot", "Says Deltarot"),
        (f"{prefux}gamble", "Let's go gambling!!"),
        (f"{prefux}coinflip", "Flip a coin"),
        (f"{prefux}bored", "Bored -_-"),
        (f"{prefux}yogurt", "Gurt"),
        (f"{prefux}starwalker", "Starwalker :)"),
        (f"{prefux}roll <max> [min=1]", "Random number between min and max"),
        (f"{prefux}calc <equation>", "Calculator — type `list` as the equation for functions"),
        (f"{prefux}avatar [user]", "Get a user's avatar (yours if no user given)"),
        (f"{prefux}pet [user/image...] [speed=40]", "Pet up to 10 users/images — separate gifs. Lower speed number = faster pet"),
        (f"{prefux}petmix [user/image...] [speed=40]", "Same as pet, but one combined gif"),
        (f"{prefux}flowery [name/list/grep <text>]", "Flowery voice clips"),
        (f"{prefux}kawkaw [name/list/grep <text>]", "Kawkaw clips"),
        (f"{prefux}prefixset <prefix>", "Change the bot's prefix — admin only"),
        (f"{prefux}this one is a secret >:3", "Can ya find it? Ow<*"),
    ]

    lines = [f"`{cmd}` — {desc}" for cmd, desc in commands_list]

    embed = fluxer.Embed(
        title="Naisey's commands",
        description="\n".join(lines),
        color=0x52F0EF
    )
    embed.set_footer(text="(That's it for right now, other commands will be added in the future enjoy! :3)")

    await ctx.reply(embed=embed)

@bot.command()
async def hug(ctx, *, who: str = None):
    user = ctx.author.mention

    if is_everyone_or_here(who):
        if who.strip().lower() == "@everyone":
            await ctx.reply(f"{user} gives a giant hug to everyone! ^^")
        else:
            await ctx.reply(f"{user} gives a giant hug to everyone here! ^^")

    if who == bot.user.mention:
        await ctx.reply("Awww Thank youuu! ^^\n*Hugs you back ^^")
        return

    who = utils.escape_mentions(who) if who else who

    target = who
    reciprocal = False

    if ctx.mentions:
        target_id = ctx.mentions[0].id
        author_id = ctx.author.id
        scope_id = ctx.guild.id if ctx.guild else f"dm-{ctx.channel_id}"

        last_hugger = database.get_last_hugger(scope_id, author_id)
        if last_hugger == str(target_id):
            reciprocal = True
            database.clear_last_hugger(scope_id, author_id)
        else:
            database.set_last_hugger(scope_id, target_id, author_id)

    if reciprocal:
        messages = [
            f"{user} hugs {target} back! Aww, mutual hugs 🫂💕",
            f"{target} hugged {user} first, and now {user} returns the favor! 🫂",
            f"{user} and {target} share a hug back and forth. So wholesome! 🤗",
        ]
    else:
        messages = [
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
            f"{user} hugs {target}. No escape. 🫂",
        ]

    choice = random.choice(messages)

    if target == user:
        await ctx.reply(f"{user} gave themselves a hug 🫂🥺")
    elif target:
        await ctx.reply(choice)
    else:
        await ctx.reply(f"{user} gave themselves a hug 🫂🥺")

@bot.command()
async def cuddle(ctx, *, who: str = None):
    user = ctx.author.mention

    target = who

    if is_everyone_or_here(who):
        if who.strip().lower() == "@everyone":
            await ctx.reply(f"{user} gives a giant cuddle to everyone! ^^")
        else:
            await ctx.reply(f"{user} gives a giant cuddle to everyone here! ^^")

    if who == bot.user.mention:
        await ctx.reply("Awwww thanks! ^w^\n*Cuddles back ^^")
        return

    if len(ctx.mentions) < 2:
        messages = \
            [
                f"{user} is cuddling {target}. Awwwww :3",
                f"{user} and {target} are now cuddling! :3",
                f"{user} gives {target} a warm cuddle! :3",
                f"{user} and {target} are wrapped up in a cuddle! :3",
                f"{user} and {target} are having a cuddle session! :3",
                f"{user} and {target} are snuggled up together! :3",
                f"{user} has cuddled {target} into oblivion :3",
                f"{target} got absolutely loved and cuddled by {user} :3"
            ]
    elif len(ctx.mentions) >= 2:
        messages = \
            [
                f"{user} gives {target} a warm cuddle! :3",
                f"{user} has cuddled {target} into oblivion :3",
                f"{target} got absolutely loved and cuddled by {user} :3"
            ]

    choice = random.choice(messages)

    if who == user:
        await ctx.reply(f"{user} cuddled themselves??")
    elif who:
        await ctx.reply(choice)
    else:
        await ctx.reply(f"{user} cuddled themselves??")

@bot.command()
async def praise(ctx, *, who: str = None):
    user = ctx.author.mention

    target = who

    is_or_are = "is"
    isnt = "isn't"
    more = " "

    if len(ctx.mentions) >= 2:
      is_or_are = "are"
      isnt = "aren't"
      more = " guys "

    if is_everyone_or_here(who):
        if who.strip().lower() == "@everyone":
            await ctx.reply(f"{user} has praised everyone! (everyone likes it :3)")
        else:
            await ctx.reply(f"{user} has praised everyone here! (everyone (here) likes it :3)")

    if who == bot.user.mention:
        await ctx.reply("Thanks >w<\nyou're awesome too! ^//^")
        return

    messages = \
        [
            f"Hehe ^^\n{target} {is_or_are} such a cutie! ^^",
            f"Awwwww :3\n{target} {is_or_are} soooo cute! :33 ",
            f"{target}! you{more}are so adorable! :3 ",
            f"{target}! you{more}are sooo awesome! :3 ",
            f"Awwwww! :3 {isnt} {target} sooooo cute? ^?^",
            f"{target} {is_or_are} so cute! :3 >w<",
            f"{target} {is_or_are} so cute that I can hug them endlessly! ^w^",
            f"{target} {is_or_are} such a cutie patooti :3 ^~^"
        ]

    choice = random.choice(messages)

    if who == user:
        await ctx.reply(f"{user} praised themselves. Must be really confident")
    elif who:
        await ctx.reply(choice)
    else:
        await ctx.reply("Mention a user or write someones name")

@bot.command()
async def nuzzle(ctx, *, who: str = None):
    user = ctx.author.mention

    target = who

    if is_everyone_or_here(who):
        if who.strip().lower() == "@everyone":
            await ctx.reply(f"{user} has nuzzled everyone! Awww so cute! ^^")
        else:
            await ctx.reply(f"{user} has nuzzled everyone here! Awwww so cute! ^^")

    if who == bot.user.mention:
        await ctx.reply("Thanks! >w<\n*nuzzles back! ^^")
        return

    messages = \
        [
            f"{user} nuzzles {target} like a susie plushie ^w^",
            f"{target} is being nuzzled in 180 rpm by {user} ^^",
            f"{target} feels the soft nuzzle of {user} :3"
        ]

    choice = random.choice(messages)

    if who == user:
        await ctx.reply(f"{user} nuzzled themselves?? Impossible...")
    elif who:
        if choice == f"{user} nuzzles {target} like a susie plushie ^w^":
            status = await ctx.reply("Uploading...")
            file = fluxer.File("files/images/gifs/susie_plush_nuzzle.gif")
            await ctx.reply(choice, file=file)
            await status.delete()
        else:
            await ctx.reply(choice)
    else:
        await ctx.reply("Mention a user or write someones name")

@bot.command()
async def permahug(ctx, *, who: str = None):
    user = ctx.author.mention

    target = who

    if is_everyone_or_here(who):
        if who.strip().lower() == "@everyone":
            await ctx.reply(f"{user} has permanently hugged everyone and won't let go")
        else:
            await ctx.reply(f"{user} has permanently hugged everyone here and won't let go")

    if who == bot.user.mention:
        await ctx.reply("Thank you! :3\n*Comforts you")
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

    if who:

      if is_everyone_or_here(who):
          if who.strip().lower() == "@everyone":
            await ctx.reply(f"{user} does silly thing to everyone >:3")
          else:
            await ctx.reply(f"{user} does silly thing to everyone in here >:3")
      if who == bot.user.mention:
          await ctx.reply("Wawa? OwO")
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
            "Hey there little guy!",
            "Heh its my jarona!",
            "He is in some king of snowgrave.",
            "*_Swoon_",
            "I'm the Roaring Knight! and am a fraud!",
            "*You looked behind the tree",
            "*Well there is a man here",
            "*And he is offering you a egg",
            "*Susie's idea",
            "WD.Gaster in deltarune build it all from a empty room.",
            "Its 12:25 outside.",
            "Well this stinks.",
            "I'm Old!",
            "I'm fOld!",
            "What do you do with a drunken gonner!\n What do you do with a drunken gonner!\nWhat do you do with a drunken gonner!\nEarly in the Roaring!",
            "PINK AND YELLOW?!?! 🩷=💛",
            "*Why wold Chara do this?!?!",## naise add chara doing What me??? pose to this line pls!!! :3 ty already!! :3 oh and i added the png lol it is Chara_What_Me.png in the files/images folder :3 ##
            "I am Frisk.",
            f"CHAOS CHAOS!"
        ]

    choice = random.choice(messages)

    if choice == "Hey undyne!\nHow many human souls do we need to break the barrier?":
        file = fluxer.File("files/images/undyne-seven.webp")
        await ctx.reply(choice, file=file)
    elif choice == "*Why wold Chara do this?!?!":
        file = fluxer.File("files/images/Chara_What_Me.png")
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

    if is_everyone_or_here(who):
        if who.strip().lower() == "@everyone":
            await ctx.reply(f"{user} has kissed everyone awwww ^w^")
        else:
            await ctx.reply(f"{user} has kissed everyone here awwww ^w^")
    if who == bot.user.mention:
        await ctx.reply("T-thanks? >/////<")
        return

    messages = \
    [
        f"{user} kissed {target}! They're so cute!",
        f"OMG- GUYS- {user} JUST KISSED {target}!!!!",
        f"{user} **VIOLENTLY** pulled {target} to them and **SMOOCHED** them on the **LIPS**, not letting **ANYONE ELSE** in >:3",
        f"Hehehehe, {user} gave {target} a little smooooch!"
    ]

    choice = random.choice(messages)

    if who == user:
        await ctx.reply(f"{user} kissed themselves? ...how?")
    elif who:
        await ctx.reply(choice)
    else:
        await ctx.reply("Mention someone or put someones name to kiss them :3")

@bot.command()
async def cheekkiss(ctx, *, who: str = None):
    user = ctx.author.mention

    target = who

    if is_everyone_or_here(who):
        if who.strip().lower() == "@everyone":
            await ctx.reply(f"{user} has kissed everyone on the cheek awwww ^w^")
        else:
            await ctx.reply(f"{user} has kissed everyone here on the cheek awwww ^w^")
    if who == bot.user.mention:
        await ctx.reply("T-thanks >///<")
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
        await ctx.reply("Mention someone or put someones name to kiss them on the cheek :3")

@bot.command()
async def calc(ctx, *, equation: str):

    try:
        result = calculator.calculate(equation)
    except Exception as e:
        await ctx.reply(f"Error: {e}")
        return

    bruh = ""
    if result == 67:
        bruh = " (Seriously bruh? -_-)"
    elif result == 69:
        bruh = " (Seriously bruh? -_-)"

    if equation == "9+10":
        await ctx.reply(f"{equation} =\n21")
    elif equation == "9 + 10":
        await ctx.reply(f"{equation} =\n21")
    else:
        await ctx.reply(f"{equation} =\n{result}{bruh}")

@bot.command()
async def pet(ctx, *, args: str = None):
    speed_ms = 40
    text = args

    user = ctx.author.mention

    if args:
        parts = args.rsplit(" ", 1)
        if len(parts) == 2 and parts[1].isdigit():
            text, speed_ms = parts[0], int(parts[1])
        elif args.isdigit():
            text, speed_ms = None, int(args)

    speed_ms = max(speed_ms, 20)

    image_urls = []

    # Attached images take priority
    if ctx.attachments:
        image_urls = [a.url for a in ctx.attachments[:10]]

    # Fall back to mentioned users
    elif ctx.mentions:
        raw_ids = re.findall(r'<@!?(\d+)>', ctx.content)
        if raw_ids:
            mention_lookup = {str(m.id): m for m in ctx.mentions}
            targets = [mention_lookup[i] for i in raw_ids[:10] if i in mention_lookup]
            image_urls = [t.avatar_url for t in targets]

    # Default to the author's own avatar
    elif not args:
        image_urls = [ctx.author.avatar_url]

    if not image_urls:
        await ctx.reply("Mention someone, attach an image, or type nothing to pet yourself :3")
        return

    status = await ctx.reply("petting... 🫳")

    files = []
    async with aiohttp.ClientSession() as session:
        for i, url in enumerate(image_urls):
            async with session.get(url) as resp:
                image_bytes = io.BytesIO(await resp.read())

            gif_bytes = io.BytesIO()
            await asyncio.to_thread(pet_gif.make_pet_gif, image_bytes, gif_bytes, speed_ms)
            gif_bytes.seek(0)

            files.append(fluxer.File(gif_bytes, filename=f"pet_{i}.gif"))

    if ctx.attachments:
        content = f"{ctx.author.mention} has pet the image(s) :3"
    elif ctx.mentions:
        target_mentions = [t.mention for t in targets]
        names = target_mentions[0] if len(target_mentions) == 1 else ", ".join(target_mentions[:-1]) + f" and {target_mentions[-1]}"
        content = f"{ctx.author.mention} has pet {names} :3"
    else:
        content = f"{ctx.author.mention} has pet themselves :3"

    await ctx.reply(content=content, files=files)
    await status.delete()

@bot.command()
async def petmix(ctx, *, args: str = None):
    speed_ms = 40
    text = args

    if args:
        parts = args.rsplit(" ", 1)
        if len(parts) == 2 and parts[1].isdigit():
            text, speed_ms = parts[0], int(parts[1])
        elif args.isdigit():
            text, speed_ms = None, int(args)

    speed_ms = max(speed_ms, 20)

    image_urls = []

    # Attached images take priority
    if ctx.attachments:
        image_urls = [a.url for a in ctx.attachments[:10]]

    # Fall back to mentioned users
    elif ctx.mentions:
        if len(ctx.mentions) > 1:
            raw_ids = re.findall(r'<@!?(\d+)>', ctx.content)
            if raw_ids:
                mention_lookup = {str(m.id): m for m in ctx.mentions}
                targets = [mention_lookup[i] for i in raw_ids[:10] if i in mention_lookup]
                image_urls = [t.avatar_url for t in targets]
        else:
            await ctx.reply("Mention more than one user (or attach multiple images) to mix pet :3")
            return

    if not image_urls:
        await ctx.reply("Attach images or mention multiple users to pet :3")
        return

    status = await ctx.reply("petting... 🫳")

    avatar_byte_list = []
    async with aiohttp.ClientSession() as session:
        for url in image_urls:
            async with session.get(url) as resp:
                avatar_byte_list.append(io.BytesIO(await resp.read()))

    gif_bytes = io.BytesIO()
    await asyncio.to_thread(multi_pet_gif.make_multi_pet_gif, avatar_byte_list, gif_bytes, speed_ms)
    gif_bytes.seek(0)

    if ctx.attachments:
        content = f"{ctx.author.mention} has pet the images :3"
    else:
        target_mentions = [t.mention for t in targets]
        names = ", ".join(target_mentions[:-1]) + f" and {target_mentions[-1]}"
        content = f"{ctx.author.mention} has pet {names} :3"

    await ctx.reply(content=content, file=fluxer.File(gif_bytes, filename="petall.gif"))
    await status.delete()

@bot.command()
async def avatar(ctx, *, who: str = None):
    if ctx.mentions:
        target = ctx.mentions[0]
    else:
        target = ctx.author

    status = await ctx.reply("Uploading...")

    embed = fluxer.Embed(
        title=f"{target.display_name}'s avatar",
        color=0xFFC0CB,
    )
    embed.set_image(url=target.avatar_url)
    await ctx.reply(embed=embed)
    await status.delete()

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
            description="\n".join(f"- {f}" for f in sorted(files)),
            color=0x52F0EF,
        )
        try:
            await ctx.author.send(embed=embed)
            await ctx.reply("Sent you the list in DMs!")
        except Exception:
            await ctx.reply("Couldn't DM you - check your privacy setting allow DMs from server members.")
        return
    elif filename and filename.lower() == "ls":
        embed = fluxer.Embed(
            title="Flowery clips",
            description="\n".join(f"- {f}" for f in sorted(files)),
            color=0x52F0EF,
        )
        try:
            await ctx.author.send(embed=embed)
            await ctx.reply("Sent you the list in DMs!")
        except Exception:
            await ctx.reply("Couldn't DM you - check your privacy setting allow DMs from server members.")
        return

    if filename:
        parts = filename.split(maxsplit=1)
        if parts and parts[0].lower() == "grep":
            if len(parts) < 2:
                await ctx.reply("Usage: `flowery grep <text>`")
                return

            query = parts[1].lower()
            found = [f for f in sorted(files) if query in f.lower()]

            if not found:
                await ctx.reply(f"No clips matching `{parts[1]}`.")
                return

            embed = fluxer.Embed(
                title=f"Flowery clips matching \"{parts[1]}\"",
                description="\n".join(f"- {f}" for f in found),
                color=0x52F0EF,
            )

            if len(found) <= 15:
                await ctx.reply(embed=embed)
            else:
                try:
                    await ctx.reply(embed=embed)
                except Exception:
                    await ctx.reply("Try a more specific search.")
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

kawkaw_folder = "files/audio/kawkaw/"

@bot.command()
async def kawkaw(ctx, *, filename: str = None):
    files = os.listdir(kawkaw_folder)
    if not files:
        await ctx.reply("No files in the folder!")
        return

    if filename and filename.lower() == "list":
        embed = fluxer.Embed(
            title="Kawkaw :3",
            description="\n".join(f"- {f}" for f in sorted(files)),
            color=0x52F0EF,
        )

        await ctx.reply(embed=embed)
        return

    elif filename and filename.lower() == "ls":
        embed = fluxer.Embed(
            title="Kawkaw :3",
            description="\n".join(f"- {f}" for f in sorted(files)),
            color=0x52F0EF,
        )

        await ctx.reply(embed=embed)
        return

    if filename:
        parts = filename.split(maxsplit=1)
        if parts and parts[0].lower() == "grep":
            if len(parts) < 2:
                await ctx.reply("Usage: `kawkaw grep <text>`")
                return

            query = parts[1].lower()
            found = [f for f in sorted(files) if query in f.lower()]

            if not found:
                await ctx.reply(f"No clips matching `{parts[1]}`.")
                return

            embed = fluxer.Embed(
                title=f"Kawkaw clips matching \"{parts[1]}\"",
                description="\n".join(f"- {f}" for f in found),
                color=0x52F0EF,
            )

            if len(found) <= 15:
                await ctx.reply(embed=embed)
            else:
                try:
                    await ctx.reply(embed=embed)
                except Exception:
                    await ctx.reply("Try a more specific search.")
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

    path = os.path.join(kawkaw_folder, choice)

    status = await ctx.reply("uploading...")

    await ctx.reply(file=fluxer.File(path, filename=choice))
    await status.delete()

@bot.command()
async def murder(ctx, *, who: str = None):
    user = ctx.author.mention

    target = who

    if is_everyone_or_here(who):
        if who.strip().lower() == "@everyone":
            await ctx.reply(f"{user} has taken the genocide root 😈")
        else:
            await ctx.reply(f"{user} has taken the genocide root 😈")
    if who == bot.user.mention:
        await ctx.reply("Whaaa? what did I do? 😨")
        return

    messages = \
    [
        f"{user} killed {target} when the light went out so no one would know it was them... >:3",
        f"{user} just went \"BOO\", giving {target} a fatal heart attack 😨",
        f"{user} just pulled out a bazooka and blew {target} up!?!? 😨",
        f"{user} just went \"OOGA BOOGA\", giving {target} a fatal heart attack 😈",
    ]

    choice = random.choice(messages)

    if who == user:
        await ctx.reply("That's suicide. Don't joke with that. If you are not okay, call a suicide helpline. Here are some resources:\n1.https://blog.opencounseling.com/suicide-hotlines/\n2.https://findahelpline.com\n3.https://en.wikipedia.org/wiki/List_of_suicide_crisis_lines\nyes we have wiki for this.")
    elif who:
        await ctx.reply(choice)
    else:
        await ctx.reply("Mention someone or put someones name to slay themmm >:3")

HARDCODED_SHIPS = {
    frozenset({1518272833992527872, 1471779547901222947}): ("Jaise",999, "Made for each other 💘"),
    frozenset({1535833572982665216, 1543089610605727744}): ("coneXiAn",34416769, "Made for each other 💘"),
}

@bot.command()
async def ship(ctx, *, args: str = None):
    if not args:
        await ctx.reply("Mention two people to ship :3")
        return

    raw_ids = re.findall(r'<@!?(\d+)>', ctx.content)

    if len(raw_ids) < 2:
        await ctx.reply("Mention two people to ship them together :3")
        return

    mention_lookup = {str(m.id): m for m in ctx.mentions}
    targets = [mention_lookup[i] for i in raw_ids[:2] if i in mention_lookup]

    if len(targets) < 2:
        await ctx.reply("Couldn't find both users mentioned :P")
        return

    a, b = targets[0], targets[1]

    name_a = a.display_name
    name_b = b.display_name

    half_a = name_a[:max(1, len(name_a) // 2)]
    half_b = name_b[len(name_b) // 2:]
    ship_name = half_a + half_b

    pair_key = frozenset({a.id, b.id})
    if pair_key in HARDCODED_SHIPS:
        ship_name, percent, verdict = HARDCODED_SHIPS[pair_key]
    else:
        percent = random.randint(0, 100)

        if percent >= 90:
            verdict = "Soulmates! 💕"
        elif percent >= 70:
            verdict = "Pretty cute together ^w^"
        elif percent >= 40:
            verdict = "Eh, could go either way"
        elif percent >= 15:
            verdict = "Yikes, rough start"
        else:
            verdict = "Absolutely not 💀"

    bar_filled = min(percent // 10, 10)
    bar = "█" * bar_filled + "░" * (10 - bar_filled)

    embed = fluxer.Embed(
        title=f"💘 {ship_name} 💘",
        description=f"{a.mention} x {b.mention}\n\n`{bar}` **{percent}%**\n{verdict}",
        color=0xFF69B4,
    )

    await ctx.reply(embed=embed)

@bot.command()
async def revive(ctx, *, who: str = None):
    user = ctx.author.mention

    target = who

    if target in ("@everyone", "@here"):
        await ctx.reply(f"{user} revived everyone! yayy! they be on the pacifist root ^w^")
        return

    messages = \
    [
        f"{user} crouched by {target} and held `E` for a few seconds",
        f"{user} performed a ritual and sacrificed a doll(?) to bring {target} back to life",
        f"In a flash of light, {user} descended upon {target} and gave them the gift of another life"
    ]

    choice = random.choice(messages)

    if who == user:
        await ctx.reply(f"... Oh my god *{user}'S **IMMORTAL**-*!")
    elif who == bot.user.mention:
        await ctx.reply("Thankies ^^")
    elif who:
        await ctx.reply(choice)
    else:
        await ctx.reply("Mention someone or put someones name to revive them :3")

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
        current_prefix = database.get_prefix(ctx.guild.id)
        await ctx.reply(f"Current prefix is: `{current_prefix}`")
        return

    database.set_prefix(ctx.guild.id, new_prefix)

    await ctx.reply(f"Prefix changed to: `{new_prefix}`")

@bot.command()
async def rake(ctx):
    rake = [
        "files/images/rake.png",
        "files/images/rake_heart.png"
    ]
    choice = random.choice(rake)
    status = await ctx.reply("uploading...")
    file = fluxer.File(choice)
    await ctx.reply(file=file)
    await status.delete()

@bot.command()
async def starwalker(ctx):

    messages = [
        "These birds are pissing me off\nI am the ORIGINAL\n\n\nStarwalker",
        "It was a long journey but now it is time\n`*Transforms*`\nThe Final\n\nStarwalker",
        "These tropical birds are tropissing me off\nI am the Tropical\n\n\nStarwalker"
    ]

    choice = random.choice(messages)

    if choice == "These birds are pissing me off\nI am the ORIGINAL\n\n\nStarwalker":
        file_choice = "files/images/starwalker.png"
    elif choice == "It was a long journey but now it is time\n`*Transforms*`\nThe Final\n\nStarwalker":
        file_choice = "files/images/starwalker_final.png"
    elif choice == "These tropical birds are tropissing me off\nI am the Tropical\n\n\nStarwalker":
        file_choice = "files/images/starwalker_tropical.png"

    status = await ctx.reply("uploading...")
    file = fluxer.File(file_choice)
    await ctx.reply(choice, file=file)
    await status.delete()

@bot.command()
async def bored(ctx):
    file = fluxer.File("files/images/gifs/bernii_bored.gif")
    status = await ctx.reply("uploading...")
    await ctx.reply(file=file)
    await status.delete()

@bot.command()
async def yogurt(ctx):
    gurt = "files/images/gurt.jpg"
    status = await ctx.reply("uploading...")
    file = fluxer.File(gurt)
    await ctx.reply(file=file)
    await status.delete()

@bot.command()
async def coinflip(ctx):

    messages = ["Heads",
                "Tails"]

    choice = random.choice(messages)
    await ctx.reply("The coin has landed on: " + choice)

if not debug:
  keep_alive.keep_alive()

# 4. Run the bot using your Fluxer token
if __name__ == "__main__":
    if not debug:
        TOKEN = os.getenv('TOKEN')
    else:
        TOKEN = os.getenv('TOKEN2')
    bot.run(TOKEN)