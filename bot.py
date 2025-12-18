import os
import importlib
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackQueryHandler, filters, ContextTypes
from storage import *
from config import TOKEN

# -------- تحميل كل الأوامر من مجلد commands --------
def تحميل_الأوامر(app):
    for ملف in os.listdir("commands"):
        if ملف.endswith(".py"):
            اسم_الملف = ملف[:-3]
            module = importlib.import_module(f"commands.{اسم_الملف}")
            # يفترض أن كل ملف فيه قاموس commands
            if hasattr(module, "commands"):
                for cmd_name, func in module.commands.items():
                    app.add_handler(CommandHandler(cmd_name, func))
            # إذا كان هناك هاندلر XO
            if hasattr(module, "xo_handler"):
                app.add_handler(module.xo_handler)

# -------- مراقبة الرسائل (لتفعيل نقاط، الردود، التنظيف، المنع) --------
async def راقب(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    add_user(user_id)
    add_message(user_id)
    text = update.message.text
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
    # المراقبة لأي إضافات مستقبلية
    return

# -------- تشغيل البوت --------
def تشغيل_البوت():
    app = Application.builder().token(TOKEN).build()

    # تحميل كل الأوامر من commands
    تحميل_الأوامر(app)

    # مراقبة كل الرسائل
    app.add_handler(MessageHandler(filters.ALL, راقب))

    # رسالة ترحيب عند تشغيل البوت
    print("🤖 البوت جاهز! أضف البوت لمجموعتك ورفعه كأدمن لرؤية الأوامر.")

    # تشغيل البوت
    app.run_polling()

if __name__ == "__main__":
    تشغيل_البوت()
