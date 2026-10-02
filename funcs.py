from flask import Flask
from threading import Thread
import io
import math
import cmath
import re
import os
import psycopg2

from petpetgif_fix import petpet
from PIL import Image

DEFAULT_PREFIX = "!"

def get_connection():
    return psycopg2.connect(os.getenv("DATABASE_URL"))


def init_db():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS prefixes (
            server_id TEXT PRIMARY KEY,
            prefix TEXT NOT NULL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS last_hugged (
            server_id TEXT NOT NULL,
            target_id TEXT NOT NULL,
            hugger_id TEXT NOT NULL,
            hugged_at TIMESTAMP NOT NULL DEFAULT NOW(),
            PRIMARY KEY (server_id, target_id)
        )
    """)

    conn.commit()
    cursor.close()
    conn.close()


def get_prefix(server_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT prefix FROM prefixes WHERE server_id = %s",
        (str(server_id),)
    )

    result = cursor.fetchone()

    cursor.close()
    conn.close()

    return result[0] if result else DEFAULT_PREFIX


def set_prefix(server_id, prefix):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO prefixes (server_id, prefix)
        VALUES (%s, %s)
        ON CONFLICT (server_id)
        DO UPDATE SET prefix = EXCLUDED.prefix
    """, (str(server_id), prefix))

    conn.commit()
    cursor.close()
    conn.close()


def get_bot_prefix(bot, message):
    if message.guild is None:
        return DEFAULT_PREFIX

    return get_prefix(message.guild.id)

HUG_EXPIRY_DAYS = 3

def get_last_hugger(server_id, target_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """SELECT hugger_id FROM last_hugged WHERE server_id = %s AND target_id = %s AND hugged_at > NOW() - make_interval(days => %s)""",
        (str(server_id), str(target_id), HUG_EXPIRY_DAYS)
    )

    result = cursor.fetchone()

    cursor.close()
    conn.close()

    return result[0] if result else None


def set_last_hugger(server_id, target_id, hugger_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO last_hugged (server_id, target_id, hugger_id, hugged_at)
        VALUES (%s, %s, %s, NOW())
        ON CONFLICT (server_id, target_id)
        DO UPDATE SET hugger_id = EXCLUDED.hugger_id, hugged_at = NOW()
    """, (str(server_id), str(target_id), str(hugger_id)))

    conn.commit()
    cursor.close()
    conn.close()


def clear_last_hugger(server_id, target_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM last_hugged WHERE server_id = %s AND target_id = %s",
        (str(server_id), str(target_id))
    )

    conn.commit()
    cursor.close()
    conn.close()

def init_db_start():
    init_db()

MIN_SPEED_MS = 20
def make_pet_gif(source, dest, speed_ms=20):
    speed_ms = max(speed_ms, MIN_SPEED_MS)

    temp = io.BytesIO()
    petpet.make(source, temp)
    temp.seek(0)

    img = Image.open(temp)
    frames = []
    try:
        while True:
            frames.append(img.copy())
            img.seek(img.tell() + 1)
    except EOFError:
        pass

    frames[0].save(
        dest, format="GIF", save_all=True,
        append_images=frames[1:], duration=speed_ms, loop=0,disposal=2,
    )

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
            "pi  e  i",
        ])
    expr = expr.replace('x', '*').replace('X', '*').replace('^', '**')
    if not re.fullmatch(r'[\d+\-*/().\s^a-zA-Z,]+', expr):
        raise ValueError("Invalid characters in expression")
    allowed_names = {
        "sqrt": cmath.sqrt,
        # radians (standard)
        "sin": cmath.sin,
        "cos": cmath.cos,
        "tan": cmath.tan,
        "asin": cmath.asin,
        "acos": cmath.acos,
        "atan": cmath.atan,
        # degrees
        "sind": lambda x: cmath.sin(x * cmath.pi / 180),
        "cosd": lambda x: cmath.cos(x * cmath.pi / 180),
        "tand": lambda x: cmath.tan(x * cmath.pi / 180),
        "asind": lambda x: cmath.asin(x) * 180 / cmath.pi,
        "acosd": lambda x: cmath.acos(x) * 180 / cmath.pi,
        "atand": lambda x: cmath.atan(x) * 180 / cmath.pi,
        # hyperbolic
        "sinh": cmath.sinh,
        "cosh": cmath.cosh,
        "tanh": cmath.tanh,
        "log": cmath.log,
        "log10": cmath.log10,
        "log2": lambda x: cmath.log(x, 2),
        "exp": cmath.exp,
        "pi": cmath.pi,
        "e": cmath.e,
        "i": 1j,
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
        "deg": lambda x: x * 180 / cmath.pi,
        "rad": lambda x: x * cmath.pi / 180,
    }
    return eval(expr, {"__builtins__": {}}, allowed_names)

app = Flask('')

@app.route('/')
def home():
    return "Bot is running!"

def run():
    port = int(os.getenv("PORT", 8000))
    app.run(host='0.0.0.0', port=port)

def keep_alive():
    t = Thread(target=run)
    t.start()