# ============================================
# 📱 بوت التليجرام + إنشاء فيسبوك
# ============================================

import asyncio
import threading
from flask import Flask
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes
from fb_creator import FacebookCreator, Config
import logging

# ====== بيانات البوت (بتاعتك انت) ======
TOKEN = "8265031988:AAFLdci-eVMHlGU-O5K4N4se_dJFDPmRdnc"
ADMIN_ID = 5284917152

app = Flask(__name__)

# ====== تشغيل خادم ويب عشان الموقع المجاني يفضل شغال ======
@app.route('/')
def index():
    return "✅ البوت شغال يا باشا!"

# ====== أوامر البوت ======
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [[InlineKeyboardButton("🚀 إنشاء حساب فيسبوك", callback_data="fb_create")]]
    await update.message.reply_text(
        "🎯 أهلاً بك!\nاضغط الزر عشان يشتغل ويجيبلك حساب جديد.",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

async def callback_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer("⏳ جاري التجهيز...")
    await query.edit_message_text("⏳ شغال... انتظر لحظات")

    # ====== شغال إنشاء الحساب في خلفية (عشان البوت ما يعلقش) ======
    def run_creator():
        try:
            creator = FacebookCreator(Config())
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            results = loop.run_until_complete(creator.create_multiple_accounts(1))
            
            if results and results[0].status == "success":
                acc = results[0]
                context.bot.send_message(
                    query.from_user.id,
                    f"✅ **تم إنشاء الحساب بنجاح!**\n\n📧 البريد: `{acc.email}`\n🔑 الباسورد: `{acc.password}`",
                    parse_mode="Markdown"
                )
            else:
                context.bot.send_message(query.from_user.id, "❌ فشل الإنشاء، حاول تاني.")
        except Exception as e:
            context.bot.send_message(query.from_user.id, f"❌ حصل خطأ: {e}")

    threading.Thread(target=run_creator).start()

# ====== تشغيل البوت ======
def run_bot():
    application = ApplicationBuilder().token(TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(callback_handler))
    application.run_polling()

if __name__ == "__main__":
    # شغال البوت في خلفية
    threading.Thread(target=run_bot).start()
    # شغال خادم الويب عشان منصة Render تحافظ على التشغيل
    app.run(host='0.0.0.0', port=8080)
