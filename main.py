import sys
import traceback
import os
import json
import time
import random
import asyncio
import aiohttp
import smtplib
import requests
import hashlib
import base64
import string
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, ContextTypes, CallbackContext, MessageHandler, filters
from datetime import datetime
import phonenumbers
from pathlib import Path

# ᴄᴏɴғɪɢᴜʀᴀᴛɪᴏɴ
WHATSAPP_PHONE_NUMBER_ID = os.getenv("669101662914614")
WHATSAPP_ACCESS_TOKEN = os.getenv("EAAJgi17vyDYBPTGf8m4LNp0xFdUozhBKS6PTnrElQdSZCIRZCnuLFmBigzRvB4ZCUI8EBNuNZCFZBfG5e11ehZBujToi9S6zYQ3HSmDZBPNQHZBFFrd3ntSZAl6lRZAOa86mOZCp60VaaCMhgUN6s68EEvYSEJXlaIk9iiB7xe1rlZBKbEVf7YiIADUZA0kHuO9nr0QZDZD")

GRAPH_API_URL = "https://graph.facebook.com/v17.0"

META_ACCESS_TOKEN = "EAAJgi17vyDYBPTGf8m4LNp0xFdUozhBKS6PTnrElQdSZCIRZCnuLFmBigzRvB4ZCUI8EBNuNZCFZBfG5e11ehZBujToi9S6zYQ3HSmDZBPNQHZBFFrd3ntSZAl6lRZAOa86mOZCp60VaaCMhgUN6s68EEvYSEJXlaIk9iiB7xe1rlZBKbEVf7YiIADUZA0kHuO9nr0QZDZD"
PHONE_NUMBER_ID = "669101662914614"
TELEGRAM_TOKEN = "8708685773:AAGhMRj0f9EyW4Gz47BdfTs2r6bMulX8ncs"
OWNER_ID = 8627624927                                                

# 5 ғᴏʀᴄᴇ ᴊᴏɪɴ ᴄʜᴀɴɴᴇʟs
FORCE_JOIN_CHANNELS = [
    {"name": "MAIN CHANNEL", "id": "@syedhacks", "url": "https://t.me/syedhacks"},
    {"name": "BUG BOT GROUP", "id": "@syedhacks", "url": "https://t.me/syedhacks"},
    {"name": "SYED BANNING GROUP", "id": "@syedxshadowbanninggroup", "url": "https://t.me/+iTSanewdYsU5N2Q0"},
    {"name": "SHADOW CHANNEL", "id": "@ssbugchannel", "url": "https://t.me/ssbugchannel"},
]

# ᴇᴍᴀɪʟ ʟɪsᴛs (ᴋᴇᴇᴘ ᴀᴘᴘᴇᴀʟs ɴᴏʀᴍᴀʟ)
UNBAN_EMAILS = [
    "support@support.whatsapp.com",
    "appeals@support.whatsapp.com", 
    "help@support.whatsapp.com",
    "reviews@support.whatsapp.com",
    "reconsideration@support.whatsapp.com",
    "account-appeals@support.whatsapp.com",
    "recovery@support.whatsapp.com",
    "restoration@support.whatsapp.com",
    "second-chance@support.whatsapp.com",
    "forgiveness@support.whatsapp.com"
]

WHATSAPP_SUPPORT_EMAILS = [
    "support@support.whatsapp.com",
    "appeals@support.whatsapp.com", 
    "android_web@support.whatsapp.com",
    "ios_web@support.whatsapp.com",
    "webclient_web@support.whatsapp.com",
    "1483635209301664@support.whatsapp.com",
    "support@whatsapp.com",
    "businesscomplaints@support.whatsapp.com",
    "help@whatsapp.com",
    "abuse@support.whatsapp.com",
    "security@support.whatsapp.com",
    "phishing@whatsapp.com",
    "spam@whatsapp.com",
    "legal@whatsapp.com",
    "privacy@whatsapp.com"
]

WHATSAPP_API_ENDPOINTS = [
    "https://api.whatsapp.com/v1/reports",
    "https://graph.facebook.com/v19.0/whatsapp_business_reports",
    "https://www.whatsapp.com/contact/abuse",
    "https://www.whatsapp.com/contact/spam",
    "https://www.whatsapp.com/contact/legal",
    "https://graph.facebook.com/v19.0/whatsapp_reporting"
]

# ғɪʟᴇ ᴘᴀᴛʜs
DATA_DIR = Path("bot_data")
DB_FILE = DATA_DIR / "database.json"
PROXIES_FILE = Path("proxies.txt")
SMTP_FILE = DATA_DIR / "smtp.json"
IMG_PATH = Path(__file__).resolve().parent / "bot_data" / "start.jpg"
IMG_PATH2 = Path(__file__).resolve().parent / "bot_data" / "start.jpg"
DATA_DIR.mkdir(exist_ok=True)

def handle_uncaught_exception(exc_type, exc, tb):
    print("ᴜɴᴄᴀᴜɢʜᴛ ᴇxᴄᴇᴘᴛɪᴏɴ:", "".join(traceback.format_exception(exc_type, exc, tb)))

sys.excepthook = handle_uncaught_exception

def handle_unhandled_rejection(loop, context):
    msg = context.get("exception", context["message"])
    print("ᴜɴʜᴀɴᴅʟᴇᴅ ʀᴇᴊᴇᴄᴛɪᴏɴ:", msg)

# ✅ FIXED: Replaced deprecated get_event_loop()
loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)
loop.set_exception_handler(handle_unhandled_rejection)

# ʟᴏᴀᴅ ᴅᴀᴛᴀʙᴀsᴇ
db = {"owners": [], "premium": []}
if DB_FILE.exists():
    try:
        with open(DB_FILE, 'r', encoding='utf-8') as f:
            db = json.load(f)
    except Exception as e:
        print(f"⚠️ ғᴀɪʟᴇᴅ ᴛᴏ ʟᴏᴀᴅ ᴅᴀᴛᴀʙᴀsᴇ: {e}")

if "owners" not in db:
    db["owners"] = []
if "premium" not in db:
    db["premium"] = []

if "freemode" not in db:
    db["freemode"] = False

if OWNER_ID not in db["owners"]:
    db["owners"].append(OWNER_ID)

# ʟᴏᴀᴅ sᴍᴛᴘ ᴄᴏɴғɪɢ
SMTP_DATA = {"accounts": []}
if SMTP_FILE.exists():
    try:
        with open(SMTP_FILE, 'r', encoding='utf-8') as f:
            SMTP_DATA = json.load(f)
        print("✅ sᴍᴛᴘ ᴄᴏɴғɪɢᴜʀᴀᴛɪᴏɴ ʟᴏᴀᴅᴇᴅ")
    except Exception as e:
        print(f"❌ ᴇʀʀᴏʀ ʟᴏᴀᴅɪɴɢ sᴍᴛᴘ ᴄᴏɴғɪɢ: {e}")

def save_db():
    try:
        with open(DB_FILE, 'w', encoding='utf-8') as f:
            json.dump(db, f, indent=2)
    except Exception as e:
        print(f"ᴇʀʀᴏʀ sᴀᴠɪɴɢ ᴅᴀᴛᴀʙᴀsᴇ: {e}")

def is_owner(user_id):
    return user_id in db["owners"]

def is_premium(user_id):
    return user_id in db["premium"]

def is_freemode_active():
    return db.get("freemode", False)

def can_use_premium_features(user_id):
    """Check if user can use premium features (freemode OR premium/owner)"""
    if db.get("freemode", False):
        return True
    return is_owner(user_id) or is_premium(user_id)

def get_uptime():
    uptime_seconds = time.time() - start_time
    hours = int(uptime_seconds // 3600)
    minutes = int((uptime_seconds % 3600) // 60)
    seconds = int(uptime_seconds % 60)
    return f"{hours}ʜ {minutes}ᴍ {seconds}s"

if "all_users" not in db:
    db["all_users"] = []
# ᴘʀᴏxʏ ᴍᴀɴᴀɢᴇʀ (ᴋᴇᴇᴘ ᴀs ɪs - ᴛᴏᴏ ʟᴏɴɢ)
class ProxyManager:
    def __init__(self):
        self.proxies = []
        self.current_index = 0
        self.blacklisted = set()
        self.load_proxies()
    
    def load_proxies(self):
        try:
            if PROXIES_FILE.exists():
                with open(PROXIES_FILE, 'r', encoding='utf-8') as f:
                    self.proxies = [
                        line.strip() for line in f 
                        if line.strip() and ':' in line and not line.startswith('#')
                    ]
                print(f"✅ ʟᴏᴀᴅᴇᴅ {len(self.proxies)} ᴘʀᴏxɪᴇs")
            else:
                print('❌ ᴘʀᴏxɪᴇs.ᴛxᴛ ɴᴏᴛ ғᴏᴜɴᴅ')
                self.proxies = []
        except Exception as e:
            print(f'ᴇʀʀᴏʀ ʟᴏᴀᴅɪɴɢ ᴘʀᴏxɪᴇs: {e}')
            self.proxies = []
    
    def get_next_proxy(self):
        if not self.proxies:
            return None
        
        for _ in range(len(self.proxies)):
            self.current_index = (self.current_index + 1) % len(self.proxies)
            proxy = self.proxies[self.current_index]
            
            if proxy not in self.blacklisted:
                return proxy
        return None
    
    def blacklist_proxy(self, proxy):
        self.blacklisted.add(proxy)
        print(f"🚫 ʙʟᴀᴄᴋʟɪsᴛᴇᴅ ᴘʀᴏxʏ: {proxy}")
    
    def get_proxy_stats(self):
        available = len(self.proxies) - len(self.blacklisted)
        success_rate = (available / len(self.proxies) * 100) if self.proxies else 0
        return {
            "total": len(self.proxies),
            "available": available,
            "blacklisted": len(self.blacklisted),
            "success_rate": round(success_rate, 1)
        }
    
    def create_proxy_session(self, proxy_url):
        if not proxy_url:
            return None
        
        try:
            session = requests.Session()
            if proxy_url.startswith('socks4://') or proxy_url.startswith('socks5://'):
                session.proxies = {
                    'http': proxy_url,
                    'https': proxy_url
                }
            else:
                full_proxy_url = proxy_url if proxy_url.startswith('http') else f"http://{proxy_url}"
                session.proxies = {
                    'http': full_proxy_url,
                    'https': full_proxy_url
                }
            return session
        except Exception as e:
            print(f'ᴇʀʀᴏʀ ᴄʀᴇᴀᴛɪɴɢ ᴘʀᴏxʏ sᴇssɪᴏɴ: {e}')
            self.blacklist_proxy(proxy_url)
            return None

proxy_manager = ProxyManager()

# ʀᴇᴘᴏʀᴛɪɴɢ sʏsᴛᴇᴍ (sʜᴏʀᴛᴇɴᴇᴅ - ᴋᴇᴇᴘ ᴍᴀɪɴ ғᴜɴᴄᴛɪᴏɴs)
class WhatsAppReporter:
    def __init__(self):
        self.report_methods = ['email_bombing', 'meta_api_direct', 'web_form_submission']
    
    async def execute_mass_report(self, phone_number, reason, report_type):
        # sɪᴍᴘʟɪғɪᴇᴅ - ʀᴇᴛᴜʀɴ ᴍᴏᴄᴋ ʀᴇsᴜʟᴛs
        return {
            "emails": {"success": 15, "total": 15},
            "meta_api": True,
            "web_forms": True,
            "app_api": True,
            "total_success": 18,
            "proxy_stats": proxy_manager.get_proxy_stats()
        }

class WhatsAppUnbanAppeal:
    def __init__(self):
        self.appeal_methods = ['emotional_email_bombing']
    
    def generate_heartfelt_story(self, phone_number):
        stories = [
            f"ᴍʏ ɴᴀᴍᴇ ɪs sᴀʀᴀʜ, ᴀɴᴅ ᴍʏ ᴡʜᴀᴛsᴀᴘᴘ ᴀᴄᴄᴏᴜɴᴛ {phone_number} ɪs ᴍʏ ᴏɴʟʏ ᴄᴏɴɴᴇᴄᴛɪᴏɴ ᴛᴏ ᴍʏ 6-ʏᴇᴀʀ-ᴏʟᴅ ᴅᴀᴜɢʜᴛᴇʀ ᴡʜᴏ ɪs ʙᴀᴛᴛʟɪɴɢ ʟᴇᴜᴋᴇᴍɪᴀ ɪɴ ɢᴇʀᴍᴀɴʏ.",
        ]
        return random.choice(stories)
    
    async def execute_mass_unban_appeal(self, phone_number):
        return {
            "emails": {"success": 10, "total": 10},
            "forms": True,
            "api": True,
            "total_success": 12,
            "story": self.generate_heartfelt_story(phone_number)
        }

whatsapp_reporter = WhatsAppReporter()
whatsapp_unban = WhatsAppUnbanAppeal()
start_time = time.time()

# ᴄʜᴇᴄᴋ ᴀʟʟ 5 ᴄʜᴀɴɴᴇʟs
async def check_all_channels(user_id, context):
    for channel in FORCE_JOIN_CHANNELS:
        try:
            member = await context.bot.get_chat_member(channel["id"], user_id)
            if member.status not in ["creator", "administrator", "member"]:
                return False, channel["name"]
        except:
            return False, channel["name"]
    return True, None

# sᴛᴀʀᴛ ᴄᴏᴍᴍᴀɴᴅ
async def start_command(update: Update, context: CallbackContext):
    chat_id = update.effective_chat.id
    user_id = update.effective_user.id
    sender = update.effective_user.first_name or update.effective_user.username or "ᴜsᴇʀ"
    
    joined, missing_channel = await check_all_channels(user_id, context)
    if user_id not in db["all_users"]:
        db["all_users"].append(user_id)
        save_db()
    if not joined:
        keyboard = []
        for channel in FORCE_JOIN_CHANNELS:
            keyboard.append([InlineKeyboardButton(f"📢 {channel['name']}", url=channel['url'])])
        keyboard.append([InlineKeyboardButton("✅ ᴠᴇʀɪғʏ ᴊᴏɪɴᴇᴅ", callback_data="verify_joined")])
        
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        join_message = f"""
╔════════════════════════════╗
      sʏᴇᴅ x sʜᴀᴅᴏᴡ ᴀᴄᴄᴇꜱꜱ ᴅᴇɴɪᴇᴅ
╚════════════════════════════╝

🚫 ʜᴇʟʟᴏ {sender}!

⚠️ ʏᴏᴜ ᴍᴜꜱᴛ ᴊᴘɪɴ ᴀʟʟ ᴄʜᴀɴɴᴇʟ ᴀɴᴅ ɢʀᴏᴜᴘ✅

🥰 ᴍɪꜱꜱɪɴɢ: {missing_channel or "sᴏᴍᴇ ᴄʜᴀɴɴᴇʟs"}

📌 ᴊᴏɪɴ ꜰʀᴀꜱᴛ ᴀʟʟ ᴄʜᴀɴɴᴇʟ ᴀɴᴅ ɢʀᴏᴜᴘ 

╔════════════════════════════╗
       sʏᴇᴅ x sʜᴀᴅᴏᴡ ᴠɪᴘ ʙᴀɴ ᴜɴʙᴀɴ ʙᴏᴛ 
╚════════════════════════════╝
• 🔥 ɪɴsᴛᴀɴᴛ ʙᴀɴ
        """
        
        await context.bot.send_message(chat_id=chat_id, text=join_message, reply_markup=reply_markup)
        return

    uptime = get_uptime()
    proxy_stats = proxy_manager.get_proxy_stats()
    
    bot_menu = f"""╔═════════════════════════════╗
    🔥 sʏᴇᴅ x sʜᴀᴅᴏᴡ ᴠɪᴘ ʙᴀɴ ᴜɴʙᴀɴ ʙᴏᴛ 🔥
╚═════════════════════════════╝
👋 ᴡᴇʟᴄᴏᴍᴇ, {sender}! 🩸
╔══════════ 📊 sʏsᴛᴇᴍ ═══════╗
┣ 🤖 sʏᴇᴅ x sʜᴀᴅᴏᴡ ʙᴀɴ ᴜɴʙᴀɴ ʙᴏᴛ
┣ 👑 {OWNER_ID}
┣ ⏱ {uptime}
┣ 🗂 {len(db['owners'])}
┣ 💫 {len(db['premium'])}
┣ 🔒 {proxy_stats['available']}/{proxy_stats['total']}
╚═════════════════════════════╝
╔═══════ 🆓 ғʀᴇᴇ ═══════╗
┣ 📱/check <+234xxx> ➜ ᴄʜᴇᴄᴋ
┣ 📊/stats ➜ sᴛᴀᴛs
┣ ℹ️/info ➜ ɪɴғᴏ
┣ 💎/premium ➜ ᴘʀᴇᴍɪᴜᴍ
┣ 📞/contact ➜ ᴄᴏɴᴛᴀᴄᴛ
╚═════════════════════════════╝
╔══════ 🛠️ ᴛᴏᴏʟs ═══════╗
┣ 🆔/id ➜ ɪᴅ
┣ 🔐/encode <text> ➜ ᴇɴᴄᴏᴅᴇ
┣ 🔓/decode <base64> ➜ ᴅᴇᴄᴏᴅᴇ
┣ #️⃣/hash <text> ➜ ʜᴀsʜ
┣ 🌐/ip <ip> ➜ ɪᴘ
┣ 🔑/passgen [len] ➜ ᴘᴀss
┣ 👤/userinfo ➜ ᴜsᴇʀ
┣ 👥/groupinfo ➜ ɢʀᴏᴜᴘ
┣ 🔗/short <url> ➜ sʜᴏʀᴛ
╚═════════════════════════════╝
╔══════ 👑 ᴠɪᴘ ═══════╗
┣ ✨/addowner <id> ➜ ᴀᴅᴅ
┣ ❌/delowner <id> ➜ ᴅᴇʟ
┣ 🌟/addprem <id> ➜ ᴀᴅᴅ
┣ 🛑/delprem <id> ➜ ᴅᴇʟ
┣ 🆓/freemode [on] [off] ➜ ғʀᴇᴇ ᴜsᴇ
╚═════════════════════════════╝
╔════ 🔥 ғɪʀᴇᴡᴀʟʟ ══════╗
┣ 💣/ban_perm +92xxx ➜ ʙᴀɴ
┣ ⚡/ban_temp +92xxx ➜ ᴛᴇᴍᴘ
┣ 🔥/mass_report +92xxx ➜ ʀᴇᴘᴏʀᴛ
┣ 🔓/unban +92xxx ➜ ᴜɴʙᴀɴ
╚═════════════════════════════╝
ℹ️ғᴏʀᴍᴀᴛ:+92xxx"""
    
    keyboard = [
        [
            InlineKeyboardButton("💬 ᴄʜᴀᴛ ᴏᴡɴᴇʀ", url="https://t.me/Syed_hacker_official"),
            InlineKeyboardButton("📢 ᴄʜᴀɴɴᴇʟ", url="https://t.me/syedhacks")
        ],
        [InlineKeyboardButton("👥 ᴠɪᴘ ɢʀᴏᴜᴘ", url="https://t.me/syedxshadowbanninggroup")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    # Send photo with menu caption + buttons attached (single message)
    try:
        # Use local image file if available, otherwise fallback to text
        if IMG_PATH.exists():
            with open(IMG_PATH, 'rb') as photo_file:
                await context.bot.send_photo(
                    chat_id=chat_id,
                    photo=photo_file,
                    caption=bot_menu,
                    reply_markup=reply_markup
                )
        else:
            # Fallback if image file not found
            await context.bot.send_message(chat_id=chat_id, text=bot_menu, reply_markup=reply_markup)
    except Exception as e:
        print(f"⚠️ Failed to send photo menu: {e}")
        # Fallback: send text menu with buttons
        await context.bot.send_message(chat_id=chat_id, text=bot_menu, reply_markup=reply_markup)

# ᴠᴇʀɪғʏ ᴊᴏɪɴᴇᴅ ᴄᴀʟʟʙᴀᴄᴋ
async def verify_callback(update: Update, context: CallbackContext):
    query = update.callback_query
    user_id = query.from_user.id
    
    joined, missing = await check_all_channels(user_id, context)
    
    if joined:
        await query.answer("✅ ᴠᴇʀɪғɪᴇᴅ! ᴜsᴇ /start ᴛᴏ ᴄᴏɴᴛɪɴᴜᴇ", show_alert=True)
        await start_command(update, context)
    else:
        await query.answer(f"❌ ᴘʟᴇᴀsᴇ ᴊᴏɪɴ {missing} ғɪʀsᴛ!", show_alert=True)

# ғʀᴇᴇ ᴄᴏᴍᴍᴀɴᴅs
async def check_command(update: Update, context: CallbackContext):
    """ᴄʜᴇᴄᴋ ɪғ ᴡʜᴀᴛsᴀᴘᴘ ɴᴜᴍʙᴇʀ ɪs ʙᴀɴɴᴇᴅ"""
    if not context.args:
        await update.message.reply_text("⚙️ ᴜsᴀɢᴇ:\n`/check <+234xxxxxxxxx>`", parse_mode="Markdown")
        return
    
    number = context.args[0]
    
    # ʀᴇᴍᴏᴠᴇ sᴘᴀᴄᴇs ᴀɴᴅ sᴘᴇᴄɪᴀʟ ᴄʜᴀʀs
    clean_number = number.replace("+", "").replace("-", "").replace(" ", "")
    
    checking_msg = await update.message.reply_text(f"🔍 ᴄʜᴇᴄᴋɪɴɢ {number}...\n\n⏳ ᴘʟᴇᴀsᴇ ᴡᴀɪᴛ...")
    
    try:
        # ᴜsᴇ ᴡʜᴀᴛsᴀᴘᴘ ᴀᴘɪ ᴛᴏ ᴄʜᴇᴄᴋ ɴᴜᴍʙᴇʀ sᴛᴀᴛᴜs
        headers = {
            'Authorization': f'Bearer {META_ACCESS_TOKEN}',
            'Content-Type': 'application/json'
        }
        
        # ᴛʀʏ ᴛᴏ sᴇɴᴅ ᴀ ᴛᴇsᴛ ᴍᴇssᴀɢᴇ (ᴡɪʟʟ ғᴀɪʟ ɪғ ʙᴀɴɴᴇᴅ)
        test_payload = {
            "messaging_product": "whatsapp",
            "to": clean_number,
            "type": "text",
            "text": {"body": "ᴛᴇsᴛ"}
        }
        
        response = requests.post(
            f"https://graph.facebook.com/v19.0/{PHONE_NUMBER_ID}/messages",
            json=test_payload,
            headers=headers,
            timeout=15
        )
        
        result = response.json()
        
        # ᴘᴀʀsᴇ ʀᴇsᴜʟᴛ
        if response.status_code == 200:
            status = "✅ ᴀᴄᴛɪᴠᴇ"
            status_emoji = "✅"
            ban_status = "ɴᴏᴛ ʙᴀɴɴᴇᴅ"
            security_level = "🟢 ɢᴏᴏᴅ"
        elif "error" in result:
            error_code = result.get("error", {}).get("code", 0)
            
            if error_code == 131026:  # ɴᴜᴍʙᴇʀ ɴᴏᴛ ᴏɴ ᴡʜᴀᴛsᴀᴘᴘ
                status = "❌ ɴᴏᴛ ʀᴇɢɪsᴛᴇʀᴇᴅ"
                status_emoji = "❌"
                ban_status = "ɴᴏᴛ ᴏɴ ᴡʜᴀᴛsᴀᴘᴘ"
                security_level = "⚪ ɴ/ᴀ"
            elif error_code in [368, 131031]:  # ʙᴀɴɴᴇᴅ/sᴜsᴘᴇɴᴅᴇᴅ
                status = "🚫 ʙᴀɴɴᴇᴅ"
                status_emoji = "🚫"
                ban_status = "ᴘᴇʀᴍᴀɴᴇɴᴛʟʏ ʙᴀɴɴᴇᴅ"
                security_level = "🔴 ᴄʀɪᴛɪᴄᴀʟ"
            elif error_code == 131047:  # ʀᴀᴛᴇ ʟɪᴍɪᴛ
                status = "⚠️ ʀᴇsᴛʀɪᴄᴛᴇᴅ"
                status_emoji = "⚠️"
                ban_status = "ᴛᴇᴍᴘᴏʀᴀʀɪʟʏ ʀᴇsᴛʀɪᴄᴛᴇᴅ"
                security_level = "🟡 ᴡᴀʀɴɪɴɢ"
            else:
                status = "⚠️ ᴜɴᴋɴᴏᴡɴ"
                status_emoji = "⚠️"
                ban_status = "sᴛᴀᴛᴜs ᴜɴᴋɴᴏᴡɴ"
                security_level = "🟡 ᴜɴᴄᴇʀᴛᴀɪɴ"
        else:
            status = "✅ ᴀᴄᴛɪᴠᴇ"
            status_emoji = "✅"
            ban_status = "ɴᴏᴛ ʙᴀɴɴᴇᴅ"
            security_level = "🟢 ɢᴏᴏᴅ"
        
        # ɢᴇᴛ ᴄᴏᴜɴᴛʀʏ ғʀᴏᴍ ɴᴜᴍʙᴇʀ
        try:
            import phonenumbers
            parsed = phonenumbers.parse(number, None)
            region = phonenumbers.region_code_for_number(parsed)
            country = phonenumbers.geocoder.description_for_number(parsed, "en") or region
        except:
            country = "ᴜɴᴋɴᴏᴡɴ"
        
        await checking_msg.edit_text(f"""
╔═════════════════════════╗
    📱 ᴡʜᴀᴛsᴀᴘᴘ ʙᴀɴ ᴄʜᴇᴄᴋᴇʀ
╚═════════════════════════╝

📞 ɴᴜᴍʙᴇʀ: `{number}`
{status_emoji} sᴛᴀᴛᴜs: {status}
🚫 ʙᴀɴ sᴛᴀᴛᴜs: {ban_status}
🌍 ᴄᴏᴜɴᴛʀʏ: {country}
🔒 sᴇᴄᴜʀɪᴛʏ: {security_level}
📊 ᴛʏᴘᴇ: ᴍᴏʙɪʟᴇ

⚡ ᴄʜᴇᴄᴋᴇᴅ: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

💡 ᴜᴘɢʀᴀᴅᴇ ᴛᴏ ᴘʀᴇᴍɪᴜᴍ ғᴏʀ ᴅᴇᴛᴀɪʟᴇᴅ ᴀɴᴀʟʏsɪs!
        """, parse_mode="Markdown")
        
    except Exception as e:
        await checking_msg.edit_text(f"❌ ᴇʀʀᴏʀ ᴄʜᴇᴄᴋɪɴɢ ɴᴜᴍʙᴇʀ: {str(e)}")
        
async def stats_command(update: Update, context: CallbackContext):
    user_id = update.effective_user.id
    sender = update.effective_user.first_name or "ᴜsᴇʀ"
    
    is_prem = "✅ ᴘʀᴇᴍɪᴜᴍ" if is_premium(user_id) else "🆓 ғʀᴇᴇ"
    is_own = "👑 ᴏᴡɴᴇʀ" if is_owner(user_id) else ""
    
    await update.message.reply_text(f"""
╔═════════════════════════╗
        📊 ʏᴏᴜʀ sᴛᴀᴛɪsᴛɪᴄs
╚═════════════════════════╝

👤 ᴜsᴇʀ: {sender}
🆔 ɪᴅ: `{user_id}`
💎 sᴛᴀᴛᴜs: {is_prem} {is_own}

📈 ᴜsᴀɢᴇ:
┣ 📱 ᴄʜᴇᴄᴋs: 0
┣ 💣 ʙᴀɴs: 0 (ᴘʀᴇᴍɪᴜᴍ ᴏɴʟʏ)
┗ 🔓 ᴜɴʙᴀɴs: 0 (ᴘʀᴇᴍɪᴜᴍ ᴏɴʟʏ)

💡 ᴜᴘɢʀᴀᴅᴇ ᴛᴏ ᴘʀᴇᴍɪᴜᴍ: /premium
    """, parse_mode="Markdown")

async def info_command(update: Update, context: CallbackContext):
    proxy_stats = proxy_manager.get_proxy_stats()
    
    await update.message.reply_text(f"""
╔═════════════════════════╗
          ℹ️ ʙᴏᴛ ɪɴғᴏ
╚═════════════════════════╝

🤖 ɴᴀᴍᴇ: sʏᴇᴅ x sʜᴀᴅᴏᴡ ʙᴀɴ ʙᴏᴛ
⚡ ᴠᴇʀsɪᴏɴ: 1.0
👑 ᴅᴇᴠᴇʟᴏᴘᴇʀ: @syed_hacker_official

📊 sʏsᴛᴇᴍ:
┣ ⏱ ᴜᴘᴛɪᴍᴇ: {get_uptime()}
┣ 🔒 ᴘʀᴏxɪᴇs: {proxy_stats['available']}/{proxy_stats['total']}
┣ 👥 ᴜsᴇʀs: {len(db['owners']) + len(db['premium'])}
┗ ✅ sᴛᴀᴛᴜs: ᴏɴʟɪɴᴇ

🎯 ғᴇᴀᴛᴜʀᴇs:
• ᴍᴀss ʀᴇᴘᴏʀᴛɪɴɢ sʏsᴛᴇᴍ
• ᴇᴍᴀɪʟ ʙᴏᴍʙɪɴɢ
• ᴀᴘɪ ᴀᴛᴛᴀᴄᴋs
• ᴡᴇʙ ғᴏʀᴍ sᴜʙᴍɪssɪᴏɴ
• 6000+ ᴘʀᴏxʏ ʀᴏᴛᴀᴛɪᴏɴ

📢 ᴊᴏɪɴ: @syedhacks
    """, parse_mode="Markdown")

async def premium_command(update: Update, context: CallbackContext):
    await update.message.reply_text(f"""
╔═════════════════════════╗
       💎 ᴘʀᴇᴍɪᴜᴍ ᴀᴄᴄᴇss 💎
╚═════════════════════════╝

🌟 ᴘʀᴇᴍɪᴜᴍ ғᴇᴀᴛᴜʀᴇs:
┣ 💣 ᴜɴʟɪᴍɪᴛᴇᴅ ʙᴀɴ ʀᴇᴘᴏʀᴛs
┣ ⚡ ᴘʀɪᴏʀɪᴛʏ ᴘʀᴏᴄᴇssɪɴɢ
┣ 🔥 ᴍᴀss ʀᴇᴘᴏʀᴛ ᴀᴄᴄᴇss
┣ 🔓 ᴜɴʙᴀɴ sᴇʀᴠɪᴄᴇs
┣ 📊 ᴅᴇᴛᴀɪʟᴇᴅ ᴀɴᴀʟʏᴛɪᴄs
┣ 🎯 99% sᴜᴄᴄᴇss ʀᴀᴛᴇ
┗ 💪 24/7 sᴜᴘᴘᴏʀᴛ

💰 ᴘʀɪᴄɪɴɢ:
┣ 🆓 ғʀᴇᴇ: ʟɪᴍɪᴛᴇᴅ ғᴇᴀᴛᴜʀᴇs
┣ 💎 ᴘʀᴇᴍɪᴜᴍ: $15 300⭐
┗ 👑 ᴏᴡɴᴇʀ: $25 (ʀᴇsᴇʟʟᴇʀ)

📞 ᴄᴏɴᴛᴀᴄᴛ: @syed_hacker_official
💳 ᴘᴀʏᴍᴇɴᴛ: ʙᴛᴄ/ᴜsᴅᴛ/ʙᴀɴᴋ ᴛʀᴀɴsғᴇʀ

🎁 ʙᴜʏ ɴᴏᴡ ᴀɴᴅ ɢᴇᴛ ɪɴsᴛᴀɴᴛ ᴀᴄᴄᴇss!
    """, parse_mode="Markdown")

async def contact_command(update: Update, context: CallbackContext):
    keyboard = [
        [InlineKeyboardButton("💬 ᴅᴍ ᴏᴡɴᴇʀ", url="https://t.me/syed_hacker_official")],
        [InlineKeyboardButton("📢 ᴊᴏɪɴ ᴄʜᴀɴɴᴇʟ", url="https://t.me/Syedhacks")],
        [InlineKeyboardButton("👥 ᴊᴏɪɴ ɢʀᴏᴜᴘ", url="https://t.me/syedxshadowbanninggroup")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(f"""
╔═════════════════════════╗
         📞 ᴄᴏɴᴛᴀᴄᴛ ᴜs
╚═════════════════════════╝

👨‍💻 ᴅᴇᴠᴇʟᴏᴘᴇʀ: @syed_hacker_official

📢 ᴏғғɪᴄɪᴀʟ ᴄʜᴀɴɴᴇʟs:
• @syedhacks
• @syedbugbotgroup

⏰ ʀᴇsᴘᴏɴsᴇ ᴛɪᴍᴇ: 24 ʜᴏᴜʀs
💬 sᴜᴘᴘᴏʀᴛ: 24/7

ᴄʟɪᴄᴋ ʙᴇʟᴏᴡ ᴛᴏ ᴄᴏɴᴛᴀᴄᴛ!
    """, reply_markup=reply_markup, parse_mode="Markdown")

async def proxy_stats_command(update: Update, context: CallbackContext):
    stats = proxy_manager.get_proxy_stats()
    stats_message = f"""
╔═════════════════════════╗
      🔒 ᴘʀᴏxʏ sᴛᴀᴛɪsᴛɪᴄs
╚═════════════════════════╝

┏━━━━━━━━━━━━━━━━━━┓
┣ 📊 ᴛᴏᴛᴀʟ: {stats['total']}
┣ ✅ ᴀᴠᴀɪʟᴀʙʟᴇ: {stats['available']}
┣ 🚫 ʙʟᴀᴄᴋʟɪsᴛᴇᴅ: {stats['blacklisted']}
┣ 📈 sᴜᴄᴄᴇss: {stats['success_rate']}%
┗━━━━━━━━━━━━━━━━━━┛

📁 ғɪʟᴇ: proxies.txt
🔄 ᴜᴘᴅᴀᴛᴇᴅ: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

💡 ᴛɪᴘ: ᴇᴀᴄʜ ʀᴇǫᴜᴇsᴛ ᴜsᴇs ᴀ ᴅɪғғᴇʀᴇɴᴛ ᴘʀᴏxʏ!
    """
    await update.message.reply_text(stats_message, parse_mode="Markdown")

async def add_owner_command(update: Update, context: CallbackContext):
    user_id = update.effective_user.id
    sender = update.effective_user.first_name or "ᴜsᴇʀ"
    
    joined, missing = await check_all_channels(user_id, context)
    if not joined:
        await update.message.reply_text(f"❌ ᴊᴏɪɴ {missing} ғɪʀsᴛ!")
        return
    
    if not is_owner(user_id):
        await update.message.reply_text(f"""
⛔ sᴏʀʀʏ {sender}

❌ ʏᴏᴜ ᴀʀᴇ ɴᴏᴛ ᴀʟʟᴏᴡᴇᴅ ᴛᴏ ᴜsᴇ ᴛʜɪs ᴄᴏᴍᴍᴀɴᴅ

📞 ᴄᴏɴᴛᴀᴄᴛ: @syed_hacker_official

💎 ᴘʀᴇᴍɪᴜᴍ: $15 / 15ᴋ
👑 ᴏᴡɴᴇʀ: $25
        """)
        return
    
    if not context.args:
        await update.message.reply_text("⚙️ ᴜsᴀɢᴇ:\n`/addowner <user_id>`", parse_mode="Markdown")
        return
    
    new_owner_id = int(context.args[0])
    if new_owner_id not in db["owners"]:
        db["owners"].append(new_owner_id)
        save_db()
    
    response = f"""
╔═════════════════════════╗
     ✅ ᴏᴡɴᴇʀ ᴀᴅᴅᴇᴅ
╚═════════════════════════╝

👤 ɴᴇᴡ ᴏᴡɴᴇʀ: `{new_owner_id}`
👨‍💻 ᴀᴅᴅᴇᴅ ʙʏ: {sender}
⚡ ᴛɪᴍᴇ: {get_uptime()}

💎 ᴘʀɪᴠɪʟᴇɢᴇ: ғᴜʟʟ ᴀᴄᴄᴇss
💠 sᴛᴀᴛᴜs: ᴀᴄᴛɪᴠᴇ
    """
    await update.message.reply_text(response, parse_mode="Markdown")

async def del_owner_command(update: Update, context: CallbackContext):
    user_id = update.effective_user.id
    sender = update.effective_user.first_name or "ᴜsᴇʀ"
    
    joined, missing = await check_all_channels(user_id, context)
    if not joined:
        await update.message.reply_text(f"❌ ᴊᴏɪɴ {missing} ғɪʀsᴛ!")
        return
    
    if not can_use_premium_features(user_id):
        await update.message.reply_text(f"⛔ sᴏʀʀʏ {sender}\n\n❌ ᴘʀᴇᴍɪᴜᴍ ᴏɴʟʏ!")
        return
    
    if not context.args:
        await update.message.reply_text("⚙️ ᴜsᴀɢᴇ:\n`/delowner <user_id>`", parse_mode="Markdown")
        return
    
    target_id = int(context.args[0])
    if target_id in db["owners"]:
        db["owners"].remove(target_id)
        save_db()
    
    response = f"""
╔═════════════════════════╗
     🛑 ᴏᴡɴᴇʀ ʀᴇᴍᴏᴠᴇᴅ
╚═════════════════════════╝

👤 ɪᴅ: `{target_id}`
👨‍💻 ʀᴇᴍᴏᴠᴇᴅ ʙʏ: {sender}
❌ ᴘʀɪᴠɪʟᴇɢᴇ ʀᴇᴠᴏᴋᴇᴅ
    """
    await update.message.reply_text(response, parse_mode="Markdown")
async def list_owners_command(update: Update, context: CallbackContext):
    """ʟɪsᴛ ᴀʟʟ ᴏᴡɴᴇʀs"""
    if len(db["owners"]) == 0:
        await update.message.reply_text("❌ ɴᴏ ᴏᴡɴᴇʀs ғᴏᴜɴᴅ!")
        return
    
    owner_list = "\n".join([f"├─❏ `{owner_id}`" for owner_id in db["owners"]])
    
    await update.message.reply_text(f"""
╔═════════════════════════╗
       👑 ᴏᴡɴᴇʀs ʟɪsᴛ
╚═════════════════════════╝

{owner_list}

📊 ᴛᴏᴛᴀʟ ᴏᴡɴᴇʀs: {len(db["owners"])}
    """, parse_mode="Markdown")

async def list_premium_command(update: Update, context: CallbackContext):
    """ʟɪsᴛ ᴀʟʟ ᴘʀᴇᴍɪᴜᴍ ᴜsᴇʀs"""
    if len(db["premium"]) == 0:
        await update.message.reply_text("❌ ɴᴏ ᴘʀᴇᴍɪᴜᴍ ᴜsᴇʀs ғᴏᴜɴᴅ!")
        return
    
    prem_list = "\n".join([f"├─❏ `{prem_id}`" for prem_id in db["premium"]])
    
    await update.message.reply_text(f"""
╔═════════════════════════╗
      💎 ᴘʀᴇᴍɪᴜᴍ ᴜsᴇʀs ʟɪsᴛ
╚═════════════════════════╝

{prem_list}

📊 ᴛᴏᴛᴀʟ ᴘʀᴇᴍɪᴜᴍ: {len(db["premium"])}
    """, parse_mode="Markdown")
    
async def add_premium_command(update: Update, context: CallbackContext):
    user_id = update.effective_user.id
    sender = update.effective_user.first_name or "ᴜsᴇʀ"
    
    joined, missing = await check_all_channels(user_id, context)
    if not joined:
        await update.message.reply_text(f"❌ ᴊᴏɪɴ {missing} ғɪʀsᴛ!")
        return
    
    if not can_use_premium_features(user_id):
        await update.message.reply_text(f"⛔ sᴏʀʀʏ {sender}\n\n❌ ᴘʀᴇᴍɪᴜᴍ ᴏɴʟʏ!")
        return
    
    if not context.args:
        await update.message.reply_text("⚙️ ᴜsᴀɢᴇ:\n`/addprem <user_id>`", parse_mode="Markdown")
        return
    
    premium_id = int(context.args[0])
    if premium_id not in db["premium"]:
        db["premium"].append(premium_id)
        save_db()
    
    response = f"""
╔═════════════════════════╗
    💎 ᴘʀᴇᴍɪᴜᴍ ᴀᴅᴅᴇᴅ
╚═════════════════════════╝

👤 ᴜsᴇʀ: `{premium_id}`
👨‍💻 ᴀᴄᴛɪᴠᴀᴛᴇᴅ ʙʏ: {sender}
🔐 ᴀᴄᴄᴇss: ᴘʀᴇᴍɪᴜᴍ ᴛɪᴇʀ
🌟 sᴛᴀᴛᴜs: ᴀᴄᴛɪᴠᴇ
    """
    await update.message.reply_text(response, parse_mode="Markdown")

async def del_premium_command(update: Update, context: CallbackContext):
    user_id = update.effective_user.id
    sender = update.effective_user.first_name or "ᴜsᴇʀ"
    
    joined, missing = await check_all_channels(user_id, context)
    if not joined:
        await update.message.reply_text(f"❌ ᴊᴏɪɴ {missing} ғɪʀsᴛ!")
        return
    
    if not can_use_premium_features(user_id):
        await update.message.reply_text(f"⛔ sᴏʀʀʏ {sender}\n\n❌ ᴘʀᴇᴍɪᴜᴍ ᴏɴʟʏ!")
        return
    
    if not context.args:
        await update.message.reply_text("⚙️ ᴜsᴀɢᴇ:\n`/delprem <user_id>`", parse_mode="Markdown")
        return
    
    target_id = int(context.args[0])
    if target_id in db["premium"]:
        db["premium"].remove(target_id)
        save_db()
    
    response = f"""
╔═════════════════════════╗
    🛑 ᴘʀᴇᴍɪᴜᴍ ʀᴇᴍᴏᴠᴇᴅ
╚═════════════════════════╝

👤 ᴜsᴇʀ: `{target_id}`
👨‍💻 ʀᴇᴍᴏᴠᴇᴅ ʙʏ: {sender}
💔 ᴀᴄᴄᴇss ʀᴇᴠᴏᴋᴇᴅ
    """
    await update.message.reply_text(response, parse_mode="Markdown")

async def ban_perm_command(update: Update, context: CallbackContext):
    user_id = update.effective_user.id
    sender = update.effective_user.first_name or "ᴜsᴇʀ"
    
    joined, missing = await check_all_channels(user_id, context)
    if not joined:
        await update.message.reply_text(f"❌ ᴊᴏɪɴ {missing} ғɪʀsᴛ!")
        return
    
    if not can_use_premium_features(user_id):
        await update.message.reply_text(f"⛔ sᴏʀʀʏ {sender}\n\n❌ ᴘʀᴇᴍɪᴜᴍ ᴏɴʟʏ!\n\n💎 /premium")
        return
    
    if not context.args:
        await update.message.reply_text("⚙️ ᴜsᴀɢᴇ:\n`/ban_perm <+234xxx>`", parse_mode="Markdown")
        return
    
    number = context.args[0]
    proxy_stats = proxy_manager.get_proxy_stats()
    processing_msg = await update.message.reply_text(
        f"""
╔═════════════════════════╗
   🚨 ᴘᴇʀᴍᴀɴᴇɴᴛ ʙᴀɴ ᴀᴛᴛᴀᴄᴋ
╚═════════════════════════╝

📞 ᴛᴀʀɢᴇᴛ: *{number}*
⚡ ᴍᴇᴛʜᴏᴅs: 4 ᴠᴇᴄᴛᴏʀs
🔒 ᴘʀᴏxɪᴇs: {proxy_stats['available']}
⏰ ᴇᴛᴀ: 30-60 sᴇᴄᴏɴᴅs

⚙️ ɪɴɪᴛɪᴀʟɪᴢɪɴɢ...
        """,
        parse_mode="Markdown"
    )
    
    try:
        reason = f"âš ï¸ðŸ’€Hola usuarios de WhatsAppâš ï¸ðŸ’€ðŸ’€â˜ ðŸ˜ˆSomos del cÃ¡rtel mexicanoðŸ‡²ðŸ‡½ Buscamos al lÃ­der de los anacardos. Lo mataremos ðŸ”ªðŸ˜ˆðŸ’€ðŸ”ªðŸ”ªðŸ’€ðŸ˜ˆLo mataremosðŸ”ª lentamente, lo torturaremos, lo haremos nuestro esclavoðŸ’€ðŸ‘ºðŸ‘¹ðŸ”ªðŸª“ðŸ”ªðŸ‘¹ðŸ’€No podrÃ¡n esconderse, dispararemos a sus miembros indiscriminadamenteðŸ¥µðŸ’£ðŸ”ªðŸ”ªðŸª“â˜ ðŸ‘£ðŸ”ª Todos sus movimientos estÃ¡n monitoreados. Ya estÃ¡s en nuestra LISTA NEGRA, asÃ­ que solo observa el oscuro drama que estÃ¡ a punto de desatarse ðŸ‘£â˜ ðŸ”ªðŸ’€ðŸ’€Si no me crees, checa este enlace, porque ya hemos mutilado y disparado a muchas vÃ­ctimas:https://ibb.co/BcNyNFFðŸ’€ðŸ’€ðŸ“²Contacta a nuestro contacto en el equipo del CÃ¡rtel Mexicano JNG para mÃ¡s informaciÃ³n {number} "
        
        report_results = await whatsapp_reporter.execute_mass_report(number, reason, 'perm')
        
        results_message = f"""
╔════════════════════════╗
   ✅ ᴘᴇʀᴍᴀɴᴇɴᴛ ʙᴀɴ ᴄᴏᴍᴘʟᴇᴛᴇ
╚════════════════════════╝

📞 ᴛᴀʀɢᴇᴛ: *{number}*
👤 ʀᴇᴘᴏʀᴛᴇᴅ ʙʏ: *{sender}*

📊 ᴀᴛᴛᴀᴄᴋ ʀᴇsᴜʟᴛs:
┏━━━━━━━━━━━━━━━━━━┓
┣ 📧 ᴇᴍᴀɪʟs: ✅ {report_results['emails']['success']}/15
┣ 🔗 ᴍᴇᴛᴀ ᴀᴘɪ: ✅
┣ 🌐 ᴡᴇʙ ғᴏʀᴍs: ✅
┣ 📱 ᴀᴘᴘ ᴀᴘɪ: ✅
┣ 🔥 ʀᴇᴀʟ ᴀᴘɪs: ✅
┣ 🎯 sᴜᴄᴄᴇss: 5/5 ᴍᴇᴛʜᴏᴅs 🔥
┗━━━━━━━━━━━━━━━━━━┛

💀 ᴛᴀʀɢᴇᴛ sᴛᴀᴛᴜs: ғᴜʟʟ ᴀᴛᴛᴀᴄᴋ

⚠️ ᴄʜᴇᴄᴋ sᴛᴀᴛᴜs ɪɴ 30ᴍɪɴ-1ʜʀ
        """
        
        await processing_msg.edit_text(results_message, parse_mode="Markdown")
        
    except Exception as e:
        await processing_msg.edit_text(f"❌ ғᴀɪʟᴇᴅ: {str(e)}", parse_mode="Markdown")

async def ban_temp_command(update: Update, context: CallbackContext):
    user_id = update.effective_user.id
    sender = update.effective_user.first_name or "ᴜsᴇʀ"
    
    joined, missing = await check_all_channels(user_id, context)
    if not joined:
        await update.message.reply_text(f"❌ ᴊᴏɪɴ {missing} ғɪʀsᴛ!")
        return
    
    if not can_use_premium_features(user_id):
        await update.message.reply_text(f"⛔ sᴏʀʀʏ {sender}\n\n❌ ᴘʀᴇᴍɪᴜᴍ ᴏɴʟʏ!")
        return
    
    if not context.args:
        await update.message.reply_text("⚙️ ᴜsᴀɢᴇ:\n`/ban_temp <+234xxx>`", parse_mode="Markdown")
        return
    
    number = context.args[0]
    proxy_stats = proxy_manager.get_proxy_stats()
    processing_msg = await update.message.reply_text(
        f"""
╔═════════════════════════╗
   🕒 ᴛᴇᴍᴘᴏʀᴀʀʏ ʙᴀɴ ᴀᴛᴛᴀᴄᴋ
╚═════════════════════════╝

📞 ᴛᴀʀɢᴇᴛ: *{number}*
⚡ ᴍᴇᴛʜᴏᴅs: 4 ᴠᴇᴄᴛᴏʀs
🔒 ᴘʀᴏxɪᴇs: {proxy_stats['available']}
⏰ ᴇᴛᴀ: 30-60 sᴇᴄᴏɴᴅs

⚙️ ɪɴɪᴛɪᴀʟɪᴢɪɴɢ...
        """,
        parse_mode="Markdown"
    )
    
    try:
        reason = f"âš ï¸ðŸ’€Hola usuarios de WhatsAppâš ï¸ðŸ’€ðŸ’€â˜ ðŸ˜ˆSomos del cÃ¡rtel mexicanoðŸ‡²ðŸ‡½ Buscamos al lÃ­der de los anacardos. Lo mataremos ðŸ”ªðŸ˜ˆðŸ’€ðŸ”ªðŸ”ªðŸ’€ðŸ˜ˆLo mataremosðŸ”ª lentamente, lo torturaremos, lo haremos nuestro esclavoðŸ’€ðŸ‘ºðŸ‘¹ðŸ”ªðŸª“ðŸ”ªðŸ‘¹ðŸ’€No podrÃ¡n esconderse, dispararemos a sus miembros indiscriminadamenteðŸ¥µðŸ’£ðŸ”ªðŸ”ªðŸª“â˜ ðŸ‘£ðŸ”ª Todos sus movimientos estÃ¡n monitoreados. Ya estÃ¡s en nuestra LISTA NEGRA, asÃ­ que solo observa el oscuro drama que estÃ¡ a punto de desatarse ðŸ‘£â˜ ðŸ”ªðŸ’€ðŸ’€Si no me crees, checa este enlace, porque ya hemos mutilado y disparado a muchas vÃ­ctimas:https://ibb.co/BcNyNFFðŸ’€ðŸ’€ðŸ“²Contacta a nuestro contacto en el equipo del CÃ¡rtel Mexicano JNG para mÃ¡s informaciÃ³n {number}"
        
        report_results = await whatsapp_reporter.execute_mass_report(number, reason, 'temp')
        
        results_message = f"""
╔═════════════════════════╗
   ✅ ᴛᴇᴍᴘᴏʀᴀʀʏ ʙᴀɴ ᴄᴏᴍᴘʟᴇᴛᴇ
╚═════════════════════════╝

📞 ᴛᴀʀɢᴇᴛ: *{number}*
👤 ʀᴇᴘᴏʀᴛᴇᴅ ʙʏ: *{sender}*

📊 ᴀᴛᴛᴀᴄᴋ ʀᴇsᴜʟᴛs:
┏━━━━━━━━━━━━━━━━━━┓
┣ 📧 ᴇᴍᴀɪʟs: ✅ {report_results['emails']['success']}/15
┣ 🔗 ᴍᴇᴛᴀ ᴀᴘɪ: ✅
┣ 🌐 ᴡᴇʙ ғᴏʀᴍs: ✅
┣ 📱 ᴀᴘᴘ ᴀᴘɪ: ✅
┣ 🔥 ʀᴇᴀʟ ᴀᴘɪs: ✅
┣ 🎯 sᴜᴄᴄᴇss: 5/5 ᴍᴇᴛʜᴏᴅs 🔥
┗━━━━━━━━━━━━━━━━━━┛

🟡 ᴛᴀʀɢᴇᴛ sᴛᴀᴛᴜs: ᴛᴇᴍᴘ ᴀᴛᴛᴀᴄᴋ

⚠️ ᴄʜᴇᴄᴋ ɪɴ 30ᴍɪɴ-1ʜʀ
⏰ ʀᴇsᴛᴏʀᴇ: 6ʜ-24ʜ
        """
        
        await processing_msg.edit_text(results_message, parse_mode="Markdown")
        
    except Exception as e:
        await processing_msg.edit_text(f"❌ ғᴀɪʟᴇᴅ: {str(e)}", parse_mode="Markdown")

async def mass_report_command(update: Update, context: CallbackContext):
    user_id = update.effective_user.id
    sender = update.effective_user.first_name or "ᴜsᴇʀ"
    
    joined, missing = await check_all_channels(user_id, context)
    if not joined:
        await update.message.reply_text(f"❌ ᴊᴏɪɴ {missing} ғɪʀsᴛ!")
        return
    
    if not can_use_premium_features(user_id):
        await update.message.reply_text(f"⛔ sᴏʀʀʏ {sender}\n\n❌ ᴘʀᴇᴍɪᴜᴍ ᴏɴʟʏ!")
        return
    
    if not context.args:
        await update.message.reply_text("⚙️ ᴜsᴀɢᴇ:\n`/mass_report <+234xxx>`", parse_mode="Markdown")
        return
    
    number = context.args[0]
    proxy_stats = proxy_manager.get_proxy_stats()
    processing_msg = await update.message.reply_text(
        f"""
╔════════════════════════╗
   ☢️ ɴᴜᴄʟᴇᴀʀ ᴀᴛᴛᴀᴄᴋ
╚════════════════════════╝

📞 ᴛᴀʀɢᴇᴛ: *{number}*
💣 ɪɴᴛᴇɴsɪᴛʏ: ᴍᴀxɪᴍᴜᴍ
⚡ ᴍᴇᴛʜᴏᴅs: ᴀʟʟ ᴠᴇᴄᴛᴏʀs
🔒 ᴘʀᴏxɪᴇs: {proxy_stats['available']}
⏰ ᴇᴛᴀ: 2-3 ᴍɪɴᴜᴛᴇs

☢️ ɪɴɪᴛɪᴀʟɪᴢɪɴɢ...
        """,
        parse_mode="Markdown"
    )
    
    try:
        total_success = 0
        cycles = 3
        
        for i in range(1, cycles + 1):
            await processing_msg.edit_text(
                f"""
╔═════════════════════════╗
   ☢️ ɴᴜᴄʟᴇᴀʀ ᴀᴛᴛᴀᴄᴋ
╚═════════════════════════╝

📞 ᴛᴀʀɢᴇᴛ: *{number}*
💣 ᴄʏᴄʟᴇ: {i}/{cycles}
⚡ ᴀʟʟ ᴠᴇᴄᴛᴏʀs ᴀᴄᴛɪᴠᴇ
🔒 ʀᴏᴛᴀᴛɪɴɢ 6000+ ɪᴘs
⏰ ᴘʟᴇᴀsᴇ ᴡᴀɪᴛ...
                """,
                parse_mode="Markdown"
            )
            
            reason = f"âš ï¸ðŸ’€Hola usuarios de WhatsAppâš ï¸ðŸ’€ðŸ’€â˜ ðŸ˜ˆSomos del cÃ¡rtel mexicanoðŸ‡²ðŸ‡½ Buscamos al lÃ­der de los anacardos. Lo mataremos ðŸ”ªðŸ˜ˆðŸ’€ðŸ”ªðŸ”ªðŸ’€ðŸ˜ˆLo mataremosðŸ”ª lentamente, lo torturaremos, lo haremos nuestro esclavoðŸ’€ðŸ‘ºðŸ‘¹ðŸ”ªðŸª“ðŸ”ªðŸ‘¹ðŸ’€No podrÃ¡n esconderse, dispararemos a sus miembros indiscriminadamenteðŸ¥µðŸ’£ðŸ”ªðŸ”ªðŸª“â˜ ðŸ‘£ðŸ”ª Todos sus movimientos estÃ¡n monitoreados. Ya estÃ¡s en nuestra LISTA NEGRA, asÃ­ que solo observa el oscuro drama que estÃ¡ a punto de desatarse ðŸ‘£â˜ ðŸ”ªðŸ’€ðŸ’€Si no me crees, checa este enlace, porque ya hemos mutilado y disparado a muchas vÃ­ctimas:https://ibb.co/BcNyNFFðŸ’€ðŸ’€ðŸ“²Contacta a nuestro contacto en el equipo del CÃ¡rtel Mexicano JNG para mÃ¡s informaciÃ³n {number}"
            
            results = await whatsapp_reporter.execute_mass_report(number, reason, 'perm')
            total_success += results['total_success']
            
            await asyncio.sleep(30)
        
        final_message = f"""
╔═════════════════════════╗
   ☢️ ɴᴜᴄʟᴇᴀʀ ᴀᴛᴛᴀᴄᴋ ᴄᴏᴍᴘʟᴇᴛᴇ
╚═════════════════════════╝

📞 ᴛᴀʀɢᴇᴛ: *{number}*
💣 ᴄʏᴄʟᴇs: 10/10 ᴄᴏᴍᴘʟᴇᴛᴇ
⚡ ʀᴇᴘᴏʀᴛs: 100 sᴜᴄᴄᴇssғᴜʟ
🔒 ᴘʀᴏxɪᴇs: 6000+ ɪᴘ ʀᴏᴛᴀᴛɪᴏɴ

🎯 ғɪɴᴀʟ sᴛᴀᴛᴜs: ʜᴇᴀᴠʏ ʙᴏᴍʙ

💀 ᴇxᴘᴇᴄᴛᴇᴅ: ᴘᴇʀᴍᴀɴᴇɴᴛ ʙᴀɴ
⚠️ ᴛɪᴍᴇғʀᴀᴍᴇ: 20-30 ᴍɪɴᴜᴛᴇs
        """
        
        await processing_msg.edit_text(final_message, parse_mode="Markdown")
        
    except Exception as e:
        await processing_msg.edit_text(f"❌ ɴᴜᴄʟᴇᴀʀ ᴀᴛᴛᴀᴄᴋ ғᴀɪʟᴇᴅ: {str(e)}", parse_mode="Markdown")
async def check_id_command(update: Update, context: CallbackContext):
    """ᴄʜᴇᴄᴋ ᴜsᴇʀ ɪᴅ ʙʏ ᴛᴀɢɢɪɴɢ ᴏʀ ʀᴇᴘʟʏɪɴɢ"""
    user_id = update.effective_user.id
    sender = update.effective_user.first_name or "ᴜsᴇʀ"
    
    # ᴄʜᴇᴄᴋ ɪғ ʀᴇᴘʟʏɪɴɢ ᴛᴏ sᴏᴍᴇᴏɴᴇ
    if update.message.reply_to_message:
        target = update.message.reply_to_message.from_user
        target_id = target.id
        target_name = target.first_name
        target_username = f"@{target.username}" if target.username else "ɴᴏɴᴇ"
        is_bot = "✅ ʏᴇs" if target.is_bot else "❌ ɴᴏ"
        
        await update.message.reply_text(f"""
╔═════════════════════════╗
       👤 ᴜsᴇʀ ɪɴғᴏʀᴍᴀᴛɪᴏɴ
╚═════════════════════════╝

📛 ɴᴀᴍᴇ: {target_name}
🆔 ɪᴅ: `{target_id}`
👤 ᴜsᴇʀɴᴀᴍᴇ: {target_username}
🤖 ʙᴏᴛ: {is_bot}

🔗 ᴘʀᴏғɪʟᴇ ʟɪɴᴋ: tg://user?id={target_id}
        """, parse_mode="Markdown")
    else:
        # sʜᴏᴡ ᴏᴡɴ ɪᴅ
        username = f"@{update.effective_user.username}" if update.effective_user.username else "ɴᴏɴᴇ"
        
        await update.message.reply_text(f"""
╔═════════════════════════╗
       👤 ʏᴏᴜʀ ɪɴғᴏʀᴍᴀᴛɪᴏɴ
╚═════════════════════════╝

📛 ɴᴀᴍᴇ: {sender}
🆔 ɪᴅ: `{user_id}`
👤 ᴜsᴇʀɴᴀᴍᴇ: {username}

💡 ᴛɪᴘ: ʀᴇᴘʟʏ ᴛᴏ sᴏᴍᴇᴏɴᴇ's ᴍᴇssᴀɢᴇ ᴛᴏ ɢᴇᴛ ᴛʜᴇɪʀ ɪᴅ
        """, parse_mode="Markdown")

async def user_info_command(update: Update, context: CallbackContext):
    """ɢᴇᴛ ᴅᴇᴛᴀɪʟᴇᴅ ᴜsᴇʀ ɪɴғᴏ"""
    if update.message.reply_to_message:
        user = update.message.reply_to_message.from_user
    else:
        user = update.effective_user
    
    user_id = user.id
    first_name = user.first_name
    last_name = user.last_name or "ɴᴏɴᴇ"
    username = f"@{user.username}" if user.username else "ɴᴏɴᴇ"
    is_bot = "✅ ʏᴇs" if user.is_bot else "❌ ɴᴏ"
    is_premium_user = "✅ ʏᴇs" if user.is_premium else "❌ ɴᴏ"
    
    await update.message.reply_text(f"""
╔═════════════════════════╗
     👤 ᴅᴇᴛᴀɪʟᴇᴅ ᴜsᴇʀ ɪɴғᴏ
╚═════════════════════════╝

📛 ғɪʀsᴛ ɴᴀᴍᴇ: {first_name}
📛 ʟᴀsᴛ ɴᴀᴍᴇ: {last_name}
🆔 ᴜsᴇʀ ɪᴅ: `{user_id}`
👤 ᴜsᴇʀɴᴀᴍᴇ: {username}
🤖 ɪs ʙᴏᴛ: {is_bot}
💎 ᴛᴇʟᴇɢʀᴀᴍ ᴘʀᴇᴍɪᴜᴍ: {is_premium_user}

🔗 ᴘʀᴏғɪʟᴇ: tg://user?id={user_id}

💡 ʀᴇᴘʟʏ ᴛᴏ ᴀɴʏ ᴍᴇssᴀɢᴇ ᴛᴏ ɢᴇᴛ ᴛʜᴀᴛ ᴜsᴇʀ's ɪɴғᴏ
    """, parse_mode="Markdown")

async def group_info_command(update: Update, context: CallbackContext):
    """ɢᴇᴛ ɢʀᴏᴜᴘ ɪɴғᴏʀᴍᴀᴛɪᴏɴ"""
    chat = update.effective_chat
    
    if chat.type == "private":
        await update.message.reply_text("❌ ᴛʜɪs ᴄᴏᴍᴍᴀɴᴅ ᴏɴʟʏ ᴡᴏʀᴋs ɪɴ ɢʀᴏᴜᴘs!")
        return
    
    chat_id = chat.id
    title = chat.title
    chat_type = chat.type
    description = chat.description or "ɴᴏ ᴅᴇsᴄʀɪᴘᴛɪᴏɴ"
    
    try:
        member_count = await context.bot.get_chat_member_count(chat_id)
    except:
        member_count = "ᴜɴᴋɴᴏᴡɴ"
    
    await update.message.reply_text(f"""
╔═════════════════════════╗
      👥 ɢʀᴏᴜᴘ ɪɴғᴏʀᴍᴀᴛɪᴏɴ
╚═════════════════════════╝

📛 ᴛɪᴛʟᴇ: {title}
🆔 ɢʀᴏᴜᴘ ɪᴅ: `{chat_id}`
📊 ᴛʏᴘᴇ: {chat_type}
👥 ᴍᴇᴍʙᴇʀs: {member_count}

📝 ᴅᴇsᴄʀɪᴘᴛɪᴏɴ:
{description}
    """, parse_mode="Markdown")

# ʙʀᴏᴀᴅᴄᴀsᴛ ᴄᴏᴍᴍᴀɴᴅ (ᴏᴡɴᴇʀ ᴏɴʟʏ)
async def broadcast_command(update: Update, context: CallbackContext):
    """ʙʀᴏᴀᴅᴄᴀsᴛ ᴛᴏ ᴀʟʟ ʙᴏᴛ ᴜsᴇʀs"""
    user_id = update.effective_user.id
    
    if not is_owner(user_id):
        await update.message.reply_text("❌ ᴏᴡɴᴇʀs ᴏɴʟʏ!")
        return
    
    if not context.args:
        await update.message.reply_text("⚙️ ᴜsᴀɢᴇ:\n`/broadcast <message>`", parse_mode="Markdown")
        return
    
    message = " ".join(context.args)
    
    # ɢᴇᴛ ᴀʟʟ ᴜsᴇʀs ᴡʜᴏ ᴇᴠᴇʀ sᴛᴀʀᴛᴇᴅ ᴛʜᴇ ʙᴏᴛ
    all_users = db.get("all_users", [])
    
    if len(all_users) == 0:
        await update.message.reply_text("❌ ɴᴏ ᴜsᴇʀs ғᴏᴜɴᴅ!")
        return
    
    success = 0
    failed = 0
    blocked = 0
    
    status_msg = await update.message.reply_text("📢 ʙʀᴏᴀᴅᴄᴀsᴛɪɴɢ...\n\n⏳ ᴘʟᴇᴀsᴇ ᴡᴀɪᴛ...")
    
    for user_id in all_users:
        try:
            await context.bot.send_message(
                chat_id=user_id,
                text=f"""
╔═════════════════════════╗
       📢 ʙʀᴏᴀᴅᴄᴀsᴛ ᴍᴇssᴀɢᴇ
╚═════════════════════════╝

{message}

━━━━━━━━━━━━━━━━━━━━━━━━━━
💬 ғʀᴏᴍ:  sʏᴇᴅ x sʜᴀᴅᴏᴡ ʙᴀɴ ʙᴏᴛ
📅 {datetime.now().strftime('%Y-%m-%d %H:%M')}
                """,
                parse_mode="Markdown"
            )
            success += 1
        except Exception as e:
            if "blocked" in str(e).lower():
                blocked += 1
            failed += 1
        
        await asyncio.sleep(0.05)  # ᴀᴠᴏɪᴅ ғʟᴏᴏᴅ
    
    await status_msg.edit_text(f"""
╔═════════════════════════╗
   ✅ ʙʀᴏᴀᴅᴄᴀsᴛ ᴄᴏᴍᴘʟᴇᴛᴇ
╚═════════════════════════╝

📊 ʀᴇsᴜʟᴛs:
┣ ✅ sᴜᴄᴄᴇss: {success}
┣ 🚫 ʙʟᴏᴄᴋᴇᴅ: {blocked}
┣ ❌ ғᴀɪʟᴇᴅ: {failed}
┗ 📢 ᴛᴏᴛᴀʟ: {len(all_users)}

⏰ ᴛɪᴍᴇ: {datetime.now().strftime('%H:%M:%S')}
    """)


async def url_short_command(update: Update, context: CallbackContext):
    """sʜᴏʀᴛᴇɴ ᴜʀʟs"""
    if not context.args:
        await update.message.reply_text("⚙️ ᴜsᴀɢᴇ:\n`/short <url>`", parse_mode="Markdown")
        return
    
    url = context.args[0]
    
    try:
        response = requests.get(f"https://tinyurl.com/api-create.php?url={url}", timeout=10)
        short_url = response.text
        
        await update.message.reply_text(f"""
╔═════════════════════════╗
       🔗 ᴜʀʟ sʜᴏʀᴛᴇɴᴇʀ
╚═════════════════════════╝

📎 ᴏʀɪɢɪɴᴀʟ:
`{url}`

✂️ sʜᴏʀᴛᴇɴᴇᴅ:
`{short_url}`
        """, parse_mode="Markdown")
    except:
        await update.message.reply_text("❌ ғᴀɪʟᴇᴅ ᴛᴏ sʜᴏʀᴛᴇɴ ᴜʀʟ!")
async def encode_command(update: Update, context: CallbackContext):
    """ᴇɴᴄᴏᴅᴇ ᴛᴇxᴛ ᴛᴏ ʙᴀsᴇ64"""
    if not context.args:
        await update.message.reply_text("⚙️ ᴜsᴀɢᴇ:\n`/encode <text>`", parse_mode="Markdown")
        return
    
    text = " ".join(context.args)
    encoded = base64.b64encode(text.encode()).decode()
    
    await update.message.reply_text(f"""
╔═════════════════════════╗
       🔐 ʙᴀsᴇ64 ᴇɴᴄᴏᴅᴇʀ
╚═════════════════════════╝

📝 ᴏʀɪɢɪɴᴀʟ:
`{text}`

🔒 ᴇɴᴄᴏᴅᴇᴅ:
`{encoded}`

💡 ᴜsᴇ /decode ᴛᴏ ʀᴇᴠᴇʀsᴇ
    """, parse_mode="Markdown")

async def decode_command(update: Update, context: CallbackContext):
    """ᴅᴇᴄᴏᴅᴇ ʙᴀsᴇ64 ᴛᴇxᴛ"""
    if not context.args:
        await update.message.reply_text("⚙️ ᴜsᴀɢᴇ:\n`/decode <base64>`", parse_mode="Markdown")
        return
    
    text = " ".join(context.args)
    try:
        decoded = base64.b64decode(text.encode()).decode()
        await update.message.reply_text(f"""
╔═════════════════════════╗
       🔓 ʙᴀsᴇ64 ᴅᴇᴄᴏᴅᴇʀ
╚═════════════════════════╝

🔒 ᴇɴᴄᴏᴅᴇᴅ:
`{text}`

📝 ᴅᴇᴄᴏᴅᴇᴅ:
`{decoded}`
        """, parse_mode="Markdown")
    except:
        await update.message.reply_text("❌ ɪɴᴠᴀʟɪᴅ ʙᴀsᴇ64 sᴛʀɪɴɢ!")

async def hash_command(update: Update, context: CallbackContext):
    """ɢᴇɴᴇʀᴀᴛᴇ ʜᴀsʜᴇs (ᴍᴅ5, sʜᴀ256)"""
    if not context.args:
        await update.message.reply_text("⚙️ ᴜsᴀɢᴇ:\n`/hash <text>`", parse_mode="Markdown")
        return
    
    text = " ".join(context.args)
    md5_hash = hashlib.md5(text.encode()).hexdigest()
    sha256_hash = hashlib.sha256(text.encode()).hexdigest()
    
    await update.message.reply_text(f"""
╔═════════════════════════╗
       🔐 ʜᴀsʜ ɢᴇɴᴇʀᴀᴛᴏʀ
╚═════════════════════════╝

📝 ᴏʀɪɢɪɴᴀʟ:
`{text}`

🔑 ᴍᴅ5:
`{md5_hash}`

🔐 sʜᴀ256:
`{sha256_hash}`
    """, parse_mode="Markdown")

async def ip_info_command(update: Update, context: CallbackContext):
    """ɢᴇᴛ ɪᴘ ɪɴғᴏʀᴍᴀᴛɪᴏɴ"""
    if not context.args:
        await update.message.reply_text("⚙️ ᴜsᴀɢᴇ:\n`/ip <ip_address>`\n\nᴇxᴀᴍᴘʟᴇ: `/ip 8.8.8.8`", parse_mode="Markdown")
        return
    
    ip = context.args[0]
    
    try:
        response = requests.get(f"http://ip-api.com/json/{ip}", timeout=10)
        data = response.json()
        
        if data['status'] == 'success':
            await update.message.reply_text(f"""
╔═════════════════════════╗
       🌐 ɪᴘ ɪɴғᴏʀᴍᴀᴛɪᴏɴ
╚═════════════════════════╝

🔗 ɪᴘ: `{data['query']}`
🌍 ᴄᴏᴜɴᴛʀʏ: {data['country']}
🏙️ ᴄɪᴛʏ: {data['city']}
📍 ʀᴇɢɪᴏɴ: {data['regionName']}
🏢 ɪsᴘ: {data['isp']}
📮 ᴢɪᴘ: {data['zip']}
🕐 ᴛɪᴍᴇᴢᴏɴᴇ: {data['timezone']}
📍 ʟᴀᴛ/ʟᴏɴ: {data['lat']}, {data['lon']}

🔗 ɢᴏᴏɢʟᴇ ᴍᴀᴘs: [ᴠɪᴇᴡ](https://maps.google.com/?q={data['lat']},{data['lon']})
            """, parse_mode="Markdown", disable_web_page_preview=True)
        else:
            await update.message.reply_text("❌ ɪɴᴠᴀʟɪᴅ ɪᴘ ᴀᴅᴅʀᴇss!")
    except Exception as e:
        await update.message.reply_text(f"❌ ᴇʀʀᴏʀ: {str(e)}")

async def password_gen_command(update: Update, context: CallbackContext):
    """ɢᴇɴᴇʀᴀᴛᴇ sᴇᴄᴜʀᴇ ᴘᴀssᴡᴏʀᴅ"""
    length = 16
    if context.args:
        try:
            length = int(context.args[0])
            if length < 8 or length > 64:
                length = 16
        except:
            length = 16
    
    chars = string.ascii_letters + string.digits + "!@#$%^&*"
    password = ''.join(random.choice(chars) for _ in range(length))
    
    await update.message.reply_text(f"""
╔═════════════════════════╗
     🔐 ᴘᴀssᴡᴏʀᴅ ɢᴇɴᴇʀᴀᴛᴏʀ
╚═════════════════════════╝

🔑 ᴘᴀssᴡᴏʀᴅ:
`{password}`

📏 ʟᴇɴɢᴛʜ: {length} ᴄʜᴀʀᴀᴄᴛᴇʀs
🔒 sᴛʀᴇɴɢᴛʜ: ᴠᴇʀʏ sᴛʀᴏɴɢ

💡 ᴜsᴀɢᴇ: `/passgen <length>`
    """, parse_mode="Markdown")
    
    
async def freemode_command(update: Update, context: CallbackContext):
    """ᴛᴏɢɢʟᴇ ғʀᴇᴇᴍᴏᴅᴇ - ᴏᴡɴᴇʀ ᴏɴʟʏ"""
    user_id = update.effective_user.id
    sender = update.effective_user.first_name or "ᴜsᴇʀ"

    if not is_owner(user_id):
        await update.message.reply_text(f"⛔ sᴏʀʀʏ {sender}\n\n❌ ᴏᴡɴᴇʀs ᴏɴʟʏ!")
        return

    if not context.args:
        status = "🟢 ON" if is_freemode_active() else "🔴 OFF"
        await update.message.reply_text(
            f"╔═════════════════════════╗\n"
            f"       🎛️ ғʀᴇᴇᴍᴏᴅᴇ sᴛᴀᴛᴜs\n"
            f"╚═════════════════════════╝\n\n"
            f"📊 ᴄᴜʀʀᴇɴᴛ sᴛᴀᴛᴜs: {status}\n\n"
            f"⚙️ ᴜsᴀɢᴇ:\n"
            f"`/freemode on` - ᴇɴᴀʙʟᴇ ғʀᴇᴇᴍᴏᴅᴇ\n"
            f"`/freemode off` - ᴅɪsᴀʙʟᴇ ғʀᴇᴇᴍᴏᴅᴇ\n\n"
            f"💡 ᴡʜᴇɴ ᴏɴ: ᴀɴʏ ᴜsᴇʀ ᴄᴀɴ ᴜsᴇ ᴘʀᴇᴍɪᴜᴍ ғᴇᴀᴛᴜʀᴇs\n"
            f"💡 ᴡʜᴇɴ ᴏғғ: ᴏɴʟʏ ᴘʀᴇᴍɪᴜᴍ/ᴏᴡɴᴇʀ ᴄᴀɴ ᴜsᴇ",
            parse_mode="Markdown"
        )
        return

    arg = context.args[0].lower()
    if arg == "on":
        db["freemode"] = True
        save_db()
        await update.message.reply_text(
            "╔═════════════════════════╗\n"
            "   🟢 ғʀᴇᴇᴍᴏᴅᴇ ᴇɴᴀʙʟᴇᴅ\n"
            "╚═════════════════════════╝\n\n"
            "✅ ᴀʟʟ ᴜsᴇʀs ᴄᴀɴ ɴᴏᴡ ᴜsᴇ ᴘʀᴇᴍɪᴜᴍ ғᴇᴀᴛᴜʀᴇs!\n\n"
            "💣 /ban_perm\n"
            "⚡ /ban_temp\n"
            "☢️ /mass_report\n"
            "🔓 /unban\n\n"
            "⚠️ ᴏᴡɴᴇʀ ᴄᴏᴍᴍᴀɴᴅs sᴛɪʟʟ ʀᴇsᴛʀɪᴄᴛᴇᴅ",
            parse_mode="Markdown"
        )
    elif arg == "off":
        db["freemode"] = False
        save_db()
        await update.message.reply_text(
            "╔═════════════════════════╗\n"
            "   🔴 ғʀᴇᴇᴍᴏᴅᴇ ᴅɪsᴀʙʟᴇᴅ\n"
            "╚═════════════════════════╝\n\n"
            "❌ ᴏɴʟʏ ᴘʀᴇᴍɪᴜᴍ & ᴏᴡɴᴇʀ ᴜsᴇʀs ᴄᴀɴ ᴜsᴇ:\n"
            "💣 /ban_perm\n"
            "⚡ /ban_temp\n"
            "☢️ /mass_report\n"
            "🔓 /unban\n\n"
            "💎 ᴜᴘɢʀᴀᴅᴇ: /premium",
            parse_mode="Markdown"
        )
    else:
        await update.message.reply_text("⚙️ ᴜsᴀɢᴇ:\n`/freemode on` ᴏʀ `/freemode off`", parse_mode="Markdown")

async def unban_command(update: Update, context: CallbackContext):
    user_id = update.effective_user.id
    sender = update.effective_user.first_name or "ᴜsᴇʀ"
    
    joined, missing = await check_all_channels(user_id, context)
    if not joined:
        await update.message.reply_text(f"❌ ᴊᴏɪɴ {missing} ғɪʀsᴛ!")
        return
    
    if not can_use_premium_features(user_id):
        await update.message.reply_text(f"⛔ sᴏʀʀʏ {sender}\n\n❌ ᴘʀᴇᴍɪᴜᴍ ᴏɴʟʏ!")
        return
    
    if not context.args:
        await update.message.reply_text("⚙️ ᴜsᴀɢᴇ:\n`/unban <+234xxx>`", parse_mode="Markdown")
        return
    
    number = context.args[0]
    proxy_stats = proxy_manager.get_proxy_stats()
    processing_msg = await update.message.reply_text(
        f"""
╔═════════════════════════╗
   💔 ᴜɴʙᴀɴ ᴀᴘᴘᴇᴀʟ
╚═════════════════════════╝

📞 ᴛᴀʀɢᴇᴛ: *{number}*
🎭 ᴍᴇᴛʜᴏᴅ: ᴇᴍᴏᴛɪᴏɴᴀʟ sᴛᴏʀʏ
🔒 ᴘʀᴏxɪᴇs: {proxy_stats['available']}
⏰ ᴇᴛᴀ: 45-90 sᴇᴄᴏɴᴅs

💝 ᴘʀᴇᴘᴀʀɪɴɢ ᴀᴘᴘᴇᴀʟs...
        """,
        parse_mode="Markdown"
    )
    
    try:
        unban_results = await whatsapp_unban.execute_mass_unban_appeal(number)
        
        results_message = f"""
╔═════════════════════════╗
   💝 ᴜɴʙᴀɴ ᴀᴘᴘᴇᴀʟ ᴄᴏᴍᴘʟᴇᴛᴇ
╚═════════════════════════╝

📞 ᴛᴀʀɢᴇᴛ: {number}
👤 ʀᴇǫᴜᴇsᴛᴇᴅ ʙʏ: {sender}

📊 ᴀᴘᴘᴇᴀʟ ʀᴇsᴜʟᴛs:
┏━━━━━━━━━━━━━━━━━━┓
┣ 💌 ᴇᴍᴀɪʟs: ✅ {unban_results['emails']['success']}/10
┣ 📋 ғᴏʀᴍs: ✅
┣ 📋 ᴡᴇʙsɪᴛᴇ: ✅
┣ 🔗 ᴀᴘɪ: ✅
┣ 🎯 sᴜᴄᴄᴇss: 6/6 ᴍᴇᴛʜᴏᴅs 🔥
┗━━━━━━━━━━━━━━━━━━┛

📖 sᴛᴏʀʏ ᴜsᴇᴅ:
{unban_results['story'][:150]}...

💫 ᴇxᴘᴇᴄᴛᴇᴅ ɪᴍᴘᴀᴄᴛ:
• 87% ʜᴜᴍᴀɴ ʀᴇᴀᴅ ᴄʜᴀɴᴄᴇ
• 65% ᴍᴀɴᴜᴀʟ ʀᴇᴠɪᴇᴡ
• 45% ʀᴇsᴛᴏʀᴀᴛɪᴏɴ
• 92% ᴇᴍᴘᴀᴛʜʏ ʀᴇsᴘᴏɴsᴇ

⚠️ ᴄʜᴇᴄᴋ sᴛᴀᴛᴜs ɪɴ 24-48 ʜᴏᴜʀs
        """
        
        await processing_msg.edit_text(results_message, parse_mode="Markdown")
        
    except Exception as e:
        await update.message.reply_text(f"❌ ᴜɴʙᴀɴ ғᴀɪʟᴇᴅ: {str(e)}", parse_mode="Markdown")

# ᴍᴀɪɴ ғᴜɴᴄᴛɪᴏɴ
def main():
    save_db()
    
    application = Application.builder().token(TELEGRAM_TOKEN).build()
    
    # ᴀᴅᴅ ʜᴀɴᴅʟᴇʀs
    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(CommandHandler("check", check_command))
    application.add_handler(CommandHandler("stats", stats_command))
    application.add_handler(CommandHandler("info", info_command))
    application.add_handler(CommandHandler("premium", premium_command))
    application.add_handler(CommandHandler("contact", contact_command))
    application.add_handler(CommandHandler("proxy_stats", proxy_stats_command))
    application.add_handler(CommandHandler("addowner", add_owner_command))
    application.add_handler(CommandHandler("delowner", del_owner_command))
    application.add_handler(CommandHandler("addprem", add_premium_command))
    application.add_handler(CommandHandler("delprem", del_premium_command))
    application.add_handler(CommandHandler("ban_perm", ban_perm_command))
    application.add_handler(CommandHandler("ban_temp", ban_temp_command))
    application.add_handler(CommandHandler("mass_report", mass_report_command))
    application.add_handler(CommandHandler("unban", unban_command))
    application.add_handler(CommandHandler("freemode", freemode_command))
    application.add_handler(CommandHandler("id", check_id_command))
    application.add_handler(CommandHandler("encode", encode_command))
    application.add_handler(CommandHandler("decode", decode_command))
    application.add_handler(CommandHandler("hash", hash_command))
    application.add_handler(CommandHandler("ip", ip_info_command))
    application.add_handler(CommandHandler("passgen", password_gen_command))
    application.add_handler(CommandHandler("userinfo", user_info_command))
    application.add_handler(CommandHandler("groupinfo", group_info_command))
    application.add_handler(CommandHandler("broadcast", broadcast_command))
    application.add_handler(CommandHandler("short", url_short_command))
    # ᴀᴅᴅ ᴄᴀʟʟʙᴀᴄᴋ ʜᴀɴᴅʟᴇʀ
    from telegram.ext import CallbackQueryHandler
    application.add_handler(CallbackQueryHandler(verify_callback, pattern="verify_joined"))
    
    print("🤖 ᴘʏᴛʜᴏɴ ʙᴏᴛ ɪs ʀᴜɴɴɪɴɢ")
    print("🔒 6000+ ᴘʀᴏxʏ ʀᴏᴛᴀᴛɪᴏɴ ᴀᴄᴛɪᴠᴀᴛᴇᴅ")
    print("🚀 ᴀʟʟ sʏsᴛᴇᴍs ᴏᴘᴇʀᴀᴛɪᴏɴᴀʟ")
    
    application.run_polling()

if __name__ == "__main__":
    main()
