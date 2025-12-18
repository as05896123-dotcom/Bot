import os
import importlib
from telegram.ext import Application, CommandHandler, MessageHandler, filters
from storage import الحمايات, اعدادات_المجموعة
from config import TOKEN

# دالة لتحميل جميع الأوامر تلقائيًا من مجلد commands
def تحميل_الأوامر(app):
    for ملف in os.listdir("commands"):
        if ملف.endswith(".py"):
            اسم_الملف = ملف[:-3]
            module = importlib.import_module(f"commands.{اسم_الملف}")
            # يفترض أن كل ملف فيه دالة بنفس اسم الملف
            handler = CommandHandler(اسم_الملف, getattr(module, اسم_الملف))
            app.add_handler(handler)

# دالة مراقبة الرسائل الأساسية (تقدر تضيف الحماية لاحقًا)
async def راقب(update, context):
    pass

# تشغيل البوت
def تشغيل_البوت():
    app = Application.builder().token(TOKEN).build()

    # تحميل كل الأوامر
    تحميل_الأوامر(app)

    # مراقبة كل الرسائل
    app.add_handler(MessageHandler(filters.ALL, راقب))

    # رسالة ترحيبية عند تشغيل البوت
    print("🤖 مرحبًا في بوت الحماية! يرجى إضافة البوت لمجموعتك ورفع البوت كأدمن لرؤية الأوامر.")

    app.run_polling()

if __name__ == "__main__":
    تشغيل_البوت()
