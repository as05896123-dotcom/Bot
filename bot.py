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
from commands.group_settings import *

app.add_handler(CommandHandler("اعدادات_المجموعة", اعدادات_المجموعة_cmd))
app.add_handler(CommandHandler("تعيين_ترحيب", تعيين_ترحيب))
app.add_handler(CommandHandler("مسح_الترحيب", مسح_الترحيب))
app.add_handler(CommandHandler("تعيين_الرابط", تعيين_الرابط))
app.add_handler(CommandHandler("مسح_الرابط", مسح_الرابط))
app.add_handler(CommandHandler("تعيين_قوانين", تعيين_قوانين))
app.add_handler(CommandHandler("مسح_القوانين", مسح_القوانين))
app.add_handler(CommandHandler("تغيير_اسم_المجموعة", تغيير_اسم_المجموعة))
app.add_handler(CommandHandler("تغيير_الوصف", تغيير_الوصف))
app.add_handler(CommandHandler("فحص_البوت", فحص_البوت))
app.add_handler(CommandHandler("صورتي", صورتي))
from commands.security import security, قفل, فتح, راقب
from telegram.ext import CommandHandler, MessageHandler, filters

app.add_handler(CommandHandler("security", security))
app.add_handler(CommandHandler("قفل", قفل))
app.add_handler(CommandHandler("فتح", فتح))
app.add_handler(MessageHandler(filters.ALL, راقب))
from telegram.ext import CommandHandler
from commands.group_settings import *

handlers = [
    ("اعدادات_المجموعة", اعدادات_المجموعة),
    ("تعيين_ترحيب", تعيين_ترحيب),
    ("مسح_الترحيب", مسح_الترحيب),
    ("تعيين_الرابط", تعيين_الرابط),
    ("مسح_الرابط", مسح_الرابط),
    ("تعيين_قوانين", تعيين_قوانين),
    ("مسح_القوانين", مسح_القوانين),
    ("تغيير_اسم_المجموعة", تغيير_اسم_المجموعة),
    ("تغيير_الوصف", تغيير_الوصف),
    ("الغاء_التثبيت", الغاء_التثبيت),
    ("فحص_البوت", فحص_البوت),
    ("تنظيف_الميديا", تنظيف_الميديا),
    ("تنظيف_التعديل", تنظيف_التعديل),
    ("صورتي", صورتي)
]

for cmd, func in handlers:
    app.add_handler(CommandHandler(cmd, func))
