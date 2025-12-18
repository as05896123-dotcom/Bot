import sqlite3

conn = sqlite3.connect('bot.db', check_same_thread=False)
cursor = conn.cursor()

# جدول المستخدمين
cursor.execute('''CREATE TABLE IF NOT EXISTS users (
    user_id INTEGER PRIMARY KEY,
    role TEXT DEFAULT 'عضو',
    points INTEGER DEFAULT 0,
    messages INTEGER DEFAULT 0,
    swhats INTEGER DEFAULT 0
)''')

# جدول الممنوعين
cursor.execute('''CREATE TABLE IF NOT EXISTS banned (
    user_id INTEGER PRIMARY KEY
)''')

# جدول الردود
cursor.execute('''CREATE TABLE IF NOT EXISTS custom_replies (
    trigger TEXT PRIMARY KEY,
    response TEXT
)''')

# جدول الاوامر المضافة
cursor.execute('''CREATE TABLE IF NOT EXISTS added_commands (
    command TEXT PRIMARY KEY,
    response TEXT
)''')

conn.commit()

# دوال مساعدة
def add_user(user_id):
    cursor.execute('INSERT OR IGNORE INTO users(user_id) VALUES(?)', (user_id,))
    conn.commit()

def add_points(user_id, pts=1):
    add_user(user_id)
    cursor.execute('UPDATE users SET points = points + ? WHERE user_id = ?', (pts, user_id))
    conn.commit()

def get_points(user_id):
    cursor.execute('SELECT points FROM users WHERE user_id = ?', (user_id,))
    row = cursor.fetchone()
    return row[0] if row else 0

def add_message(user_id):
    add_user(user_id)
    cursor.execute('UPDATE users SET messages = messages + 1 WHERE user_id = ?', (user_id,))
    conn.commit()

def get_messages(user_id):
    cursor.execute('SELECT messages FROM users WHERE user_id = ?', (user_id,))
    row = cursor.fetchone()
    return row[0] if row else 0

def ban_user(user_id):
    cursor.execute('INSERT OR IGNORE INTO banned(user_id) VALUES(?)', (user_id,))
    conn.commit()

def unban_user(user_id):
    cursor.execute('DELETE FROM banned WHERE user_id = ?', (user_id,))
    conn.commit()

def is_banned(user_id):
    cursor.execute('SELECT 1 FROM banned WHERE user_id = ?', (user_id,))
    return cursor.fetchone() is not None

def set_reply(trigger, response):
    cursor.execute('INSERT OR REPLACE INTO custom_replies(trigger,response) VALUES(?,?)', (trigger,response))
    conn.commit()

def get_reply(trigger):
    cursor.execute('SELECT response FROM custom_replies WHERE trigger = ?', (trigger,))
    row = cursor.fetchone()
    return row[0] if row else None

def delete_reply(trigger):
    cursor.execute('DELETE FROM custom_replies WHERE trigger = ?', (trigger,))
    conn.commit()

def add_command(command, response):
    cursor.execute('INSERT OR REPLACE INTO added_commands(command,response) VALUES(?,?)', (command,response))
    conn.commit()

def get_command(command):
    cursor.execute('SELECT response FROM added_commands WHERE command = ?', (command,))
    row = cursor.fetchone()
    return row[0] if row else None

def delete_command(command):
    cursor.execute('DELETE FROM added_commands WHERE command = ?', (command,))
    conn.commit()
