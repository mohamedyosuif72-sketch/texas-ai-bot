import anthropic
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes, CallbackQueryHandler

TELEGRAM_TOKEN = "9106780728:AAGDA_E_CU6t-nB6e7eLEPvl939XSpcmnNM"
ANTHROPIC_API_KEY = "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"

client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)
history = {}
SYSTEM = """أنت TEXAS AI مساعد تنفيذي ذكي باللغة العربية.
متخصص في: إدارة الأعمال، صناعة المحتوى، التقارير اليومية، إدارة المهام، جامعة بحري، وإدارة الموارد البشرية."""

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    kb = [[InlineKeyboardButton("✍️ محتوى", callback_data="content"), InlineKeyboardButton("💼 أعمال", callback_data="business")],
          [InlineKeyboardButton("📊 تقرير", callback_data="report"), InlineKeyboardButton("✅ مهام", callback_data="tasks")],
          [InlineKeyboardButton("🎓 الجامعة", callback_data="university")]]
    await update.message.reply_text("🤖 TEXAS AI | المساعد التنفيذي\n\nمرحباً! اكتب سؤالك أو اختر 👇",
                                     reply_markup=InlineKeyboardMarkup(kb))

async def chat(update: Update, context: ContextTypes.DEFAULT_TYPE, text: str):
    uid = update.effective_user.id
    if uid not in history: history[uid] = []
    history[uid].append({"role": "user", "content": text})
    if len(history[uid]) > 20: history[uid] = history[uid][-20:]
    msg = await update.effective_message.reply_text("⏳ جاري المعالجة...")
    try:
        r = client.messages.create(model="claude-sonnet-4-6", max_tokens=1000, system=SYSTEM, messages=history[uid])
        reply = r.content[0].text
        history[uid].append({"role": "assistant", "content": reply})
        await msg.delete()
        await update.effective_message.reply_text(reply)
    except Exception as e:
        await msg.delete()
        await update.effective_message.reply_text(f"❌ خطأ: {e}")

async def handle(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await chat(update, context, update.message.text)

async def callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.callback_query.answer()
    msgs = {"content": "ساعدني في صناعة محتوى إبداعي", "business": "ساعدني في إدارة أعمالي",
            "report": "أنشئ تقرير يومي احترافي", "tasks": "ساعدني في إدارة مهامي",
            "university": "ساعدني في مواد إدارة الموارد البشرية في جامعة بحري"}
    if update.callback_query.data in msgs:
        await chat(update, context, msgs[update.callback_query.data])

if __name__ == "__main__":
    app = Application.builder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(callback))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle))
    print("✅ TEXAS AI يعمل!")
    app.run_polling()
