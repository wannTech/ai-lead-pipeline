import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def enrich_lead(lead: dict) -> dict:
    prompt = f"""
Kamu adalah analis bisnis yang berpengalaman. Analisis bisnis berikut dan berikan insight singkat.

Data bisnis:
- Nama: {lead['name']}
- Kategori: {lead['category']}
- Rating: {lead['rating']}
- Alamat: {lead['address']}
- Website: {lead['website']}

Berikan analisis dalam format JSON seperti ini:
{{
    "pain_points": "kemungkinan masalah utama bisnis ini",
    "opportunities": "peluang yang bisa ditawarkan",
    "business_size": "kecil/menengah/besar",
    "digital_presence": "lemah/sedang/kuat",
    "priority_score": 1-10
}}

Jawab HANYA dengan JSON, tanpa penjelasan tambahan.
"""

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3,
        max_tokens=300
    )

    import json
    try:
        result = json.loads(response.choices[0].message.content)
    except:
        result = {"pain_points": "N/A", "opportunities": "N/A", "business_size": "N/A", "digital_presence": "N/A", "priority_score": 5}

    lead.update(result)
    return lead


def generate_outreach_message(lead: dict) -> str:
    prompt = f"""
Kamu adalah copywriter ahli yang menulis pesan WhatsApp untuk penawaran jasa automation bisnis.

Data bisnis target:
- Nama: {lead['name']}
- Kategori: {lead['category']}
- Rating: {lead['rating']}
- Pain points: {lead.get('pain_points', 'N/A')}
- Peluang: {lead.get('opportunities', 'N/A')}

Tulis pesan WhatsApp yang:
1. Singkat (max 5 kalimat)
2. Personal, sebut nama bisnisnya
3. Tunjukkan kamu tau masalah mereka
4. Tawarkan solusi automation spesifik
5. Ada call to action yang jelas
6. Bahasa Indonesia yang natural, tidak kaku

Jawab HANYA dengan teks pesan WA-nya saja.
"""

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7,
        max_tokens=200
    )

    return response.choices[0].message.content.strip()


# Test
if __name__ == "__main__":
    test_lead = {
        "name": "Kopi Nako Depok",
        "category": "Kedai Kopi",
        "rating": "4,7",
        "address": "Jl. Margonda No.38, Depok",
        "website": "N/A",
        "phone": "0812-8237-9857"
    }

    print("🤖 Enriching lead...")
    enriched = enrich_lead(test_lead)
    print("✅ Enrichment result:")
    import json
    print(json.dumps(enriched, indent=2, ensure_ascii=False))

    print("\n✍️ Generating outreach message...")
    message = generate_outreach_message(enriched)
    print("✅ Pesan WA:")
    print(message)