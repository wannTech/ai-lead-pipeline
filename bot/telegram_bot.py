import os
import sys
import asyncio
import requests
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
from dotenv import load_dotenv

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
load_dotenv()

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
BASE_URL = os.getenv("BASE_URL", "https://ai-lead-pipeline-production-f255.up.railway.app")

# ── Commands ──
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🤖 *AI Lead Pipeline Bot*\n\n"
        "Commands:\n"
        "/scrape [keyword] [lokasi] - Mulai scraping\n"
        "/status [job_id] - Cek status job\n"
        "/leads [job_id] - Lihat hasil leads\n"
        "/jobs - Lihat semua job\n"
        "/help - Bantuan",
        parse_mode="Markdown"
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "📖 *Cara pakai:*\n\n"
        "1. `/scrape restoran Depok` - scrape restoran di Depok\n"
        "2. Bot balas dengan job_id\n"
        "3. `/status abc123` - cek apakah sudah selesai\n"
        "4. `/leads abc123` - lihat hasil leads\n\n"
        "💡 Tunggu 2-3 menit setelah scrape sebelum cek status.",
        parse_mode="Markdown"
    )

async def scrape(update: Update, context: ContextTypes.DEFAULT_TYPE):
    args = context.args
    if len(args) < 2:
        await update.message.reply_text(
            "❌ Format salah!\nGunakan: /scrape [keyword] [lokasi]\n"
            "Contoh: /scrape restoran Depok"
        )
        return

    keyword = args[0]
    location = " ".join(args[1:])

    await update.message.reply_text(f"⏳ Memulai scraping *{keyword}* di *{location}*...", parse_mode="Markdown")

    try:
        response = requests.post(f"{BASE_URL}/scrape", json={
            "keyword": keyword,
            "location": location,
            "max_results": 20
        })
        data = response.json()
        job_id = data["job_id"]

        await update.message.reply_text(
            f"✅ Job dimulai!\n\n"
            f"🆔 Job ID: `{job_id}`\n"
            f"⏱ Tunggu 2-3 menit, lalu ketik:\n"
            f"`/status {job_id}`",
            parse_mode="Markdown"
        )
    except Exception as e:
        await update.message.reply_text(f"❌ Error: {str(e)}")

async def status(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("❌ Gunakan: /status [job_id]")
        return

    job_id = context.args[0]
    try:
        response = requests.get(f"{BASE_URL}/status/{job_id}")
        data = response.json()

        emoji = {"queued": "⏳", "running": "🔄", "done": "✅", "error": "❌"}
        status_emoji = emoji.get(data["status"], "❓")

        await update.message.reply_text(
            f"{status_emoji} *Status Job* `{job_id}`\n\n"
            f"Status: *{data['status']}*\n"
            f"Total leads: *{data['total']}*\n\n"
            f"{'Ketik /leads ' + job_id + ' untuk lihat hasil!' if data['status'] == 'done' else ''}",
            parse_mode="Markdown"
        )
    except Exception as e:
        await update.message.reply_text(f"❌ Error: {str(e)}")

async def leads(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("❌ Gunakan: /leads [job_id]")
        return

    job_id = context.args[0]
    try:
        response = requests.get(f"{BASE_URL}/leads/{job_id}")
        data = response.json()

        if not data["leads"]:
            await update.message.reply_text("⏳ Leads belum siap, coba lagi nanti.")
            return

        msg = f"📊 *Hasil Leads* - Total: {data['total']}\n\n"
        for i, lead in enumerate(data["leads"][:5], 1):
            msg += (
                f"*{i}. {lead['name']}*\n"
                f"📂 {lead['category']} | ⭐ {lead['rating']}\n"
                f"📞 {lead['phone']}\n"
                f"🎯 Score: {lead.get('priority_score', 'N/A')}/10\n\n"
            )

        if data["total"] > 5:
            msg += f"_...dan {data['total'] - 5} leads lainnya di CSV_"

        await update.message.reply_text(msg, parse_mode="Markdown")

    except Exception as e:
        await update.message.reply_text(f"❌ Error: {str(e)}")

async def jobs_list(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        response = requests.get(f"{BASE_URL}/jobs")
        data = response.json()

        if not data["jobs"]:
            await update.message.reply_text("📭 Belum ada job yang berjalan.")
            return

        msg = "📋 *Semua Jobs:*\n\n"
        for job in data["jobs"]:
            emoji = {"queued": "⏳", "running": "🔄", "done": "✅", "error": "❌"}
            e = emoji.get(job["status"], "❓")
            msg += f"{e} `{job['job_id']}` - {job['status']} ({job['total']} leads)\n"

        await update.message.reply_text(msg, parse_mode="Markdown")
    except Exception as e:
        await update.message.reply_text(f"❌ Error: {str(e)}")


# ── Main ──
def main():
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("scrape", scrape))
    app.add_handler(CommandHandler("status", status))
    app.add_handler(CommandHandler("leads", leads))
    app.add_handler(CommandHandler("jobs", jobs_list))

    print("🤖 Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()