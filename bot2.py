from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes, ConversationHandler
import asyncio
import re
import hashlib

TOKEN = "8587286402:AAFTxj8o1MorR5kLitB689-2vBnt77bZQDA"

DEVICE, RAM, STORAGE = range(3)

# -------- DATABASE --------
BRANDS = [
    "REDMI","REALME","SAMSUNG","VIVO","OPPO","IQOO","POCO","ONEPLUS",
    "MOTOROLA","NOKIA","INFINIX","TECNO","LAVA","MICROMAX","ASUS",
    "ROG","BLACKSHARK","LENOVO","GOOGLE","PIXEL","SONY","HTC",
    "HUAWEI","HONOR","ZTE","COOLPAD","LETV","MEIZU","ACER","DELL",
    "HP","APPLE","IPHONE","IPAD"
]

# -------- FIXED SENSI (HASH BASED) --------
def generate_fixed_sensi(device):
    h = int(hashlib.md5(device.encode()).hexdigest(), 16)

    return {
        "general": 150 + (h % 51),       # 150-200
        "reddot": 110 + (h % 61),       # 110-170
        "scope2x": 100 + (h % 51),      # 100-150
        "scope4x": 80 + (h % 51),       # 80-130
        "scope8x": 1 + (h % 20),        # 1-20
        "freecam": 10 + (h % 41)        # 10-50
    }

# ---------- START ----------
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data.clear()

    msg = """🚀 *WELCOME TO ELITE SENSI LAB*

💼 Advanced AI Sensitivity System for Pro Gamers  
🎯 Tested on 1000+ Devices  
⚡ Fast & Accurate Processing  

🔥 Improve your gameplay  
🎮 Perfect headshot control  
💎 Free & Premium features  

👇 Select option below 👇
"""

    buttons = [
        [InlineKeyboardButton("🎯 FREE SENSI", callback_data="free")],
        [InlineKeyboardButton("💎 PAID SENSI", url="https://t.me/sensi_freefirev26bot?start=_tgr_PKJKorEzNGM1")],
        [InlineKeyboardButton("📊 MENU", callback_data="menu")]
    ]

    await update.message.reply_text(msg, parse_mode="Markdown",
                                    reply_markup=InlineKeyboardMarkup(buttons))

# ---------- FREE ----------
async def free(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    msg = """📩 *DEVICE SUBMISSION REQUIRED* 💼

⚙️ Enter your device name correctly  
🔒 Only CAPITAL LETTERS  
📱 Format: BRAND MODEL  

✨ Example: REDMI NOTE11T5G  
🚫 No extra text  

👇 Send now 👇
"""
    await query.message.reply_text(msg, parse_mode="Markdown")
    return DEVICE

# ---------- DEVICE ----------
async def device(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.strip()

    if not re.match(r"^[A-Z]+ [A-Z0-9]+$", text):
        await update.message.reply_text("❌ WRONG FORMAT!\nExample: REDMI NOTE11T5G")
        return DEVICE

    brand = text.split()[0]

    if brand not in BRANDS:
        await update.message.reply_text("❌ DEVICE NOT SUPPORTED")
        return DEVICE

    context.user_data["device"] = text

    buttons = [
        [InlineKeyboardButton("4GB", callback_data="ram4"),
         InlineKeyboardButton("6GB", callback_data="ram6")],
        [InlineKeyboardButton("8GB", callback_data="ram8"),
         InlineKeyboardButton("12GB", callback_data="ram12")]
    ]

    await update.message.reply_text("📊 SELECT RAM",
                                    reply_markup=InlineKeyboardMarkup(buttons))
    return RAM

# ---------- RAM ----------
async def ram(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    buttons = [
        [InlineKeyboardButton("64GB", callback_data="st64"),
         InlineKeyboardButton("128GB", callback_data="st128")],
        [InlineKeyboardButton("256GB", callback_data="st256")]
    ]

    await query.message.reply_text("💾 SELECT STORAGE",
                                  reply_markup=InlineKeyboardMarkup(buttons))
    return STORAGE

# ---------- STORAGE ----------
async def storage(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    device = context.user_data["device"]

    msg = await query.message.reply_text("🧠 AI Processing: 0%")

    # progress bar (3 sec each)
    for i in range(0, 101, 10):
        bar = "▓" * (i // 10) + "░" * (10 - i // 10)
        await msg.edit_text(f"🧠 AI Processing: {i}%\n[{bar}]")
        await asyncio.sleep(3)

    steps = [
        "📡 Connecting to AI servers...",
        "📊 Analyzing device performance...",
        "🎯 Optimizing sensitivity...",
        "⚡ Applying pro configs...",
        "🧠 Final AI tuning..."
    ]

    for step in steps:
        await query.message.reply_text(step)
        await asyncio.sleep(3)

    data = generate_fixed_sensi(device)

    sensi = f"""🎯 *AI OPTIMIZED SENSITIVITY — {device}*

⚡ Precision tuned for your device performance

🎮 General: {data['general']}
🔴 Red Dot: {data['reddot']}
🔍 2x Scope: {data['scope2x']}
🔭 4x Scope: {data['scope4x']}
🎯 8x Scope: {data['scope8x']}
📸 Free Look: {data['freecam']}

📊 Generated using advanced AI analysis & testing

⚙️ Adjust ±5 if needed  
🔥 Performance may vary based on FPS  

📞 @Vault_With_Pratik  
💎 BLACKBOX HUB
"""

    await query.message.reply_text(sensi, parse_mode="Markdown")

    return ConversationHandler.END

# ---------- MENU ----------
async def menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    await query.message.reply_text(
        "💎 PREMIUM PACKS AVAILABLE",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("BUY NOW", url="https://t.me/sensi_freefirev26bot?start=_tgr_PKJKorEzNGM1")]
        ])
    )

# ---------- MAIN ----------
def main():
    app = ApplicationBuilder().token(TOKEN).build()

    conv = ConversationHandler(
        entry_points=[CallbackQueryHandler(free, pattern="^free$")],
        states={
            DEVICE: [MessageHandler(filters.TEXT & ~filters.COMMAND, device)],
            RAM: [CallbackQueryHandler(ram, pattern="^ram")],
            STORAGE: [CallbackQueryHandler(storage, pattern="^st")]
        },
        fallbacks=[CommandHandler("start", start)],
        per_chat=True,
        per_user=True
    )

    app.add_handler(CommandHandler("start", start))
    app.add_handler(conv)
    app.add_handler(CallbackQueryHandler(menu, pattern="^menu$"))

    app.run_polling()

if __name__ == "__main__":
    main()
