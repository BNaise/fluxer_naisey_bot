import psycopg2
import os

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

HUG_EXPIRY_DAYS = 1

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

    cursor.execute("""
        DELETE FROM last_hugged
        WHERE hugged_at < NOW() - make_interval(days => %s)
    """, (HUG_EXPIRY_DAYS,))

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