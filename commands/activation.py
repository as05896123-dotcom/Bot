from telegram import Update
from telegram.ext import ContextTypes
import json
import os
from datetime import datetime

# =====================================================
# الملفات
# =====================================================
DATA_FILE = "data/features.json"
LOG_FILE  = "data/features.log"

os.makedirs("data", exist_ok=True)

# =====================================================
# التحميل والحفظ
# =====================================================
def load():
    if not os.path.exists(DATA_FILE):
        return {}
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

FEATURES = load()

# =====================================================
# الصلاحيات
# =====================================================
ROLE_OWNER   = "owner"
ROLE_CREATOR = "creator"
ROLE_ADMIN   = "admin"

ROLE_LEVEL = {
    ROLE_ADMIN: 1,
    ROLE_CREATOR: 2,
    ROLE_OWNER: 3
}

# =====================================================
# القواعد
# =====================================================
FEATURE_RULES = {
    # مالك
    "السوبر": ROLE_OWNER,
    "all": ROLE_OWNER,
    "امسح": ROLE_OWNER,
    "ردود البوت": ROLE_OWNER,

    # منشئ
    "رفع مميز تلقائي": ROLE_CREATOR,
    "الملصق المميز": ROLE_CREATOR,
    "التشويش": ROLE_CREATOR,
    "المسح التلقائي": ROLE_CREATOR,
    "الطرد": ROLE_CREATOR,
    "الحظر": ROLE_CREATOR,
    "الكتم": ROLE_CREATOR,
    "الرفع": ROLE_CREATOR,

    # مدير
    "الايدي": ROLE_ADMIN,
    "الايدي بالصورة": ROLE_ADMIN,
    "التنظيف": ROLE_ADMIN,
    "الترحيب": ROLE_ADMIN,
    "المميزات": ROLE_ADMIN,
    "الرابط": ROLE_ADMIN,
    "صورتي": ROLE_ADMIN,
    "البايو": ROLE_ADMIN,
    "المكناسة": ROLE_ADMIN,
    "الثنائي": ROLE_ADMIN,
    "التاك التلقائي": ROLE_ADMIN,
    "الردود": ROLE_ADMIN,
    "الردود العامة": ROLE_ADMIN,
    "منو ضافني": ROLE_ADMIN,

    # تسلية
    "الالعاب": ROLE_ADMIN,
    "الالعاب الاحترافية": ROLE_ADMIN,
    "اوامر التسلية": ROLE_ADMIN,
    "النداء": ROLE_ADMIN,
    "غنيلي": ROLE_ADMIN,
    "ارسل شعر": ROLE_ADMIN,
    "ارسل ريمكس": ROLE_ADMIN,
    "ارسل متحركة": ROLE_ADMIN,
    "ارسل راب": ROLE_ADMIN,
    "ارسل ميمز": ROLE_ADMIN,
    "ارسل فيديو": ROLE_ADMIN,
    "ارسل فلم": ROLE_ADMIN,
    "ارسل صورة": ROLE_ADMIN,
}

# =====================================================
# أدوات
# =====================================================
def get_chat(chat_id):
    return FEATURES.setdefault(str(chat_id), {})

def is_enabled(chat_id, feature):
    return FEATURES.get(str(chat_id), {}).get(feature, True)

def log(chat_id, user, action, feature):
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(
            f"[{datetime.now()}] "
            f"{chat_id} | {user} | {action} | {feature}\n"
        )

def get_user_role(update: Update):
    # 🔴 اربطها بنظامك الحقيقي
    return ROLE_OWNER

def allowed(user_role, needed):
    return ROLE_LEVEL[user_role] >= ROLE_LEVEL[needed]

# =====================================================
# عرض القائمة
# =====================================================
async def اوامر_التفعيل(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
"""▸ اوامر التفعيل والتعطيل

الاستخدام:
تفعيل <الامر>
تعطيل <الامر>
حالة <الامر>
الحالات
تفعيل_الكل
تعطيل_الكل
اعادة_الضبط
"""
    )

# =====================================================
# تفعيل / تعطيل
# =====================================================
async def تفعيل(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await _toggle(update, context, True)

async def تعطيل(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await _toggle(update, context, False)

async def _toggle(update, context, value):
    if not context.args:
        return await update.message.reply_text("❌ اكتب اسم الأمر")

    feature = " ".join(context.args)
    rule = FEATURE_RULES.get(feature)

    if not rule:
        return await update.message.reply_text("❌ أمر غير معروف")

    role = get_user_role(update)
    if not allowed(role, rule):
        return await update.message.reply_text("⛔ صلاحياتك لا تسمح")

    chat = get_chat(update.effective_chat.id)
    chat[feature] = value
    save(FEATURES)

    log(update.effective_chat.id, update.effective_user.id,
        "تفعيل" if value else "تعطيل", feature)

    await update.message.reply_text(
        f"{'✅' if value else '⛔'} تم {'تفعيل' if value else 'تعطيل'} {feature}"
    )

# =====================================================
# حالة أمر
# =====================================================
async def حالة(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        return await update.message.reply_text("❌ اكتب اسم الأمر")

    feature = " ".join(context.args)
    status = is_enabled(update.effective_chat.id, feature)

    await update.message.reply_text(
        f"📊 {feature} : {'مفعل ✅' if status else 'معطل ⛔'}"
    )

# =====================================================
# عرض كل الحالات
# =====================================================
async def الحالات(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = get_chat(update.effective_chat.id)
    if not chat:
        return await update.message.reply_text("ℹ️ لا يوجد إعدادات بعد")

    text = "📊 حالات الأوامر:\n\n"
    for k, v in chat.items():
        text += f"▸ {k} : {'✅' if v else '⛔'}\n"

    await update.message.reply_text(text)

# =====================================================
# جماعي
# =====================================================
async def تفعيل_الكل(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = get_chat(update.effective_chat.id)
    for f in FEATURE_RULES:
        chat[f] = True
    save(FEATURES)
    await update.message.reply_text("✅ تم تفعيل جميع الأوامر")

async def تعطيل_الكل(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = get_chat(update.effective_chat.id)
    for f in FEATURE_RULES:
        chat[f] = False
    save(FEATURES)
    await update.message.reply_text("⛔ تم تعطيل جميع الأوامر")

# =====================================================
# إعادة ضبط
# =====================================================
async def اعادة_الضبط(update: Update, context: ContextTypes.DEFAULT_TYPE):
    FEATURES.pop(str(update.effective_chat.id), None)
    save(FEATURES)
    await update.message.reply_text("♻️ تم إعادة ضبط الإعدادات")
