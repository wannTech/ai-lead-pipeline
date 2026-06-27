import os
import json
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
from dotenv import load_dotenv

load_dotenv()

SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]

def get_sheets_service():
    import json
    creds_json = os.getenv("GOOGLE_CREDENTIALS_JSON")
    
    if creds_json:
        # Production: baca dari environment variable
        creds_info = json.loads(creds_json)
        creds = Credentials.from_service_account_info(creds_info, scopes=SCOPES)
    else:
        # Local: baca dari file
        creds = Credentials.from_service_account_file(
            os.getenv("GOOGLE_CREDENTIALS_PATH"),
            scopes=SCOPES
        )
    
    return build("sheets", "v4", credentials=creds)

def save_leads_to_sheets(leads: list[dict], spreadsheet_id: str = None):
    if not spreadsheet_id:
        spreadsheet_id = os.getenv("GOOGLE_SHEETS_ID")

    service = get_sheets_service()
    sheet = service.spreadsheets()

    # Header
    headers = [
        "Name", "Category", "Rating", "Phone", "Address", "Website",
        "Keyword", "Location", "Pain Points", "Opportunities",
        "Business Size", "Digital Presence", "Priority Score",
        "Outreach Message", "Status"
    ]

    # Rows
    rows = []
    for lead in leads:
        rows.append([
            lead.get("name", ""),
            lead.get("category", ""),
            lead.get("rating", ""),
            lead.get("phone", ""),
            lead.get("address", ""),
            lead.get("website", ""),
            lead.get("keyword", ""),
            lead.get("location", ""),
            lead.get("pain_points", ""),
            lead.get("opportunities", ""),
            lead.get("business_size", ""),
            lead.get("digital_presence", ""),
            str(lead.get("priority_score", "")),
            lead.get("outreach_message", ""),
            lead.get("status", "pending")
        ])

    # Cek apakah sheet sudah ada header
    result = sheet.values().get(
        spreadsheetId=spreadsheet_id,
        range="Sheet1!A1:A1"
    ).execute()

    existing = result.get("values", [])

    if not existing:
        # Tulis header dulu
        sheet.values().update(
            spreadsheetId=spreadsheet_id,
            range="Sheet1!A1",
            valueInputOption="RAW",
            body={"values": [headers]}
        ).execute()
        next_row = 2
    else:
        # Cari baris terakhir
        result2 = sheet.values().get(
            spreadsheetId=spreadsheet_id,
            range="Sheet1!A:A"
        ).execute()
        next_row = len(result2.get("values", [])) + 1

    # Tulis data
    range_name = f"Sheet1!A{next_row}"
    sheet.values().update(
        spreadsheetId=spreadsheet_id,
        range=range_name,
        valueInputOption="RAW",
        body={"values": rows}
    ).execute()

    print(f"✅ {len(leads)} leads saved to Google Sheets (row {next_row})")
    return len(leads)


# Test
if __name__ == "__main__":
    test_leads = [
        {
            "name": "Kopi Nako Depok",
            "category": "Kedai Kopi",
            "rating": "4,7",
            "phone": "0812-8237-9857",
            "address": "Jl. Margonda No.38, Depok",
            "website": "N/A",
            "keyword": "restoran",
            "location": "Depok",
            "pain_points": "Tidak ada website resmi",
            "opportunities": "Bisa pakai sistem order online",
            "business_size": "kecil",
            "digital_presence": "lemah",
            "priority_score": 8,
            "outreach_message": "Halo Kopi Nako! Kami bisa bantu digitalisasi bisnis kamu.",
            "status": "pending"
        }
    ]
    save_leads_to_sheets(test_leads)