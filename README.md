# 🤖 AI-Powered Lead Generation & Research Pipeline

[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?logo=python&logoColor=white)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-009688?logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![Playwright](https://img.shields.io/badge/Playwright-Automation-2EAD33?logo=microsoft&logoColor=white)](https://playwright.dev)
[![Groq AI](https://img.shields.io/badge/Groq-Llama_3.1-FF6B00?logo=&logoColor=white)](https://groq.com)
[![Railway](https://img.shields.io/badge/Railway-Deployed-0B0D0E?logo=railway&logoColor=white)](https://railway.app)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

Sistem otomatis untuk mencari leads bisnis, menganalisis dengan AI, dan mengirim outreach yang dipersonalisasi — **berjalan 24/7 di cloud tanpa intervensi manual**.

## 🎬 Quick Demo

```bash
# Telegram Command
/scrape restoran Jakarta

# Sistem melakukan:
✅ Scrape Google Maps (20-50 leads)
✅ AI Enrichment (pain points, opportunities)
✅ Generate personalized WA messages
✅ Auto-save ke Google Sheets
✅ Kirim laporan ke Telegram
⏱️ Waktu eksekusi: ~2-3 menit
```

## 🚀 Key Features

| Feature | Detail |
|---------|--------|
| 🗺️ **Multi-source Scraping** | Google Maps, dapat dikembangkan ke Instagram, Tokopedia |
| 🧠 **AI Enrichment** | Analisis pain points, opportunities, business size per lead |
| ✍️ **Personalized Copywriting** | Pesan WA unik untuk tiap bisnis berdasarkan AI analysis |
| 📊 **Priority Scoring** | Lead di-score 1-10 berdasarkan potensi konversi |
| 📋 **Google Sheets CRM** | Data otomatis masuk dengan 15 kolom terstruktur |
| 🤖 **Telegram Dashboard** | Control & monitor dari HP (commands: `/scrape`, `/status`, `/export`) |
| 🔄 **n8n Workflow** | Visual automation yang bisa dijadwalkan (daily, weekly, monthly) |
| ☁️ **Full Cloud Deployment** | Railway → Jalan 24/7, zero maintenance |

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────┐
│              TELEGRAM BOT (Command Interface)            │
└──────────────────────┬──────────────────────────────────┘
                       │ /scrape restoran Jakarta
                       ▼
┌─────────────────────────────────────────────────────────┐
│         FASTAPI (Orchestration & API)                    │
│  • Request validation                                    │
│  • Queue management                                      │
│  • Response formatting                                   │
└──────────────┬──────────────────────────┬────────────────┘
               │                          │
        ▼      ▼                          ▼
┌────────────────────┐  ┌──────────────────────────────┐
│ PLAYWRIGHT SCRAPER │  │  GROQ AI ENRICHMENT         │
│ • Google Maps      │  │  • Pain point analysis       │
│ • Extract data     │  │  • Opportunity scoring       │
│ • Smart pagination │  │  • Business profiling        │
└────────────┬───────┘  └──────────────┬───────────────┘
             │                         │
             └────────────┬────────────┘
                          ▼
            ┌──────────────────────────┐
            │ GOOGLE SHEETS CRM         │
            │ • Structured data storage │
            │ • 15 column schema        │
            │ • Real-time updates       │
            └──────────┬────────────────┘
                       │
        ┌──────────────┼──────────────┐
        ▼              ▼              ▼
    [N8N]      [TELEGRAM]       [EMAIL]
   Workflow    Notifications    (optional)
```

## ⚡ Tech Stack

| Layer | Technology | Purpose |
|-------|-----------|---------|
| **Scraping** | Playwright (Chromium) | Reliable, handles JS-heavy Google Maps |
| **AI Engine** | Groq Llama 3.1 (70B) | Fast, low-cost, 8K context window |
| **API Backend** | FastAPI + Uvicorn | Async, high-performance, auto-docs |
| **Database** | Google Sheets API | Structured, shareable, pivot-friendly |
| **Bot** | python-telegram-bot | Command-based interface, webhooks |
| **Orchestration** | n8n | Visual workflows, scheduling, integrations |
| **Deployment** | Railway | One-click deploy, auto-restart, logs |

## 📊 Pipeline Flow (Step-by-Step)

```
INPUT: /scrape restoran Jakarta
  │
  ├─→ [Parse Command] Extract query, parameters
  │
  ├─→ [Playwright Scraper]
  │   └─→ Google Maps search
  │   └─→ Extract 20-50 leads (name, phone, rating, reviews)
  │   └─→ Rate limiting (2-3 sec per lead)
  │
  ├─→ [Groq AI Enrichment] For each lead:
  │   ├─→ Analyze reviews → pain points
  │   ├─→ Assess potential → opportunities
  │   ├─→ Estimate business size → budget category
  │   └─→ Generate priority score (1-10)
  │
  ├─→ [Groq AI Copywriting]
  │   └─→ Create personalized WA message based on analysis
  │
  ├─→ [Google Sheets]
  │   └─→ Auto-append row with all data (15 columns)
  │
  ├─→ [Telegram Report]
  │   ├─→ Summary: "Found 32 leads, avg score 7.2"
  │   ├─→ Top 5 leads with priority score
  │   └─→ Link to Google Sheets
  │
  └─→ [N8N Webhook] (optional)
      └─→ Trigger additional workflows (email, SMS, etc)

TOTAL TIME: ~2-3 minutes for 50 leads
```

## 🛠️ Setup & Installation

### Prerequisites
```bash
# System Requirements
- Python 3.10+
- Git
- 1GB RAM (minimum)

# API Keys (Free)
- Groq API Key (groq.com) — Free tier: 30 requests/min
- Telegram Bot Token (BotFather on Telegram)
- Google Cloud Service Account (JSON key)
```

### Local Setup (5 minutes)

```bash
# 1. Clone repository
git clone https://github.com/wannTech/ai-lead-pipeline
cd ai-lead-pipeline

# 2. Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt
playwright install chromium

# 4. Setup environment variables
cp .env.example .env
nano .env  # Edit with your keys

# 5. Run services (Terminal 1)
uvicorn api.main:app --reload --port 8000

# 6. Run bot (Terminal 2)
python bot/telegram_bot.py

# 7. Test
# Go to Telegram → @YourBotName → Type: /scrape coffee Jakarta
```

### Environment Variables
```env
# Groq AI
GROQ_API_KEY=gsk_xxxxxxxxxxxxxxxxxxxxxxx
GROQ_MODEL=llama-3.1-70b-versatile

# Telegram
TELEGRAM_BOT_TOKEN=123456789:ABCDefGhijKlmnOpqrstuVwxyz
TELEGRAM_CHAT_ID=987654321

# Google Sheets
GOOGLE_SHEETS_ID=1xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
GOOGLE_CREDENTIALS_JSON={"type":"service_account",...}

# Deployment (Railway)
BASE_URL=https://ai-lead-pipeline-production.up.railway.app
ENVIRONMENT=production
```

### Deployment on Railway (Recommended)

```bash
# 1. Push to GitHub
git push origin main

# 2. Connect to Railway
# Visit: railway.app/dashboard
# → New Project → GitHub → Select this repo

# 3. Add environment variables in Railway Dashboard
# (Same as .env file)

# 4. Deploy
# Railway auto-deploys on push. Takes ~2 minutes

# 5. Get URL and set webhook
# Your bot URL: https://<your-railway-url>/telegram/webhook
```

## 📊 Output Example

**Google Sheets CRM** (auto-populated):

| Name | Category | Rating | Phone | Pain Points | Opportunities | Budget | Score | WA Message |
|------|----------|--------|-------|---|---|---|---|---|
| Kopi Nako Depok | Kedai Kopi | 4.7 | 0812-8237-9857 | Tidak ada website | Sistem order online | UKM | 8/10 | Halo Kopi Nako! 👋 Kami bantu... |
| Ayam Goreng Mas Ade | Restoran | 4.5 | 0821-5555-5555 | Manual order via chat | Booking system | UKM | 7/10 | Hai Mas Ade! Sistem booking... |

**Telegram Report**:
```
✅ Scrape Complete!

📊 Results:
- Total leads: 32
- Avg priority score: 7.3/10
- Processing time: 2m 45s

🏆 Top 5 Targets:
1. Kopi Nako Depok (Score: 8/10)
2. Ayam Goreng Mas Ade (Score: 7/10)
3. Restoran Padang Murah (Score: 7/10)
...

📋 Full data saved to Google Sheets:
https://sheets.google.com/d/1xxxxx

⏭️ Next: /export to download CSV
```

## 🎯 Use Cases

### 1. **Digital Agency** 💼
- Generate leads UKM yang belum digital
- Pitch custom website/mobile app
- Expected conversion: 5-10% dari leads

### 2. **B2B Startup** 🚀
- Cari decision maker perusahaan target
- Personalized outreach dengan insights
- Build customer list untuk cold email

### 3. **Freelancer (Developer, Designer)** 👨‍💻
- Cari klien potensial di niche tertentu
- Automate outreach untuk 50+ prospects/hari
- Track interest via CRM

### 4. **Marketing Team** 📈
- Scale lead generation tanpa tambah headcount
- A/B test messaging
- Measure conversion funnel

## 📈 Performance Metrics

```
Scraping Speed: 2-3 leads/second
AI Processing: ~10 leads/minute
Pipeline Throughput: 50 leads in ~2-3 minutes
Google Sheets Write: Batched (1 API call per 100 rows)
Telegram Response: <1 second (queued processing)
```

## 🔧 Customization Examples

### Add Instagram Scraping
```python
# In scraper/
from scrapers.instagram_scraper import InstagramScraper

scraper = InstagramScraper()
leads = scraper.search_hashtag("#kedaiKopi", limit=30)
```

### Change AI Model
```python
# In ai/enrichment.py
from groq import Groq

client = Groq(api_key=os.getenv("GROQ_API_KEY"))
# Switch to: llama-3-8b-8192 (faster, cheaper)
# Or: mixtral-8x7b-32768 (multimodal capable)
```

### Custom Telegram Commands
```python
# In bot/telegram_bot.py
@app.message_handler(commands=['mynewcommand'])
def my_command(message):
    chat_id = message.chat.id
    # Your custom logic
    bot.send_message(chat_id, "Response")
```

## 📁 Project Structure

```
ai-lead-pipeline/
│
├── scraper/
│   ├── google_maps.py      # Playwright scraper, rate limiting
│   └── utils.py            # Helper functions
│
├── ai/
│   ├── enrichment.py       # Groq API calls, pain point analysis
│   ├── copywriter.py       # Generate personalized messages
│   └── prompts.py          # System prompts for AI
│
├── api/
│   ├── main.py             # FastAPI app, routes
│   ├── sheets.py           # Google Sheets integration
│   ├── models.py           # Pydantic schemas
│   └── config.py           # Configuration
│
├── bot/
│   ├── telegram_bot.py     # Telegram bot handler
│   ├── handlers/
│   │   ├── scrape_handler.py
│   │   ├── status_handler.py
│   │   └── export_handler.py
│   └── run_bot.py          # Entry point for Railway
│
├── n8n/
│   ├── workflow_export.json # N8N workflow template
│   └── README_WORKFLOW.md  # N8N setup guide
│
├── tests/
│   ├── test_scraper.py
│   ├── test_ai.py
│   └── test_api.py
│
├── .github/workflows/
│   ├── deploy.yml          # Auto-deploy on push
│   └── tests.yml           # Run tests on PR
│
├── docker/
│   ├── Dockerfile
│   └── docker-compose.yml
│
├── .env.example
├── requirements.txt
├── Procfile
├── railway.toml
└── README.md
```

## 🚀 Deployment Status

- ✅ **Local Development**: Ready (see Setup guide)
- ✅ **Railway Deployment**: Configured (railway.toml included)
- ✅ **Docker**: Dockerfile included
- 🔄 **N8N Workflows**: Template included (setup needed)
- ⏳ **GitHub Actions**: CI/CD pipeline in progress

## 📚 Documentation

| Doc | Purpose |
|-----|---------|
| [SETUP.md](docs/SETUP.md) | Detailed installation & configuration |
| [ARCHITECTURE.md](docs/ARCHITECTURE.md) | System design & data flow |
| [API_DOCS.md](docs/API_DOCS.md) | FastAPI endpoint reference |
| [N8N_SETUP.md](docs/N8N_SETUP.md) | N8N workflow setup guide |
| [TROUBLESHOOTING.md](docs/TROUBLESHOOTING.md) | Common issues & solutions |

## 🤝 Contributing

Found a bug or have a feature request?
- Open an issue on GitHub
- Submit a PR with improvements
- Share ideas in Discussions

## 📞 Support & Contact

- **Portfolio**: [wanntech.github.io](https://wanntech.github.io)
- **LinkedIn**: [hermawan-h-0a2bab356](https://linkedin.com/in/hermawan-h-0a2bab356)
- **Email**: hermawan170303@gmail.com
- **GitHub Issues**: [Report bugs](https://github.com/wannTech/ai-lead-pipeline/issues)

## 📄 License

MIT License — Feel free to use, modify, and distribute. See [LICENSE](LICENSE) file.

## ⭐ If This Helped You

Show some love by starring this repo! It helps other developers discover the project.

---

**Built with ❤️ by [Hermawan](https://wanntech.github.io)**  
*AI Automation Specialist | Python Developer | Open Source Contributor*
