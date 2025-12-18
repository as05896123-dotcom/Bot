from telegram import Update
from telegram.constants import ChatPermissions
from telegram.ext import ContextTypes
import re

# ================= التخزين =================
الحمايات = {}  # {chat_id: {الامر: النوع}}

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
    النص = """▸ اوامر الحماية

▸ طريقة الاستخدام
▸ قفل / فتح ← الامر
▸ انواع الحماية
▸ بالتقيد / بالطرد / بالكتم / بالتقييد

▸ الاوامر المتاحة
"""
    for امر in الاوامر_المتاحة:
        النص += f"▸ {امر}\n"

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

# ================= المراقبة (التنفيذ الفعلي) =================
async def راقب(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message:
        return

    chat_id = update.effective_chat.id
    النص = update.message.text or ""
    الحماية = الحمايات.get(chat_id, {})

    # ===== حماية الروابط =====
    if "الرابط" in الحماية:
        if re.search(r"http[s]?://|t.me/", النص):
            await update.message.delete()
            النوع = الحماية["الرابط"]

            if النوع == "بالطرد":
                await update.effective_chat.ban_member(update.effective_user.id)

            elif النوع == "بالكتم":
                await update.effective_chat.restrict_member(
                    update.effective_user.id,
                    ChatPermissions(can_send_messages=False)
                )

            elif النوع in ["بالتقيد", "بالتقييد"]:
                await update.effective_chat.restrict_member(
                    update.effective_user.id,
                    ChatPermissions()
                )

    # ===== حماية الصور =====
    if "الصور" in الحماية and update.message.photo:
        await update.message.delete()
        النوع = الحماية["الصور"]

        if النوع == "بالطرد":
            await update.effective_chat.ban_member(update.effective_user.id)

        elif النوع == "بالكتم":
            await update.effective_chat.restrict_member(
                update.effective_user.id,
                ChatPermissions(can_send_messages=False)
            )

        elif النوع in ["بالتقيد", "بالتقييد"]:
            await update.effective_chat.restrict_member(
                update.effective_user.id,
                ChatPermissions()
  )
