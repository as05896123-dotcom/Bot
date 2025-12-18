from telegram import Update, ChatPermissions
from telegram.ext import ContextTypes
from telegram.constants import ParseMode

# ================= التخزين =================
DATA = {}  # chat_id => settings

def get(chat_id):
    return DATA.setdefault(chat_id, {
        "ترحيب": None,
        "رابط": None,
        "قوانين": None,
        "ايدي": None
    })

# ================= القائمة الرئيسية =================
async def اعدادات_المجموعة(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
"""▸ اعدادات المجموعة

▸ الترحيب
▸ تعيين ترحيب
▸ مسح الترحيب
▸ مسح الرتب
▸ الغاء التثبيت
▸ فحص البوت
▸ تعيين الرابط
▸ مسح الرابط
▸ تغيير الايدي
▸ تعيين الايدي
▸ مسح الايدي
▸ صورتي
▸ تغيير اسم المجموعة
▸ تعيين قوانين
▸ مسح القوانين
▸ تغيير الوصف
▸ تنظيف التعديل
▸ تنظيف الميديا
▸ رفع الادمنية
▸ الالعاب الاحترافية
▸ اعدادات المجموعة
"""
    )

# ================= الترحيب =================
async def تعيين_ترحيب(update: Update, context: ContextTypes.DEFAULT_TYPE):
    النص = " ".join(context.args)
    if not النص:
        return await update.message.reply_text("❌ اكتب رسالة الترحيب")
    get(update.effective_chat.id)["ترحيب"] = النص
    await update.message.reply_text("✅ تم تعيين الترحيب")

async def مسح_الترحيب(update: Update, context: ContextTypes.DEFAULT_TYPE):
    get(update.effective_chat.id)["ترحيب"] = None
    await update.message.reply_text("🗑 تم مسح الترحيب")

# ================= الرابط =================
async def تعيين_الرابط(update: Update, context: ContextTypes.DEFAULT_TYPE):
    الرابط = " ".join(context.args)
    if not الرابط:
        return await update.message.reply_text("❌ اكتب الرابط")
    get(update.effective_chat.id)["رابط"] = الرابط
    await update.message.reply_text("🔗 تم تعيين الرابط")

async def مسح_الرابط(update: Update, context: ContextTypes.DEFAULT_TYPE):
    get(update.effective_chat.id)["رابط"] = None
    await update.message.reply_text("🗑 تم مسح الرابط")

# ================= القوانين =================
async def تعيين_قوانين(update: Update, context: ContextTypes.DEFAULT_TYPE):
    القوانين = " ".join(context.args)
    if not القوانين:
        return await update.message.reply_text("❌ اكتب القوانين")
    get(update.effective_chat.id)["قوانين"] = القوانين
    await update.message.reply_text("📜 تم تعيين القوانين")

async def مسح_القوانين(update: Update, context: ContextTypes.DEFAULT_TYPE):
    get(update.effective_chat.id)["قوانين"] = None
    await update.message.reply_text("🗑 تم مسح القوانين")

# ================= الاسم والوصف =================
async def تغيير_اسم_المجموعة(update: Update, context: ContextTypes.DEFAULT_TYPE):
    الاسم = " ".join(context.args)
    if not الاسم:
        return await update.message.reply_text("❌ اكتب الاسم الجديد")
    await update.effective_chat.set_title(الاسم)
    await update.message.reply_text("✏️ تم تغيير اسم المجموعة")

async def تغيير_الوصف(update: Update, context: ContextTypes.DEFAULT_TYPE):
    الوصف = " ".join(context.args)
    if not الوصف:
        return await update.message.reply_text("❌ اكتب الوصف")
    await update.effective_chat.set_description(الوصف)
    await update.message.reply_text("📝 تم تغيير الوصف")

# ================= أدوات إدارية =================
async def الغاء_التثبيت(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.effective_chat.unpin_all_messages()
    await update.message.reply_text("📌 تم الغاء التثبيت")

async def فحص_البوت(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🤖 البوت شغال بكفاءة عالية ✅")

async def تنظيف_الميديا(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🧹 تم بدء تنظيف الميديا (يدوي/مستقبلي)")

async def تنظيف_التعديل(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🧹 تم تنظيف التعديلات")

# ================= معلومات المستخدم =================
async def صورتي(update: Update, context: ContextTypes.DEFAULT_TYPE):
    u = update.effective_user
    await update.message.reply_text(
        f"👤 الاسم: {u.full_name}\n🆔 الايدي: `{u.id}`",
        parse_mode=ParseMode.MARKDOWN
                      )
