from telegram import Update, ChatPermissions
from telegram.ext import ContextTypes
import re

# ================= التخزين =================
الحمايات = {}  # {chat_id: {الامر: النوع}}
مخالفات = {}   # {chat_id: {user_id: عدد المخالفات}}

# ================= القوائم =================
الاوامر_المتاحة = [
    "التاك","القناة","الصور","الرابط","الفشار","الموقع","التكرار",
    "الفيديو","الدخول","الاضافة","الاغاني","الصوت","الملفات",
    "الرسائل","الدردشة","الجهات","السيلفي","التثبيت","الشارحة",
    "الكلايش","البوتات","التوجيه","التعديل","الانلاين","المعرفات",
    "الكيبورد","الفارسية","الانكليزية","الاستفتاء","الملصقات",
    "الاشعارات","الماركداون","المتحركات"
]

انواع_الحماية = ["بالتقيد", "بالطرد", "بالكتم", "بالتقييد"]

# ================= /security =================
async def security(update: Update, context: ContextTypes.DEFAULT_TYPE):
    النص = "▸ اوامر الحماية\n\n▸ طريقة الاستخدام\n▸ قفل / فتح ← الامر\n▸ انواع الحماية\n▸ بالتقيد / بالطرد / بالكتم / بالتقييد\n\n▸ الاوامر المتاحة:\n"
    النص += "\n".join(f"▸ {امر}" for امر in الاوامر_المتاحة)
    await update.message.reply_text(نص)

# ================= قفل =================
async def قفل(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    if len(context.args) != 2:
        await update.message.reply_text("❌ الاستخدام: قفل <الأمر> <نوع الحماية>")
        return

    الامر, النوع = context.args
    if الامر not in الاوامر_المتاحة:
        await update.message.reply_text("❌ الأمر غير موجود")
        return
    if النوع not in انواع_الحماية:
        await update.message.reply_text("❌ نوع الحماية غير صحيح")
        return

    الحمايات.setdefault(chat_id, {})[الامر] = النوع
    await update.message.reply_text(f"🔒 تم قفل {الامر} {النوع}")

# ================= فتح =================
async def فتح(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    if len(context.args) != 1:
        await update.message.reply_text("❌ الاستخدام: فتح <الأمر>")
        return

    الامر = context.args[0]
    if chat_id in الحمايات and الامر in الحمايات[chat_id]:
        del الحمايات[chat_id][الامر]
        await update.message.reply_text(f"🔓 تم فتح {الامر}")
    else:
        await update.message.reply_text("ℹ️ هذا الأمر مفتوح بالفعل")

# ================= دالة تنفيذ الحماية =================
async def تنفيذ_الحماية(update: Update, الامر: str):
    chat_id = update.effective_chat.id
    النوع = الحمايات[chat_id][الامر]

    # حذف الرسالة
    await update.message.delete()

    # تسجيل المخالفة
    مخلفات_المجموعة = مخالفات.setdefault(chat_id, {})
    مخلفات_المجموعة[update.effective_user.id] = مخلفات_المجموعة.get(update.effective_user.id, 0) + 1

    # تنفيذ نوع الحماية
    if النوع == "بالطرد":
        await update.effective_chat.ban_member(update.effective_user.id)
        await update.effective_chat.send_message(f"❌ تم طرد المستخدم {update.effective_user.mention_html()}", parse_mode="HTML")
    elif النوع == "بالكتم":
        await update.effective_chat.restrict_member(
            update.effective_user.id,
            permissions=ChatPermissions(can_send_messages=False)
        )
        await update.effective_chat.send_message(f"🔇 تم كتم المستخدم {update.effective_user.mention_html()}", parse_mode="HTML")
    elif النوع in ["بالتقيد", "بالتقييد"]:
        await update.effective_chat.restrict_member(
            update.effective_user.id,
            permissions=ChatPermissions()
        )
        await update.effective_chat.send_message(f"⛔ تم تقييد المستخدم {update.effective_user.mention_html()}", parse_mode="HTML")

# ================= المراقبة =================
async def راقب(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message:
        return

    chat_id = update.effective_chat.id
    النص = update.message.text or ""
    الحماية = الحمايات.get(chat_id, {})

    # ===== تحقق كل أنواع الحماية =====
    if "الرابط" in الحماية and re.search(r"http[s]?://|t.me/", النص):
        await تنفيذ_الحماية(update, "الرابط")
    if "الصور" in الحماية and update.message.photo:
        await تنفيذ_الحماية(update, "الصور")
    if "الفيديو" in الحماية and update.message.video:
        await تنفيذ_الحماية(update, "الفيديو")
    if "الملفات" in الحماية and update.message.document:
        await تنفيذ_الحماية(update, "الملفات")
