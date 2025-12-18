from telegram import Update
from telegram.ext import ContextTypes, MessageHandler, CommandHandler, filters

# ---------- /start ----------
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    chat = update.effective_chat

    if chat.type == "private":
        await update.message.reply_text(
            f"أهلاً يا عمري {user.first_name} 💝\nأنا البوت شغال ومستنيك تضيفني للجروب 😍"
        )
    else:
        await update.message.reply_text(
            "🤖 البوت جاهز في الجروب! ضيفوني كأدمن عشان تشوفوا كل الأوامر ويشتغل معاكم تمام 🙌"
        )

# ---------- عند إضافة البوت للجروب ----------
async def welcome_bot(update: Update, context: ContextTypes.DEFAULT_TYPE):
    for member in update.message.new_chat_members:
        if member.id == context.bot.id:
            await update.message.reply_text(
                "أهلاً يا جماعة 💝 أنا البوت شغال وجاهز 😎\nضيفوني كأدمن عشان نشوف كل الأوامر ونلعب معاكم 🙌"
            )

# ---------- القاموس الرئيسي ----------
commands = {
    "start": start
}

# ---------- هاندلر إضافي للبوت عند الانضمام ----------
handlers = [
    MessageHandler(filters.StatusUpdate.NEW_CHAT_MEMBERS, welcome_bot)
]
