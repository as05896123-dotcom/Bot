import os
import importlib
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackQueryHandler, filters, ContextTypes
from storage import add_user, add_message, cursor
from config import TOKEN

# -------- أمر /start --------
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🤖 البوت شغال")

# -------- تحميل كل الأوامر من مجلد commands --------
def تحميل_الأوامر(app: Application):
    for ملف in os.listdir("commands"):
        if ملف.endswith(".py"):
            اسم_الملف = ملف[:-3]
            module = importlib.import_module(f"commands.{اسم_الملف}")
            
            # إضافة أوامر من قاموس commands إذا موجود
            if hasattr(module, "commands"):
                for cmd_name, func in module.commands.items():
                    app.add_handler(CommandHandler(cmd_name, func))
            
            # إضافة هاندلر XO إذا موجود
            if hasattr(module, "xo_handler"):
                app.add_handler(module.xo_handler)

# -------- مراقبة الرسائل --------
async def راقب(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message is None:
        return

    user_id = update.effective_user.id
    add_user(user_id)
    add_message(user_id)
    text = update.message.text

    if not text:
        return

    # الردود المخصصة
    cursor.execute('SELECT response FROM custom_replies WHERE trigger = ?', (text,))
    row = cursor.fetchone()
    if row:
        await update.message.reply_text(row[0])

    # الأوامر المضافة
    cursor.execute('SELECT response FROM added_commands WHERE command = ?', (text,))
    row2 = cursor.fetchone()
    if row2:
        await update.message.reply_text(row2[0])

# -------- تشغيل البوت --------
def تشغيل_البوت():
    app = Application.builder().token(TOKEN).build()

    # إضافة أمر /start
    app.add_handler(CommandHandler("start", start))

    # تحميل باقي الأوامر
    تحميل_الأوامر(app)

    # مراقبة كل الرسائل
    app.add_handler(MessageHandler(filters.ALL & ~filters.COMMAND, راقب))

    print("🤖 البوت جاهز! أضف البوت لمجموعتك ورفعه كأدمن لرؤية الأوامر.")

    # تشغيل البوت
    app.run_polling()

if __name__ == "__main__":
    تشغيل_البوت()
