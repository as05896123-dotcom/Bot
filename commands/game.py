from storage import *
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes, CallbackQueryHandler
import random

# ===================== دوال مساعدة =====================
async def reply(update, text):
    if update.message:
        await update.message.reply_text(text)
    elif update.callback_query:
        await update.callback_query.message.reply_text(text)

async def register_user(update):
    user_id = update.effective_user.id
    add_user(user_id)

def add_game_points(user_id, pts):
    add_points(user_id, pts)
    msgs = pts * 25
    add_message(user_id)
    return msgs

# ===================== الألعاب =====================
async def العكس(update, context):
    await register_user(update)
    if not context.args:
        await reply(update, "اكتب كلمة لعكسها: /العكس كلمة")
        return
    word = " ".join(context.args)
    reversed_word = word[::-1]
    pts = add_game_points(update.effective_user.id, 1)
    await reply(update, f"🔄 الكلمة: {word}\n♻️ معكوسة: {reversed_word}\n🎯 نقاطك: 1 → {pts} رسالة")

async def معاني(update, context):
    await register_user(update)
    emojis = {"🍎": "تفاحة", "🐱": "قط", "⚽": "كرة القدم"}
    key, value = random.choice(list(emojis.items()))
    pts = add_game_points(update.effective_user.id, 1)
    await reply(update, f"❓ {key} معناها؟\n✅ الإجابة: {value}\n🎯 نقاطك: 1 → {pts} رسالة")

async def حزورة(update, context):
    await register_user(update)
    riddles = {"ما هو الشيء الذي له أسنان لكنه لا يعض؟": "المشط",
               "شيء نراه في الليل لكنه ليس في النهار؟": "القمر"}
    question, answer = random.choice(list(riddles.items()))
    pts = add_game_points(update.effective_user.id, 1)
    await reply(update, f"❓ {question}\n✅ الإجابة: {answer}\n🎯 نقاطك: 1 → {pts} رسالة")

# -------- XO مع كيبورد تفاعلي --------
xo_games = {}

def generate_xo_keyboard(board):
    keyboard = []
    for i in range(3):
        row = []
        for j in range(3):
            cell = board[i][j] if board[i][j] else "⬜"
            row.append(InlineKeyboardButton(cell, callback_data=f"{i},{j}"))
        keyboard.append(row)
    return InlineKeyboardMarkup(keyboard)

async def اكس_او(update, context):
    await register_user(update)
    user_id = update.effective_user.id
    board = [[None]*3 for _ in range(3)]
    xo_games[user_id] = board
    keyboard = generate_xo_keyboard(board)
    await update.message.reply_text("🎮 XO: اضغط على الخانة للعب", reply_markup=keyboard)

async def xo_callback(update, context):
    query = update.callback_query
    await query.answer()
    user_id = query.from_user.id
    if user_id not in xo_games:
        await query.edit_message_text("⚠️ لم تبدأ اللعبة! اكتب /اكس او")
        return
    board = xo_games[user_id]
    i,j = map(int, query.data.split(","))
    if board[i][j]:
        return
    board[i][j] = "❌"
    empty = [(x,y) for x in range(3) for y in range(3) if not board[x][y]]
    if empty:
        x,y = random.choice(empty)
        board[x][y] = "⭕"
    keyboard = generate_xo_keyboard(board)
    winner = check_xo_winner(board)
    if winner:
        pts = add_game_points(user_id, 1)
        await query.edit_message_text(f"🎉 {winner} فاز!\n🎯 نقاطك: 1 → {pts} رسالة")
        del xo_games[user_id]
    else:
        await query.edit_message_text("🎮 XO: اضغط على الخانة للعب", reply_markup=keyboard)

def check_xo_winner(board):
    for row in board:
        if row[0] and row.count(row[0])==3:
            return "❌ اللاعب" if row[0]=="❌" else "⭕ البوت"
    for col in range(3):
        if board[0][col] and all(board[r][col]==board[0][col] for r in range(3)):
            return "❌ اللاعب" if board[0][col]=="❌" else "⭕ البوت"
    if board[0][0] and board[0][0]==board[1][1]==board[2][2]:
        return "❌ اللاعب" if board[0][0]=="❌" else "⭕ البوت"
    if board[0][2] and board[0][2]==board[1][1]==board[2][0]:
        return "❌ اللاعب" if board[0][2]=="❌" else "⭕ البوت"
    return None

async def روليت(update, context):
    await register_user(update)
    outcomes = ["💰 ربح","💸 خسر","🎯 حاول مرة أخرى"]
    outcome = random.choices(outcomes, weights=[0.4,0.4,0.2])[0]
    pts = add_game_points(update.effective_user.id, 1)
    await reply(update, f"🎰 روليت: {outcome}\n🎯 نقاطك: 1 → {pts} رسالة")

async def حجرة(update, context):
    await register_user(update)
    choices = ["حجرة","ورقة","مقص"]
    player = random.choice(choices)
    bot_choice = random.choice(choices)
    result = determine_rps(player, bot_choice)
    pts = add_game_points(update.effective_user.id, 1)
    await reply(update,f"✊ {player} vs {bot_choice}\n✅ النتيجة: {result}\n🎯 نقاطك: 1 → {pts} رسالة")

def determine_rps(player, bot_choice):
    if player==bot_choice: return "تعادل"
    if (player=="حجرة" and bot_choice=="مقص") or (player=="ورقة" and bot_choice=="حجرة") or (player=="مقص" and bot_choice=="ورقة"):
        return "فوزك"
    return "خسارتك"

async def صراحة(update, context):
    await register_user(update)
    questions = ["ما هو سرّك؟","من تحب أكثر؟","أفضل صديق لك؟"]
    question = random.choice(questions)
    pts = add_game_points(update.effective_user.id, 1)
    await reply(update,f"❓ صراحة: {question}\n🎯 نقاطك: 1 → {pts} رسالة")

async def رياضيات(update, context):
    await register_user(update)
    a,b = random.randint(1,10), random.randint(1,10)
    pts = add_game_points(update.effective_user.id, 1)
    await reply(update,f"❓ احسب: {a} + {b} = ?\n✅ الإجابة: {a+b}\n🎯 نقاطك: 1 → {pts} رسالة")

# ===================== قاموس الألعاب بدون فواصل =====================
commands = {
    "العكس": العكس
    "معاني": معاني
    "حزورة": حزورة
    "اكس او": اكس_او
    "روليت": روليت
    "حجرة": حجرة
    "صراحة": صراحة
    "رياضيات": رياضيات
}

xo_handler = CallbackQueryHandler(xo_callback)
