from storage import *
from datetime import datetime
from telegram.ext import ContextTypes
import random

async def reply(update, text):
    await update.message.reply_text(text)

async def register_user(update):
    user_id = update.effective_user.id
    add_user(user_id)
    add_points(user_id,1)
    add_message(user_id)

# ===================== معلومات =====================
async def اسمي(update, context):
    register_user(update)
    user = update.effective_user
    await reply(update, f"🙋 اسمك: {user.first_name}")

async def ايديي(update, context):
    register_user(update)
    await reply(update, f"🆔 ايديك: {update.effective_user.id}")

async def نقاطي(update, context):
    register_user(update)
    user_id = update.effective_user.id
    pts = get_points(user_id)
    await reply(update, f"⭐ نقاطك: {pts}")

async def رسائلي(update, context):
    register_user(update)
    user_id = update.effective_user.id
    msgs = get_messages(user_id)
    await reply(update, f"💬 رسائلك: {msgs}")

async def تفاعلي(update, context):
    await reply(update, "🔥 تفاعلك: متوسط")

async def المجموعة(update, context):
    chat = update.effective_chat
    await reply(update, f"📛 اسم المجموعة: {chat.title}\n🆔 الايدي: {chat.id}")

async def الرابط(update, context):
    await reply(update, "🔗 رابط المجموعة غير متوفر حاليا")

async def التاريخ(update, context):
    now = datetime.now().strftime("%Y-%m-%d ⏰ %H:%M")
    await reply(update, now)

# ===================== الردود =====================
async def اضف_رد(update, context):
    if len(context.args) < 2:
        await reply(update, "اكتب: /اضف_رد trigger response")
        return
    trigger = context.args[0]
    response = " ".join(context.args[1:])
    set_reply(trigger,response)
    await reply(update,f"✅ تم اضافة الرد {trigger}")

async def حذف_رد(update, context):
    if not context.args:
        await reply(update, "اكتب: /حذف_رد trigger")
        return
    trigger = context.args[0]
    delete_reply(trigger)
    await reply(update,f"🗑️ تم حذف الرد {trigger}")

async def الردود_المتعددة(update, context):
    cursor.execute('SELECT trigger,response FROM custom_replies')
    rows = cursor.fetchall()
    text = "\n".join([f"{r[0]} ➜ {r[1]}" for r in rows])
    await reply(update,text if rows else "لا يوجد ردود مضافة")

# ===================== منع وتنظيف =====================
async def منع(update, context):
    if update.effective_user.id != 123456789:  # ضع ايديك هنا للمالك
        await reply(update, "❌ ليس لديك صلاحية")
        return
    if not context.args:
        await reply(update, "اكتب ايديي المستخدم")
        return
    try:
        uid = int(context.args[0])
        ban_user(uid)
        await reply(update,f"⛔ تم منع {uid}")
    except:
        await reply(update,"❌ خطأ في الايديي")

async def منع_بالرد(update, context):
    if update.message.reply_to_message:
        uid = update.message.reply_to_message.from_user.id
        ban_user(uid)
        await reply(update,f"⛔ تم منع {uid}")

async def قائمة_المنع(update, context):
    cursor.execute('SELECT user_id FROM banned')
    rows = cursor.fetchall()
    text = "📋 قائمة الممنوعين:\n" + "\n".join(str(r[0]) for r in rows)
    await reply(update,text if rows else "لا يوجد مستخدمين ممنوعين")

async def مسح_قائمة_المنع(update, context):
    cursor.execute('DELETE FROM banned')
    conn.commit()
    await reply(update,"🗑️ تم مسح قائمة المنع")

async def تنظيف(update, context):
    if not context.args or not context.args[0].isdigit():
        await reply(update,"اكتب: /تنظيف عدد")
        return
    n = int(context.args[0])
    await reply(update,f"🧹 تم تنظيف {n} رسالة (تجريبي)")

# ===================== ترفيه وألعاب =====================
async def غنيلي(update, context):
    songs = ["🎵 أغنية 1","🎵 أغنية 2","🎵 أغنية 3"]
    await reply(update, random.choice(songs))

async def فلم(update, context):
    movies = ["🎬 The Matrix","🎬 Inception","🎬 Interstellar"]
    await reply(update, random.choice(movies))

async def متحركة(update, context):
    await reply(update, "🌀 صورة متحركة")

async def فيديو(update, context):
    await reply(update, "📹 فيديو قادم قريباً")

async def رمزية(update, context):
    await reply(update, "🖼️ صورة رمزية")

# ===================== القاموس الرئيسي =====================
commands = {
    "اسمي": اسمي,
    "ايديي": ايديي,
    "نقاطي": نقاطي,
    "رسائلي": رسائلي,
    "تفاعلي": تفاعلي,
    "المجموعة": المجموعة,
    "الرابط": الرابط,
    "التاريخ": التاريخ,
    "اضف_رد": اضف_رد,
    "حذف_رد": حذف_رد,
    "الردود_المتعددة": الردود_المتعددة,
    "منع": منع,
    "منع_بالرد": منع_بالرد,
    "قائمة_المنع": قائمة_المنع,
    "مسح_قائمة_المنع": مسح_قائمة_المنع,
    "تنظيف": تنظيف,
    "غنيلي": غنيلي,
    "فلم": فلم,
    "متحركة": متحركة,
    "فيديو": فيديو,
    "رمزية": رمزية
  }
