# 🤖 AI-Powered Lead Generation & Research Pipeline

Sistem otomatis untuk mencari leads bisnis, menganalisis dengan AI, dan mengirim outreach yang dipersonalisasi — semua berjalan 24/7 di cloud tanpa intervensi manual.

## 🚀 Demo

- **Telegram Bot:** Ketik `/scrape restoran Jakarta` → sistem otomatis scrape, analisis AI, simpan ke Google Sheets
- **n8n Dashboard:** Workflow visual yang bisa dijadwalkan otomatis
- **Google Sheets:** Data leads lengkap dengan AI enrichment & pesan outreach

## ⚡ Tech Stack

| Layer | Technology |
|-------|-----------|
| Scraping | Python + Playwright |
| AI Engine | Groq (Llama 3.1) |
| API | FastAPI |
| Orchestration | n8n |
| Storage | Google Sheets API |
| Bot | Python Telegram Bot |
| Deployment | Railway (Cloud) |

## 🏗️ Architecture

```
[Telegram Bot] → [FastAPI] → [Playwright Scraper]
                     ↓
              [Groq AI Enrichment]
                     ↓
           [Google Sheets Storage]
                     ↓
            [n8n Orchestration]
                     ↓
          [Telegram Notification]
```

## ✨ Features

- **Multi-source scraping** — Google Maps, dapat dikembangkan ke Instagram, Tokopedia
- **AI Enrichment** — Analisis pain points, opportunities, business size per lead
- **Personalized Copywriting** — Pesan WA unik untuk tiap bisnis berdasarkan analisis AI
- **Priority Scoring** — Lead di-score 1-10 berdasarkan potensi konversi
- **Google Sheets CRM** — Data otomatis masuk dengan 15 kolom terstruktur
- **Telegram Dashboard** — Control & monitor dari HP tanpa buka laptop
- **n8n Workflow** — Visual automation yang bisa dijadwalkan
- **Full Cloud Deployment** — Jalan 24/7 di Railway tanpa perlu laptop nyala

## 📋 Pipeline Flow

```
Input: /scrape restoran Jakarta
         ↓
[Playwright] Scrape Google Maps
         ↓
[Groq AI] Enrichment per lead:
  - Pain points analysis
  - Opportunities identification
  - Business size & digital presence
  - Priority score (1-10)
         ↓
[Groq AI] Generate personalized WA message
         ↓
[Google Sheets] Auto-save semua data
         ↓
[Telegram] Laporan hasil ke user
```

## 🛠️ Setup & Installation

### Prerequisites
- Python 3.10+
- Akun Railway
- Groq API Key
- Google Cloud Service Account
- Telegram Bot Token

### Installation

```bash
git clone https://github.com/wannTech/ai-lead-pipeline
cd ai-lead-pipeline
pip install -r requirements.txt
playwright install chromium
```

### Environment Variables

```env
GROQ_API_KEY=your_groq_api_key
TELEGRAM_BOT_TOKEN=your_bot_token
TELEGRAM_CHAT_ID=your_chat_id
GOOGLE_SHEETS_ID=your_spreadsheet_id
GOOGLE_CREDENTIALS_JSON=your_service_account_json
BASE_URL=your_railway_url
```

### Run Locally

```bash
# Start API
uvicorn api.main:app --reload --port 8000

# Start Bot (terminal baru)
python bot/telegram_bot.py
```

## 📊 Output Example

| Field | Example |
|-------|---------|
| Name | Kopi Nako Depok |
| Category | Kedai Kopi |
| Rating | 4.7 |
| Phone | 0812-8237-9857 |
| Pain Points | Tidak ada website resmi |
| Opportunities | Sistem order online |
| Priority Score | 8/10 |
| Outreach Message | Halo Kopi Nako! Kami bisa... |

## 🎯 Use Cases

- **Digital Agency** — Generate leads UKM yang belum digital
- **B2B Startup** — Cari decision maker perusahaan target
- **Freelancer** — Cari klien potensial di niche tertentu
- **Marketing Team** — Otomatisin proses lead generation

## 📁 Project Structure

```
ai-lead-pipeline/
├── scraper/
│   └── google_maps.py      # Playwright scraper
├── ai/
│   └── enrichment.py       # Groq AI enrichment & copywriting
├── api/
│   ├── main.py             # FastAPI endpoints
│   └── sheets.py           # Google Sheets integration
├── bot/
│   ├── telegram_bot.py     # Telegram bot commands
│   └── run_bot.py          # Bot runner for Railway
├── n8n/
│   └── workflow_export.json # n8n workflow template
├── .env.example
├── Procfile
├── requirements.txt
└── README.md
```

## 🔗 Links

- **Portfolio:** [wanntech.github.io](https://wanntech.github.io)
- **LinkedIn:** [linkedin.com/in/hermawan-h-0a2bab356](https://linkedin.com/in/hermawan-h-0a2bab356)
- **Email:** hermawan170303@gmail.com

---

Built with ❤️ by [Hermawan](https://wanntech.github.io) | AI Automation Specialist