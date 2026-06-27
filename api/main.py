from api.sheets import save_leads_to_sheets
from fastapi import FastAPI, BackgroundTasks
from pydantic import BaseModel
import asyncio
import sys
import os
import uuid
import json

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from scraper.google_maps import scrape_google_maps, save_to_csv
from ai.enrichment import enrich_lead, generate_outreach_message
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(title="AI Lead Pipeline API")

# Simpan status job di memory
jobs = {}


class ScrapeRequest(BaseModel):
    keyword: str
    location: str
    max_results: int = 20


class EnrichRequest(BaseModel):
    leads: list[dict]


# ── Background job scraper ──
async def run_scrape_job(job_id: str, keyword: str, location: str, max_results: int):
    jobs[job_id]["status"] = "running"
    try:
        import concurrent.futures
        loop = asyncio.get_event_loop()
        
        def run_sync():
            new_loop = asyncio.ProactorEventLoop()
            asyncio.set_event_loop(new_loop)
            try:
                return new_loop.run_until_complete(
                    scrape_google_maps(keyword, location, max_results)
                )
            finally:
                new_loop.close()

        with concurrent.futures.ThreadPoolExecutor() as pool:
            results = await loop.run_in_executor(pool, run_sync)

        # Enrich semua leads
        enriched = []
        for lead in results:
            lead = enrich_lead(lead)
            lead["outreach_message"] = generate_outreach_message(lead)
            enriched.append(lead)

        save_to_csv(enriched, f"leads_{job_id}.csv")
        save_leads_to_sheets(enriched)  # ← tambah ini
        jobs[job_id]["status"] = "done"
        jobs[job_id]["leads"] = enriched
        jobs[job_id]["total"] = len(enriched)

    except Exception as e:
        jobs[job_id]["status"] = "error"
        jobs[job_id]["error"] = str(e)


# ── Endpoints ──
@app.get("/")
def root():
    return {"message": "AI Lead Pipeline API is running 🚀"}


@app.post("/scrape")
async def start_scrape(req: ScrapeRequest, background_tasks: BackgroundTasks):
    job_id = str(uuid.uuid4())[:8]
    jobs[job_id] = {"status": "queued", "leads": [], "total": 0}
    background_tasks.add_task(
        run_scrape_job, job_id, req.keyword, req.location, req.max_results
    )
    return {"job_id": job_id, "message": "Scraping dimulai!"}


@app.get("/status/{job_id}")
def get_status(job_id: str):
    if job_id not in jobs:
        return {"error": "Job tidak ditemukan"}
    return {
        "job_id": job_id,
        "status": jobs[job_id]["status"],
        "total": jobs[job_id].get("total", 0)
    }


@app.get("/leads/{job_id}")
def get_leads(job_id: str):
    if job_id not in jobs:
        return {"error": "Job tidak ditemukan"}
    return {
        "job_id": job_id,
        "total": jobs[job_id].get("total", 0),
        "leads": jobs[job_id].get("leads", [])
    }


@app.get("/jobs")
def list_jobs():
    return {"jobs": [{"job_id": k, "status": v["status"], "total": v.get("total", 0)} for k, v in jobs.items()]}