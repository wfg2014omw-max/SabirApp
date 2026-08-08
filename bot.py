# -*- coding: utf-8 -*-

"""
================================================================================
🔥 SABIR OMEGA V18 - THE TITAN SUPREME EDITION (FULL ACCOUNT REGISTRATION + G4F AI)
================================================================================
Developer: Sabir Fathy (The Sabir Sniper)
Project: Ultimate Multi-Domain Mail & OTP Automated System & AI Assistant
Framework: Python 3.10+ / Telegram-Bot / Flask / MongoDB / G4F (GPT-4 Free)
================================================================================
"""

from pymongo import MongoClient
import certifi
import os
import re
import json
import time
import random
import string
import pyotp
import logging
import asyncio
import httpx
import sys
import threading
import io
import hashlib
from datetime import datetime, timedelta
from threading import Thread
from flask import Flask, jsonify

# ==========================================
# 🤖 استيراد مكتبة الذكاء الاصطناعي المجاني (G4F)
# ==========================================
import g4f

# Telegram Library Imports
from telegram import (
    Update, 
    ReplyKeyboardMarkup, 
    InlineKeyboardButton, 
    InlineKeyboardMarkup,
    constants
)
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters,
    CallbackQueryHandler,
    Defaults
)

# ==========================================
# ⚙️ CORE CONFIGURATION & CONSTANTS
# ==========================================
TELEGRAM_TOKEN = "8265031988:AAGAnCmpQNtFx3ZSfF_BLAiqbd5XU7jpmHI"
ADMIN_ID = 5284917152
ADMIN_USERNAME = "@SabirFathy20"

# MongoDB Configuration
MONGO_URL = "mongodb+srv://Sabir_db_user:SabirFathy%4022@sabir.lmgceju.mongodb.net/sabir_omega?retryWrites=true&w=majority&appName=Sabir"
ca = certifi.where()

# API Infrastructure
API_KEY_PRIYO = "7jkmE5NM2VS6GqJ9pzlI"
API_KEY_CYBER = "tk_0bf2b34656f5933b0015c0a4bbe026811a754c32074e4591afec8b27a293e253"

# Hugging Face AI Image Editor Config
HF_API_TOKEN = "Hf_KlwRoumAmahrrQpyjVzZevnvotGXnmguqe"
HF_MODEL_URL = "https://api-inference.huggingface.co/models/timbrooks/instruct-pix2pix"

# Domain Pools
DOMAINS_LIST = [
    "Sabir.funnylolcap.com",
    "Sabir.picturehostel.com",
    "Sabir.crazy.hcap.ai",  
    "Sabir.loganister.com", 
    "Sabir.diddyricky.com", 
    "Sabir.Wg.rexabot.com",
    "Sabir.fruitservice.xyz",
    "Sabir.kmail123.com",
]

# Logging Architecture
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[logging.FileHandler("sabir_system.log"), logging.StreamHandler()]
)
logger = logging.getLogger("SABIR_OMEGA_V18")

# ==========================================
# 🧠 AI MEMORY ENGINE (الذاكرة السياقية للذكاء الاصطناعي)
# ==========================================
user_chat_history = {}

def get_g4f_response(uid, prompt):
    if uid not in user_chat_history:
        user_chat_history[uid] = [
            {"role": "system", "content": "أنت مساعد ذكي ومحترف جداً، اسمك 'صابر AI' تابع لنظام SABIR OMEGA V18. مطورك هو Sabir Sniper. مهمتك مساعدة المستخدمين والإجابة على أسئلتهم باللغة العربية وبدقة عالية."}
        ]
    
    user_chat_history[uid].append({"role": "user", "content": prompt})
    
    if len(user_chat_history[uid]) > 11:
        user_chat_history[uid] = [user_chat_history[uid][0]] + user_chat_history[uid][-10:]
        
    try:
        response = g4f.ChatCompletion.create(
            model=g4f.models.gpt_4,
            messages=user_chat_history[uid],
            timeout=60
        )
        
        user_chat_history[uid].append({"role": "assistant", "content": response})
        return response
    except Exception as e:
        user_chat_history[uid].pop()
        raise e

def edit_image_with_ai(image_bytes, prompt):
    """
    دالة تعديل الصور المطورة:
    1. تستخدم G4F لترجمة أوامر المستخدم العربية إلى أوامر إنجليزية احترافية للـ AI.
    2. تحتوي على نظام (Retry) للانتظار إذا كان سيرفر Hugging Face يحتاج وقت للتشغيل.
    """
    headers = {"Authorization": f"Bearer {HF_API_TOKEN}"}
    
    # 1. ترجمة وفهم الطلب باستخدام GPT-4
    try:
        translation_prompt = f"Translate this image editing command to a short, direct English instruction for an AI image editor. Just return the English translation, nothing else. Command: '{prompt}'"
        english_instruction = g4f.ChatCompletion.create(
            model=g4f.models.gpt_4,
            messages=[{"role": "user", "content": translation_prompt}],
            timeout=30
        ).strip()
        # إزالة علامات التنصيص إن وجدت
        english_instruction = english_instruction.replace('"', '').replace("'", "")
    except Exception as e:
        logger.error(f"Translation failed, using original prompt: {e}")
        english_instruction = prompt

    # 2. إرسال الطلب لـ Hugging Face مع نظام إعادة المحاولة
    max_retries = 3
    for attempt in range(max_retries):
        try:
            response = httpx.post(
                HF_MODEL_URL, 
                headers=headers, 
                files={"image": ("image.jpg", image_bytes, "image/jpeg")},
                data={"inputs": english_instruction},
                timeout=120.0
            )
            
            if response.status_code == 200:
                # نجاح التعديل
                return response.content, True, english_instruction
                
            elif response.status_code == 503:
                # السيرفر نائم ويحتاج وقت للتشغيل
                logger.warning(f"HF Server is loading... attempt {attempt+1}/{max_retries}")
                time.sleep(15) # انتظار 15 ثانية قبل المحاولة التالية
                continue
                
            else:
                logger.error(f"HF API Error: {response.status_code} - {response.text}")
                return image_bytes, False, f"API Error {response.status_code}"
                
        except Exception as e:
            logger.error(f"HuggingFace Request Exception: {e}")
            return image_bytes, False, str(e)
            
    return image_bytes, False, "Server Timeout or Overloaded"

# ==========================================
# 📊 DATABASE ARCHITECTURE (MONGODB)
# ==========================================
class DatabaseManager:
    def __init__(self, uri):
        self.client = MongoClient(uri, tlsCAFile=ca)
        self.db = self.client['sabir_omega']
        self.users = self.db['users']
        self.logs = self.db['logs']
        self.tokens = self.db['tokens'] 
        self.settings = self.db['settings'] 
        self._initialize_database()

    def _initialize_database(self):
        admin = self.users.find_one({"user_id": ADMIN_ID})
        if not admin:
            self.users.insert_one({
                "user_id": ADMIN_ID,
                "username": "SabirSniper",
                "status": "active",
                "role": "admin",
                "access_type": "full",
                "domain": "Sabir.loganister.com",
                "total_mails": 0,
                "created_at": datetime.now(),
                "expire_at": None,
                # حقول الحساب المسجل
                "registered_email": "admin@sabir.com",
                "signup_username": "SabirSniper",
                "signup_password_hash": hashlib.sha256("admin123".encode()).hexdigest()
            })
        
        if not self.settings.find_one({"_id": "bot_status"}):
            self.settings.insert_one({"_id": "bot_status", "status": "active"})
            
        logger.info("MongoDB Engine Initialized & Connected.")

    def get_bot_status(self):
        doc = self.settings.find_one({"_id": "bot_status"})
        return doc.get("status", "active") if doc else "active"

    def set_bot_status(self, status):
        self.settings.update_one({"_id": "bot_status"}, {"$set": {"status": status}})

    def create_user_token(self, token_type="full"):
        token = ''.join(random.choices(string.ascii_uppercase + string.digits, k=15))
        self.tokens.insert_one({
            "token": token,
            "type": token_type,
            "used_by": None,
            "created_at": datetime.now()
        })
        return token

    def verify_and_use_token(self, token, user_id):
        doc = self.tokens.find_one({"token": token, "used_by": None})
        if doc:
            token_type = doc.get("type", "full")
            self.tokens.update_one({"token": token}, {"$set": {"used_by": user_id, "used_at": datetime.now()}})
            expire_time = datetime.now() + timedelta(hours=24)
            self.users.update_one({"user_id": int(user_id)}, {
                "$set": {
                    "status": "active", 
                    "expire_at": expire_time,
                    "access_type": token_type
                }
            })
            return True
        return False

    def activate_user_manual(self, user_id):
        expire_time = datetime.now() + timedelta(hours=24)
        self.users.update_one({"user_id": int(user_id)}, {
            "$set": {
                "status": "active", 
                "expire_at": expire_time,
                "access_type": "full"
            }
        })

    def reset_user(self, user_id):
        self.users.update_one({"user_id": int(user_id)}, {"$set": {"status": "pending", "expire_at": None}})

    def clear_all_users(self):
        self.users.delete_many({"user_id": {"$ne": ADMIN_ID}})

    def check_expired_users(self):
        expired = self.users.find({"status": "active", "expire_at": {"$lt": datetime.now()}})
        for u in expired:
            if u['user_id'] != ADMIN_ID:
                self.reset_user(u['user_id'])

    def get_user_data(self, user_id):
        return self.users.find_one({"user_id": user_id})

    def update_status(self, user_id, status):
        self.users.update_one({"user_id": int(user_id)}, {"$set": {"status": status}})

    def set_user_role(self, user_id, role):
        self.users.update_one({"user_id": int(user_id)}, {"$set": {"role": role}})

    def update_domain(self, user_id, domain):
        self.users.update_one({"user_id": user_id}, {"$set": {"domain": domain}})

    def increment_mail_count(self, user_id):
        self.users.update_one({"user_id": user_id}, {"$inc": {"total_mails": 1}})

    def fetch_admin_panel_users(self):
        self.check_expired_users() 
        return list(self.users.find({"status": {"$in": ["active", "banned"]}}))

    def fetch_all_users_for_stats(self):
        return list(self.users.find())

    def log_action(self, user_id, action):
        self.logs.insert_one({
            "user_id": user_id,
            "action": action,
            "timestamp": datetime.now()
        })
        
    def add_generated_email(self, user_id, email):
        self.users.update_one(
            {"user_id": int(user_id)}, 
            {"$addToSet": {"generated_emails": email}}
        )

    def get_user_emails(self, user_id):
        user = self.users.find_one({"user_id": int(user_id)})
        return user.get("generated_emails", []) if user else []

    # ==========================================
    # 🆕 ⭐ الوظائف الجديدة لإدارة إنشاء الحسابات ⭐
    # ==========================================
    def check_email_exists(self, email):
        """التحقق من وجود البريد الإلكتروني في قاعدة بيانات الحسابات المسجلة"""
        return self.users.find_one({"registered_email": email}) is not None

    def register_new_account(self, user_id, username, email, password_hash):
        """إنشاء حساب جديد مرتبط بـ ID التليجرام مع تشفير الباسورد"""
        try:
            self.users.update_one(
                {"user_id": int(user_id)},
                {"$set": {
                    "signup_username": username,
                    "registered_email": email,
                    "signup_password_hash": password_hash
                }}
            )
            return True
        except Exception as e:
            logger.error(f"Database Error during registration: {e}")
            return False

    def get_registered_profile(self, user_id):
        user = self.users.find_one({"user_id": int(user_id)})
        if user and user.get("registered_email"):
            return {
                "username": user.get("signup_username", "N/A"),
                "email": user.get("registered_email"),
                "registered_at": user.get("created_at")
            }
        return None

db = DatabaseManager(MONGO_URL)

# ==========================================
# 🛡️ WEB SERVER & MOBILE API (PORT 8080)
# ==========================================
app = Flask(__name__)

@app.route('/')
def index():
    return jsonify({
        "status": "Online",
        "system": "SABIR OMEGA V18",
        "developer": "Sabir Fathy",
        "database": "MongoDB Connected",
        "ai_engine": "G4F & HF Image Editor Active (Smart Retry)",
        "uptime": datetime.now().strftime("%H:%M:%S")
    })

# 📱 بوابة تطبيق الموبايل لإنشاء بريد جديد
@app.route('/api/create_email/<int:user_id>', methods=['GET'])
def api_create_email(user_id):
    user = db.get_user_data(user_id)
    if not user:
        return jsonify({"status": "error", "message": "المستخدم غير موجود"})

    prefix = ''.join(random.choices(string.ascii_lowercase + string.digits, k=10))
    current_dom = user.get('domain', 'auth2fa.com')
    email = f"{prefix}@{current_dom}"

    db.add_generated_email(user_id, email)
    return jsonify({"status": "success", "email": email})

def run_web_server():
    try:
        app.run(host='0.0.0.0', port=8080, debug=False, use_reloader=False)
    except Exception as e:
        logger.error(f"Flask Server Failure: {e}")

# ==========================================
# 📡 ENGINE: MULTI-API OTP & LINK FETCHER
# ==========================================
async def get_latest_email_content(email_address):
    async with httpx.AsyncClient(timeout=30.0, follow_redirects=True) as client:
        try:
            if "auth2fa.com" in email_address:
                api_url = f"https://free.priyo.email/api/messages/{email_address}/{API_KEY_PRIYO}"
                response = await client.get(api_url)
            else:
                api_url = "https://api.cybertemp.xyz/getMail"
                headers = {"X-API-KEY": API_KEY_CYBER}
                params = {"email": email_address, "limit": 1}
                response = await client.get(api_url, headers=headers, params=params)

            if response.status_code == 200:
                data = response.json()
                if data and isinstance(data, list) and len(data) > 0:
                    msg = data[0]
                    subj = str(msg.get('subject', 'No Subject'))
                    body_txt = str(msg.get('text', ''))
                    body_html = str(msg.get('html', ''))
                    
                    full_payload = f"{subj} {body_txt} {body_html}".lower()
                    clean_txt = re.sub(r'<[^>]+>', ' ', full_payload)
                    
                    links = re.findall(r'(https?://[^\s<>"]+)', full_payload)
                    verification_links = [l for l in links if any(word in l for word in ["verify", "click", "confirm", "activate", "discord"])]
                    
                    digits = re.findall(r'\b\d{4,8}\b', clean_txt)
                    current_year = str(datetime.now().year)
                    valid_otps = [d for d in digits if d not in [current_year, "2024", "2025", "2026", "94025"]]
                    
                    result_msg = ""
                    if verification_links:
                        result_msg += f"🔗 **رابط التفعيل المكتشف:**\n`{verification_links[0]}`\n\n"
                    
                    if valid_otps:
                        result_msg += f"🔢 **كود OTP (إلمس للنسخ):**\n`{valid_otps[0]}`\n\n"
                    
                    if not result_msg:
                        result_msg = f"📄 **محتوى الرسالة:**\n{clean_txt[:400]}..."
                    
                    return result_msg
            return None
        except Exception as e:
            logger.error(f"OTP Fetcher Error: {e}")
            return None

async def email_monitoring_loop(context, chat_id, email):
    for i in range(300): 
        await asyncio.sleep(4)
        content = await get_latest_email_content(email)
        if content:
            header = f"🚀 **صيد جديد!**\n➖➖➖➖➖➖➖➖➖➖\n📧 البريد: `{email}`\n\n"
            await context.bot.send_message(chat_id, header + content, parse_mode=constants.ParseMode.MARKDOWN)
            db.increment_mail_count(chat_id)
            db.log_action(chat_id, f"Caught mail for {email}")
            return
    await context.bot.send_message(chat_id, f"⚠️ انتهت مهلة مراقبة البريد: `{email}`")

# ==========================================
# 🎮 USER INTERFACE & KEYBOARDS
# ==========================================
def get_main_menu(uid):
    user = db.get_user_data(uid)
    role = user.get('role', 'user') if user else 'user'

    keyboard = [
        ["🆕 إنشاء بريد جديد", "🔄 استرجاع بريد سابق"],
        ["🌐 تغيير الدومين", "🔐 استخراج كود 2FA"],
        ["🆔 استخراج ID الفيس بوك", "👤 بروفيلي"],
        ["📝 إنشاء حساب جديد", "🤖 الذكاء الاصطناعي", "🎨 تعديل الصور", "🧹 مسح ذاكرة الذكاء"],
        ["🗂 إدارة الحسابات المستخدمة", "🔑 إدارة الباسوردات"]
    ]

    if uid == ADMIN_ID:
        keyboard.append(["🛠 لوحة التحكم", "📊 إحصائيات"])
        keyboard.append(["🔑 إنشاء يوزر جديد", "📢 إذاعة شاملة"])
        keyboard.append(["🛑 إيقاف للجميع", "✅ تشغيل للجميع"])
    elif role == 'reseller':
        keyboard.append(["🔑 إنشاء يوزر جديد"])
        
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True, is_persistent=True)

def get_admin_inline():
    active_banned_users = db.fetch_admin_panel_users()
    buttons = []
    
    for u in active_banned_users:
        uid = u['user_id']
        if uid == ADMIN_ID: continue  
        
        uname = u.get('username', 'Unknown')
        status = u.get('status', 'pending')
        mails = u.get('total_mails', 0)
        role = u.get('role', 'user')
        
        name_display = uname if uname != "Unknown" else f"ID:{uid}"
        icon = "✅" if status == 'active' else "⛔"
        role_icon = "⭐" if role == 'reseller' else "👤"
        
        buttons.append([InlineKeyboardButton(f"{role_icon} {icon} {name_display} | 📩 {mails}", callback_data="ignore")])
        
        control_row = []
        if status != 'active':
            control_row.append(InlineKeyboardButton(f"✅ تفعيل", callback_data=f"activate_{uid}"))
        if status != 'banned':
            control_row.append(InlineKeyboardButton(f"❌ حظر", callback_data=f"ban_{uid}"))
        control_row.append(InlineKeyboardButton(f"👁️ إخفاء", callback_data=f"hide_{uid}"))
        
        if control_row:
            buttons.append(control_row)
            
        role_row = []
        if role != 'reseller':
            role_row.append(InlineKeyboardButton(f"⭐ ترقية لموزع", callback_data=f"promote_{uid}"))
        else:
            role_row.append(InlineKeyboardButton(f"⬇️ سحب الترقية", callback_data=f"demote_{uid}"))
        buttons.append(role_row)
        
    buttons.append([InlineKeyboardButton("➕ تفعيل يدوي بالـ ID", callback_data="manual_activate")])
    buttons.append([InlineKeyboardButton("🗑 مسح جميع الأعضاء الحاليين (تصفير)", callback_data="clear_db")])
    
    return InlineKeyboardMarkup(buttons)

# ==========================================
# 🧠 CORE BOT LOGIC (HANDLERS)
# ==========================================
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = update.effective_user.id
    uname = update.effective_user.username or "Unknown"
    user_info = db.get_user_data(uid)

    if not user_info:
        status = 'active' if uid == ADMIN_ID else 'pending'
        db.users.insert_one({
            "user_id": uid,
            "username": uname,
            "status": status,
            "role": "admin" if uid == ADMIN_ID else "user",
            "access_type": "full",
            "domain": "auth2fa.com",
            "total_mails": 0,
            "created_at": datetime.now(),
            "expire_at": None
        })
        user_info = db.get_user_data(uid)
        
    if user_info['status'] == 'pending' and uid != ADMIN_ID:
        await update.message.reply_text(
            "🔒 **مرحباً بك في البوت**\n\n"
            "هذا البوت مخصص للمشتركين فقط.\n\n"
            "💰 **للاشتراك بالبوت بـ 20 جنيه في اليوم (تفعيل لمدة 24 ساعة)**\n"
            "📱 **التحويل على الرقم التالي:**\n"
            "`01144381960`\n\n"
            "📸 **يرجى إرسال صورة الدفع و ID التليجرام الخاص بك إلى المطور لتفعيل البوت.**\n"
            "👉 **أو إذا كان لديك مفتاح تفعيل مسبقاً، أرسله الآن للبدء:**",
            parse_mode=constants.ParseMode.MARKDOWN
        )
        return

    welcome_msg = (
        f"🔥 **أهلاً بك في النظام**\n"
        f"----------------------------------\n"
        f"نظام سحب الـ OTP وروابط التفعيل الأسرع.\n\n"
        f"🧠 **الذكاء الاصطناعي:** GPT-4 Active 🚀\n"
        f"🛠 **الحالة:** متصل بـ MongoDB 🚀\n\n"
        f"📝 **هل أنت مستخدم جديد؟** استخدم زر *إنشاء حساب جديد* في القائمة."
    )
    await update.message.reply_text(welcome_msg, reply_markup=get_main_menu(uid), parse_mode=constants.ParseMode.MARKDOWN)

async def message_dispatcher(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = update.effective_user.id
    msg_text = update.message.text
    if not msg_text: return

    db.check_expired_users()

    user = db.get_user_data(uid)
    if not user: return

    if user['status'] == 'pending' and uid != ADMIN_ID:
        if db.verify_and_use_token(msg_text.strip(), uid):
            await update.message.reply_text("✅ **تم تفعيل حسابك بنجاح لمدة 24 ساعة! أهلاً بك في النظام.**", reply_markup=get_main_menu(uid))
        else:
            await update.message.reply_text("❌ **المفتاح غير صحيح أو تم استخدامه من قبل. تأكد منه أو تواصل مع المطور.**")
        return

    if db.get_bot_status() == 'stopped' and uid != ADMIN_ID:
        return await update.message.reply_text("⛔ **البوت متوقف حالياً من قبل الإدارة.**")

    if user['status'] == 'banned' and uid != ADMIN_ID:
        return await update.message.reply_text("⛔ **أنت محظور من استخدام البوت.**")
        
    if user['status'] != 'active' and uid != ADMIN_ID:
        return await update.message.reply_text(
            "⛔ **حسابك غير مفعل أو انتهت صلاحيته.**\n\n"
            "💰 **للاشتراك بالبوت بـ 20 جنيه في اليوم (تفعيل لمدة 24 ساعة)**\n"
            "📱 **التحويل على الرقم:** `01144381960`\n\n"
            "📸 **يرجى إرسال صورة الدفع و ID التليجرام الخاص بك إلى المطور لتفعيل البوت.**\n"
            "👉 **أو أرسل مفتاح التفعيل الخاص بك هنا إذا كان متوفر لديك.**",
            parse_mode=constants.ParseMode.MARKDOWN
        )

    access_type = user.get('access_type', 'full')
    restricted_commands = ["🆕 إنشاء بريد جديد", "🌐 تغيير الدومين", "🆔 استخراج ID الفيس بوك", "🗂 إدارة الحسابات المستخدمة", "🎨 تعديل الصور"]

    if access_type == 'restricted' and uid != ADMIN_ID and msg_text in restricted_commands:
        return await update.message.reply_text("⛔ **عذراً، نوع اشتراكك الحالي يسمح باسترجاع البريد واستخراج كود 2FA فقط.**")

    # ================= أزرار القائمة الرئيسية =================
    if msg_text == "🆕 إنشاء بريد جديد":
        prefix = ''.join(random.choices(string.ascii_lowercase + string.digits, k=10))
        current_dom = user.get('domain', 'auth2fa.com')
        email = f"{prefix}@{current_dom}"
        
        db.add_generated_email(uid, email)
        
        await update.message.reply_text(f"📩 **بريدك الجديد:**\n`{email}`\n\n⏳ بدأت المراقبة...", parse_mode=constants.ParseMode.MARKDOWN)
        asyncio.create_task(email_monitoring_loop(context, uid, email))

    elif msg_text == "🌐 تغيير الدومين":
        buttons = [[InlineKeyboardButton(d, callback_data=f"setdom_{d}")] for d in DOMAINS_LIST]
        await update.message.reply_text("🌍 **اختر الدومين المطلوب:**", reply_markup=InlineKeyboardMarkup(buttons), parse_mode=constants.ParseMode.MARKDOWN)

    elif msg_text == "🔐 استخراج كود 2FA":
        context.user_data['sabir_state'] = 'WAIT_2FA'
        await update.message.reply_text("🔑 **أرسل كود الـ 2FA الآن:**", parse_mode=constants.ParseMode.MARKDOWN)

    elif msg_text == "🆔 استخراج ID الفيس بوك":
        context.user_data['sabir_state'] = 'WAIT_FBID'
        await update.message.reply_text("👤 **أرسل رابط الحساب المراد فحصه:**", parse_mode=constants.ParseMode.MARKDOWN)

    elif msg_text == "🗂 إدارة الحسابات المستخدمة":
        emails = db.get_user_emails(uid)
        if not emails:
            await update.message.reply_text("📭 **لم تقم بإنشاء أي حسابات بريد حتى الآن.**", parse_mode=constants.ParseMode.MARKDOWN)
        else:
            emails_list = "\n".join([f"📧 `{e}`" for e in emails])
            await update.message.reply_text(f"🗂 **قائمة الحسابات التي قمت بإنشائها مسبقاً:**\n\n{emails_list}", parse_mode=constants.ParseMode.MARKDOWN)

    elif msg_text == "🔑 إدارة الباسوردات":
        context.user_data['sabir_state'] = 'WAIT_ACCOUNTS_FOR_PASS'
        await update.message.reply_text("📝 **أرسل لستة الإيميلات أو اليوزرات في رسالة واحدة:**", parse_mode=constants.ParseMode.MARKDOWN)

    elif msg_text == "👤 بروفيلي":
        expire_txt = "غير محدود"
        if user.get('expire_at') and uid != ADMIN_ID:
            expire_txt = user['expire_at'].strftime("%Y-%m-%d %H:%M:%S")
            
        role_ar = "مدير" if uid == ADMIN_ID else ("موزع" if user.get('role') == 'reseller' else "عضو")
        type_ar = "كامل الصلاحيات" if access_type == 'full' else "استرجاع و 2FA فقط"
        
        # جلب معلومات الحساب المسجل
        reg_account = db.get_registered_profile(uid)
        acc_info = ""
        if reg_account:
            acc_info = f"📧 الإيميل المسجل: `{reg_account['email']}`\n👤 يوزر الحساب: `{reg_account['username']}`\n"
        else:
            acc_info = "⚠️ لم تقم بإنشاء حساب داخل النظام بعد. استخدم زر (إنشاء حساب جديد)."
            
        profile = (
            f"👤 **معلوماتك الشخصية:**\n"
            f"🆔 ID: `{user['user_id']}`\n"
            f"🌍 الدومين: `{user.get('domain', 'auth2fa.com')}`\n"
            f"📊 السحبات: `{user.get('total_mails', 0)}`\n"
            f"🛡️ الحالة: `{user['status']}`\n"
            f"💼 الرتبة: `{role_ar}`\n"
            f"🔑 نوع الاشتراك: `{type_ar}`\n"
            f"⏳ ينتهي في: `{expire_txt}`\n\n"
            f"--- **بيانات حسابك المسجل** ---\n"
            f"{acc_info}"
        )
        await update.message.reply_text(profile, parse_mode=constants.ParseMode.MARKDOWN)

    elif msg_text == "🔄 استرجاع بريد سابق":
        context.user_data['sabir_state'] = 'WAIT_RESTORE'
        await update.message.reply_text("📝 **أرسل البريد بالكامل لمراقبته:**", parse_mode=constants.ParseMode.MARKDOWN)
        
    elif msg_text == "🔑 إنشاء يوزر جديد" and (uid == ADMIN_ID or user.get('role') == 'reseller'):
        buttons = [
            [InlineKeyboardButton("🌟 يوزر عادي (كامل الصلاحيات)", callback_data="gentoken_full")],
            [InlineKeyboardButton("🔐 يوزر استرجاع و 2FA فقط", callback_data="gentoken_restricted")]
        ]
        await update.message.reply_text("🎯 **اختر نوع اليوزر المطلوب إنشاؤه:**", reply_markup=InlineKeyboardMarkup(buttons), parse_mode=constants.ParseMode.MARKDOWN)

    # ================= 🆕 زر إنشاء حساب جديد (التسجيل الرئيسي) =================
    elif msg_text == "📝 إنشاء حساب جديد":
        # التحقق من وجود حساب لهذا المستخدم مسبقاً
        existing_acc = db.get_registered_profile(uid)
        if existing_acc:
            await update.message.reply_text(
                f"⚠️ **لقد قمت بالفعل بإنشاء حساب مسبقاً!**\n\n"
                f"📧 الإيميل المسجل لديك هو: `{existing_acc['email']}`\n"
                f"👤 اسم المستخدم: `{existing_acc['username']}`\n\n"
                f"إذا كنت تريد تغيير بيانات الحساب، تواصل مع الإدارة.",
                parse_mode=constants.ParseMode.MARKDOWN
            )
            return
        
        # البدء بمحادثة إنشاء الحساب
        context.user_data['sabir_state'] = 'WAIT_SIGNUP_USERNAME'
        await update.message.reply_text(
            "📝 **مرحباً بك في معالج إنشاء الحساب!**\n\n"
            "الرجاء إرسال **اسم المستخدم** الذي ترغب في استخدامه في التطبيقات الخارجية (بدون مسافات):",
            parse_mode=constants.ParseMode.MARKDOWN
        )
            # ================= الذكاء الاصطناعي وتعديل الصور =================
    elif msg_text == "🤖 الذكاء الاصطناعي":
        context.user_data['sabir_state'] = 'WAIT_AI_PROMPT'
        await update.message.reply_text("✨ **مرحباً بك في قسم الذكاء الاصطناعي!** 🤖\nتحدث معي كأنك تتحدث مع خبير..", parse_mode=constants.ParseMode.MARKDOWN)

    elif msg_text == "🎨 تعديل الصور":
        context.user_data['sabir_state'] = 'WAIT_IMAGE_FOR_EDIT'
        await update.message.reply_text(
            "🖼️ **أرسل الصورة التي تريد تعديلها الآن:**\n\n"
            "💡 **أمثلة لأوامر يفهمها الذكاء الاصطناعي:**\n"
            "- حول الصورة لكرتون\n"
            "- اجعل القميص باللون الأزرق\n"
            "- اجعل الخلفية سوداء\n"
            "⚠️ ملاحظة: تعديل ومسح النصوص العربية غير مدعوم بدقة.", 
            parse_mode=constants.ParseMode.MARKDOWN
        )
        
    elif msg_text == "🧹 مسح ذاكرة الذكاء":
        if uid in user_chat_history:
            del user_chat_history[uid]
        await update.message.reply_text("🧹 **تم مسح الذاكرة بنجاح!**", parse_mode=constants.ParseMode.MARKDOWN)

    # ================= أزرار لوحة الإدارة =================
    elif uid == ADMIN_ID:
        if msg_text == "🛠 لوحة التحكم":
            await update.message.reply_text("🛠 **إدارة المستخدمين النشطين:**", reply_markup=get_admin_inline(), parse_mode=constants.ParseMode.MARKDOWN)
        elif msg_text == "🛑 إيقاف للجميع":
            db.set_bot_status('stopped')
            await update.message.reply_text("⛔ **تم إيقاف البوت لجميع المستخدمين بنجاح.**", parse_mode=constants.ParseMode.MARKDOWN)
        elif msg_text == "✅ تشغيل للجميع":
            db.set_bot_status('active')
            await update.message.reply_text("✅ **تم إعادة تشغيل البوت لجميع المستخدمين بنجاح.**", parse_mode=constants.ParseMode.MARKDOWN)
        elif msg_text == "📊 إحصائيات":
            all_u = db.fetch_all_users_for_stats()
            stat_msg = f"📊 **الإحصائيات العامة:**\n👥 إجمالي المسجلين في القاعدة: `{len(all_u)}`\n\n**تفاصيل السحبات:**\n"
            for u in all_u:
                if u.get('status') in ['active', 'banned']:
                    stat_msg += f"👤 ID: `{u['user_id']}` | سحبات: `{u.get('total_mails', 0)}`\n"
            await update.message.reply_text(stat_msg, parse_mode=constants.ParseMode.MARKDOWN)
        elif msg_text == "📢 إذاعة شاملة":
            context.user_data['sabir_state'] = 'WAIT_BC'
            await update.message.reply_text("📣 **أرسل رسالة الإذاعة:**", parse_mode=constants.ParseMode.MARKDOWN)

    # ================= 🎯 معالجة الحالات (States) للنصوص =================
    state = context.user_data.get('sabir_state')
    main_buttons = ["🤖 الذكاء الاصطناعي", "🎨 تعديل الصور", "🧹 مسح ذاكرة الذكاء", "🆕 إنشاء بريد جديد", "🔄 استرجاع بريد سابق", "🌐 تغيير الدومين", "🔐 استخراج كود 2FA", "🆔 استخراج ID الفيس بوك", "👤 بروفيلي", "🛠 لوحة التحكم", "📊 إحصائيات", "📢 إذاعة شاملة", "🗂 إدارة الحسابات المستخدمة", "🔑 إدارة الباسوردات", "🔑 إنشاء يوزر جديد", "🛑 إيقاف للجميع", "✅ تشغيل للجميع", "📝 إنشاء حساب جديد"]

    if state and msg_text not in main_buttons:
        # 🆕 حالة: إدخال اسم المستخدم
        if state == 'WAIT_SIGNUP_USERNAME':
            if not msg_text.strip() or " " in msg_text:
                await update.message.reply_text("❌ **اسم المستخدم غير صحيح.** يجب ألا يحتوي على مسافات. حاول مرة أخرى.")
                return
            context.user_data['signup_username'] = msg_text.strip()
            context.user_data['sabir_state'] = 'WAIT_SIGNUP_EMAIL'
            await update.message.reply_text("✅ **اسم المستخدم جيد!**\n\nالآن أرسل **بريدك الإلكتروني** (مثال: user@domain.com):", parse_mode=constants.ParseMode.MARKDOWN)
            
        # 🆕 حالة: إدخال البريد الإلكتروني
        elif state == 'WAIT_SIGNUP_EMAIL':
            email = msg_text.strip().lower()
            # التحقق من صحة الإيميل
            email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
            if not re.match(email_pattern, email):
                await update.message.reply_text("❌ **البريد الإلكتروني غير صحيح.** الرجاء إعادة الإرسال بصيغة صحيحة.")
                return
            
            # التحقق من وجود الإيميل في الداتابيس
            if db.check_email_exists(email):
                await update.message.reply_text("❌ **البريد الإلكتروني موجود بالفعل في قاعدة البيانات!** الرجاء استخدام إيميل آخر.")
                return
            
            context.user_data['signup_email'] = email
            context.user_data['sabir_state'] = 'WAIT_SIGNUP_PASSWORD'
            await update.message.reply_text("✅ **تم استلام الإيميل!**\n\nآخر خطوة: أرسل **كلمة المرور** (يجب ألا تقل عن 6 أحرف):", parse_mode=constants.ParseMode.MARKDOWN)

        # 🆕 حالة: إدخال كلمة المرور
        elif state == 'WAIT_SIGNUP_PASSWORD':
            password = msg_text.strip()
            if len(password) < 6:
                await update.message.reply_text("❌ **كلمة المرور قصيرة جداً.** يجب أن تكون 6 أحرف على الأقل. حاول مرة أخرى.")
                return
            
            # الحصول على البيانات من الذاكرة المؤقتة
            username = context.user_data.get('signup_username')
            email = context.user_data.get('signup_email')
            
            if not username or not email:
                await update.message.reply_text("⚠️ حدث خطأ في تسلسل الخطوات. أعد الضغط على زر 'إنشاء حساب جديد'.")
                context.user_data['sabir_state'] = None
                return
            
            # تشفير كلمة المرور وتخزينها
            password_hash = hashlib.sha256(password.encode('utf-8')).hexdigest()
            success = db.register_new_account(uid, username, email, password_hash)
            
            if success:
                await update.message.reply_text(
                    f"🎉 **مبروك! تم إنشاء حسابك بنجاح!**\n\n"
                    f"👤 الاسم: `{username}`\n"
                    f"📧 الإيميل: `{email}`\n"
                    f"🔒 تم تشفير كلمة المرور وحفظها في قاعدة البيانات.\n\n"
                    f"يمكنك الآن الضغط على '👤 بروفيلي' لعرض بياناتك المسجلة.",
                    parse_mode=constants.ParseMode.MARKDOWN
                )
                logger.info(f"User {uid} registered successfully with email {email}")
            else:
                await update.message.reply_text("❌ حدث خطأ في قاعدة البيانات أثناء التسجيل. حاول مرة أخرى لاحقاً أو اتصل بالمطور.")
            
            # تنظيف ذاكرة المستخدم
            context.user_data['sabir_state'] = None
            context.user_data['signup_username'] = None
            context.user_data['signup_email'] = None

        elif state == 'WAIT_2FA':
            try:
                totp = pyotp.TOTP(msg_text.replace(" ", "")).now()
                await update.message.reply_text(f"🔐 **الكود الحالي:** `{totp}`", parse_mode=constants.ParseMode.MARKDOWN)
            except: 
                await update.message.reply_text("❌ خطأ في الكود.")

        elif state == 'WAIT_FBID':
            found = re.findall(r'(?:id=|/)([0-9]{10,})', msg_text)
            if found: 
                await update.message.reply_text(f"✅ **ID المستخرج:** `{found[0]}`", parse_mode=constants.ParseMode.MARKDOWN)
            else: 
                await update.message.reply_text("❌ لم يتم العثور على ID.")

        elif state == 'WAIT_RESTORE':
            if "@" in msg_text:
                await update.message.reply_text(f"⏳ بدأت مراقبة: `{msg_text}`", parse_mode=constants.ParseMode.MARKDOWN)
                asyncio.create_task(email_monitoring_loop(context, uid, msg_text))

        elif state == 'WAIT_ACCOUNTS_FOR_PASS':
            context.user_data['temp_accounts'] = msg_text.split('\n')
            context.user_data['sabir_state'] = 'WAIT_PASS_FOR_ACCOUNTS'
            await update.message.reply_text("🔑 **ممتاز، الآن أرسل الباسورد الذي تريد إضافته:**", parse_mode=constants.ParseMode.MARKDOWN)

        elif state == 'WAIT_PASS_FOR_ACCOUNTS':
            accounts = context.user_data.get('temp_accounts', [])
            password = msg_text.strip()
            result = [f"{acc.split(':')[0].strip()}:{password}" for acc in accounts if acc.strip()]
            final_text = "✅ **تمت إضافة الباسورد بنجاح:**\n\n`" + "`\n`".join(result) + "`"
            await update.message.reply_text(final_text, parse_mode=constants.ParseMode.MARKDOWN)
            context.user_data['sabir_state'] = None

        elif state == 'WAIT_BC' and uid == ADMIN_ID:
            users = db.fetch_all_users_for_stats()
            for u in users:
                try: await context.bot.send_message(u['user_id'], f"📢 **إشعار إداري:**\n\n{msg_text}", parse_mode=constants.ParseMode.MARKDOWN)
                except: pass
            await update.message.reply_text("✅ تمت الإذاعة.")
            context.user_data['sabir_state'] = None

        elif state == 'WAIT_MANUAL_ACTIVATE' and uid == ADMIN_ID:
            if msg_text.isdigit():
                db.activate_user_manual(int(msg_text))
                await update.message.reply_text(f"✅ تم تفعيل `{msg_text}` لمدة 24 ساعة.", parse_mode=constants.ParseMode.MARKDOWN)
            context.user_data['sabir_state'] = None
        
        elif state == 'WAIT_AI_PROMPT':
            processing_msg = await update.message.reply_text("⏳ **جاري التفكير وتجهيز الرد...**", parse_mode=constants.ParseMode.MARKDOWN)
            try:
                ai_reply = await asyncio.to_thread(get_g4f_response, uid, msg_text)
                if len(ai_reply) > 4000:
                    for i in range(0, len(ai_reply), 4000):
                        await update.message.reply_text(ai_reply[i:i+4000])
                else:
                    await update.message.reply_text(ai_reply)
            except Exception as e:
                logger.error(f"G4F AI Error: {e}")
                await update.message.reply_text("❌ حدث خطأ أثناء الاتصال بالذكاء الاصطناعي.")
            finally:
                context.user_data['sabir_state'] = None
                try: await context.bot.delete_message(chat_id=uid, message_id=processing_msg.message_id)
                except: pass

        elif state == 'WAIT_EDIT_PROMPT':
            prompt = msg_text
            img_bytes = context.user_data.get('temp_image')
            processing_msg = await update.message.reply_text("⏳ جاري ترجمة وفهم طلبك وإرساله لسيرفرات تعديل الصور (قد يستغرق بعض الوقت إذا كان السيرفر نائماً)...")
            
            try:
                # استدعاء دالة التعديل الذكية
                edited_bytes, success, ai_info = await asyncio.to_thread(edit_image_with_ai, img_bytes, prompt)
                
                final_photo = bytes(edited_bytes)
                
                if success:
                    caption_text = (
                        "✅ **اكتمل التعديل بالذكاء الاصطناعي!**\n\n"
                        f"🧠 **ما فهمه الموديل (تمت الترجمة):**\n`{ai_info}`"
                    )
                else:
                    caption_text = (
                        "⚠️ **فشل التعديل، تم إرجاع الصورة الأصلية.**\n\n"
                        f"السبب: `{ai_info}`\n"
                        "يرجى المحاولة بأمر آخر أسهل (مثل تغيير الألوان أو الخلفية)."
                    )

                await context.bot.send_photo(
                    chat_id=uid,
                    photo=final_photo,
                    caption=caption_text,
                    parse_mode=constants.ParseMode.MARKDOWN
                )
            except Exception as e:
                logger.error(f"Image Edit Error: {e}")
                await update.message.reply_text(f"❌ حدث خطأ أثناء معالجة الصورة: {e}")
            finally:
                context.user_data['sabir_state'] = None
                context.user_data['temp_image'] = None
                try: await context.bot.delete_message(chat_id=uid, message_id=processing_msg.message_id)
                except: pass
# ==========================================
# 🖼️ مُعالج الصور (IMAGE HANDLER)
# ==========================================
async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = update.effective_user.id
    state = context.user_data.get('sabir_state')
    
    if state == 'WAIT_IMAGE_FOR_EDIT':
        try:
            photo_file = await update.message.photo[-1].get_file()
            photo_bytes = await photo_file.download_as_bytearray()
            
            context.user_data['temp_image'] = photo_bytes
            context.user_data['sabir_state'] = 'WAIT_EDIT_PROMPT'
            
            await update.message.reply_text("✍️ **ممتاز! تم استلام الصورة.**\nالآن أرسل أمر التعديل (مثال: حولها لكرتون / غيّر لون التيشيرت للأحمر):", parse_mode=constants.ParseMode.MARKDOWN)
        except Exception as e:
            logger.error(f"Photo Download Error: {e}")
            await update.message.reply_text("❌ فشل في تحميل الصورة، الرجاء المحاولة مرة أخرى.")

async def handle_callbacks(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    data = query.data
    uid = query.from_user.id
    user = db.get_user_data(uid)

    if data.startswith("setdom_"):
        db.update_domain(uid, data.split("_")[1])
        await query.answer("تم التحديث")
        await query.edit_message_text(f"✅ الدومين الحالي: `{data.split('_')[1]}`", parse_mode=constants.ParseMode.MARKDOWN)
        
    elif data.startswith("gentoken_"):
        role = user.get('role', 'user')
        if uid == ADMIN_ID or role == 'reseller':
            token_type = data.split("_")[1] 
            new_token = db.create_user_token(token_type)
            type_text = "يوزر عادي كامل" if token_type == "full" else "استرجاع و 2FA فقط"
            await query.answer("تم إنشاء المفتاح")
            await query.edit_message_text(
                f"✅ **تم إنشاء يوزر تفعيل ({type_text}):**\n\n"
                f"`{new_token}`\n\n"
                f"(صالح لمدة 24 ساعة - يستخدم لمرة واحدة فقط)", 
                parse_mode=constants.ParseMode.MARKDOWN
            )

    elif data.startswith("activate_") and uid == ADMIN_ID:
        target = data.split("_")[1]
        db.activate_user_manual(target)
        await query.answer("تم التفعيل")
        await query.edit_message_text(f"✅ تم تفعيل المستخدم `{target}` لمدة 24 ساعة.", parse_mode=constants.ParseMode.MARKDOWN)
        try: await context.bot.send_message(int(target), "🚀 مبروك! تم تفعيل حسابك بنجاح لمدة 24 ساعة من قبل الإدارة.")
        except: pass
        
    elif data.startswith("ban_") and uid == ADMIN_ID:
        target = data.split("_")[1]
        db.update_status(target, 'banned')
        await query.answer("تم الحظر")
        await query.edit_message_text(f"❌ تم حظر المستخدم `{target}`", parse_mode=constants.ParseMode.MARKDOWN)
        
    elif data.startswith("hide_") and uid == ADMIN_ID:
        target = data.split("_")[1]
        db.reset_user(target)
        await query.answer("تم الإخفاء والتصفير")
        await query.edit_message_text(f"👁️ تم إخفاء المستخدم `{target}`، الآن هو يظهر كأنه مستخدم جديد غير مفعل.", parse_mode=constants.ParseMode.MARKDOWN)
        try: await context.bot.send_message(int(target), "⚠️ **تم إنهاء جلستك.**\nبرجاء إرسال مفتاح تفعيل جديد للبدء.", parse_mode=constants.ParseMode.MARKDOWN)
        except: pass

    elif data.startswith("promote_") and uid == ADMIN_ID:
        target = data.split("_")[1]
        db.set_user_role(target, 'reseller')
        await query.answer("تمت الترقية لموزع")
        await query.edit_message_text(f"⭐ تم ترقية المستخدم `{target}` إلى موزع.", parse_mode=constants.ParseMode.MARKDOWN)
        try: 
            await context.bot.send_message(int(target), "🎉 **تمت ترقيتك إلى موزع!**\nالآن يمكنك إنشاء يوزرات تفعيل للأعضاء.", reply_markup=get_main_menu(int(target)), parse_mode=constants.ParseMode.MARKDOWN)
        except: pass

    elif data.startswith("demote_") and uid == ADMIN_ID:
        target = data.split("_")[1]
        db.set_user_role(target, 'user')
        await query.answer("تم سحب الترقية")
        await query.edit_message_text(f"⬇️ تم سحب صلاحية الموزع من المستخدم `{target}`.", parse_mode=constants.ParseMode.MARKDOWN)
        try: 
            await context.bot.send_message(int(target), "⚠️ **تم سحب صلاحية الموزع منك.**", reply_markup=get_main_menu(int(target)), parse_mode=constants.ParseMode.MARKDOWN)
        except: pass

    elif data == "clear_db" and uid == ADMIN_ID:
        db.clear_all_users()
        await query.answer("تم مسح القاعدة")
        await query.edit_message_text("🗑 **تم مسح جميع الأعضاء الحاليين وبدء نظام جديد بالكامل.**", parse_mode=constants.ParseMode.MARKDOWN)

    elif data == "manual_activate" and uid == ADMIN_ID:
        context.user_data['sabir_state'] = 'WAIT_MANUAL_ACTIVATE'
        await query.message.reply_text("👤 **أرسل الـ ID لتفعيله لمدة 24 ساعة فوراً (بدون يوزر):**", parse_mode=constants.ParseMode.MARKDOWN)

# ==========================================
# 🚀 STARTUP BOOTLOADER
# ==========================================
if __name__ == '__main__':
    Thread(target=run_web_server, daemon=True).start()

    defaults = Defaults(parse_mode=constants.ParseMode.MARKDOWN)
    sabir_app = ApplicationBuilder().token(TELEGRAM_TOKEN).defaults(defaults).build()

    sabir_app.add_handler(CommandHandler("start", start_command))
    sabir_app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), message_dispatcher))
    
    # 📸 إضافة معالج الصور
    sabir_app.add_handler(MessageHandler(filters.PHOTO, handle_photo))
    
    sabir_app.add_handler(CallbackQueryHandler(handle_callbacks))

    print("[*] SYSTEM IS READY WITH SMART AI IMAGE EDITOR & FULL ACCOUNT REGISTRATION...")
    
    sabir_app.run_polling(drop_pending_updates=True)
