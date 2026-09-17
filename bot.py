import os
import random
import re
import math

import fluxer

from dotenv import load_dotenv

import keep_alive

load_dotenv()

debug = False
# debug = True

bot = fluxer.Bot(command_prefix="!", intents=fluxer.Intents.all())

def calculate(expr):
    if expr.strip().lower() == "list":
        return "\n".join([
            "+  -  *  /  x  ^",
            "sqrt(x)",
            "sin(x)  cos(x)  tan(x)          [radians]",
            "asin(x) acos(x) atan(x)         [radians]",
            "sind(x) cosd(x) tand(x)         [degrees]",
            "asind(x) acosd(x) atand(x)      [degrees]",
            "sinh(x) cosh(x) tanh(x)",
            "log(x) log(x, base) log10(x) log2(x)",
            "exp(x)",
            "abs(x)",
            "factorial(x)",
            "round(x) round(x, n)",
            "floor(x) ceil(x)",
            "gcd(a, b) lcm(a, b)",
            "hypot(a, b)",
            "mod(a, b)",
            "min(a, b, ...) max(a, b, ...)",
            "deg(x) rad(x)",
            "pi  e",
        ])
    expr = expr.replace('x', '*').replace('X', '*').replace('^', '**')
    if not re.fullmatch(r'[\d+\-*/().\s^a-zA-Z,]+', expr):
        raise ValueError("Invalid characters in expression")
    allowed_names = {
        "sqrt": math.sqrt,
        # radians (standard)
        "sin": math.sin,
        "cos": math.cos,
        "tan": math.tan,
        "asin": math.asin,
        "acos": math.acos,
        "atan": math.atan,
        # degrees
        "sind": lambda x: math.sin(math.radians(x)),
        "cosd": lambda x: math.cos(math.radians(x)),
        "tand": lambda x: math.tan(math.radians(x)),
        "asind": lambda x: math.degrees(math.asin(x)),
        "acosd": lambda x: math.degrees(math.acos(x)),
        "atand": lambda x: math.degrees(math.atan(x)),
        # hyperbolic
        "sinh": math.sinh,
        "cosh": math.cosh,
        "tanh": math.tanh,
        "log": math.log,
        "log10": math.log10,
        "log2": math.log2,
        "exp": math.exp,
        "pi": math.pi,
        "e": math.e,
        "abs": abs,
        "factorial": math.factorial,
        "round": round,
        "floor": math.floor,
        "ceil": math.ceil,
        "gcd": math.gcd,
        "lcm": math.lcm,
        "hypot": math.hypot,
        "mod": lambda a, b: a % b,
        "min": min,
        "max": max,
        "deg": math.degrees,
        "rad": math.radians,
    }
    return eval(expr, {"__builtins__": {}}, allowed_names)

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
    embed.add_field(name="!kiss (user)", value="Kiss the mentioned user", inline=False)
    embed.add_field(name="!cheekkiss (user)", value="Kiss the mentioned user on the cheek :3", inline=False)
    embed.add_field(name="!silly (user (optional))", value="Silly :P", inline=False)
    embed.add_field(name="!deltarot", value="Says Deltarots -_-", inline=False)
    embed.add_field(name="!gamble", value="Let's go gambling!!", inline=False)
    embed.add_field(name="!roll (Finishing number) (Starting number (Optional, Default is 1))", value="Rolls a random number between the Starting number and Finishing number.", inline=False)
    embed.add_field(name="!calc (equation)", value="Calculator! (type \"list\" as an equation to get a list of functions)", inline=False)

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

    try:
      await ctx.reply(f"{equation} =\n{calculate(equation)}")

    except Exception as e:
      await ctx.reply(f"Error: {e}")

if not debug:
    keep_alive.keep_alive()

# 4. Run the bot using your Fluxer token
if __name__ == "__main__":
    if not debug:
        TOKEN = os.getenv('TOKEN')
    else:
        TOKEN = os.getenv('TOKEN2')
    bot.run(TOKEN)