import os
import requests
from dotenv import load_dotenv

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

if not SUPABASE_URL or not SUPABASE_KEY:
    raise ValueError("Missing SUPABASE_URL or SUPABASE_KEY in .env")

REST_URL = f"{SUPABASE_URL}/rest/v1"

HEADERS = {
    "apikey": SUPABASE_KEY,
    "Authorization": f"Bearer {SUPABASE_KEY}",
    "Content-Type": "application/json",
    "Prefer": "return=representation"
}

def supabase_select(table, limit=100):
    url = f"{REST_URL}/{table}?select=*&order=created_at.desc&limit={limit}"
    response = requests.get(url, headers=HEADERS)
    return response.json()

def supabase_insert(table, data):
    url = f"{REST_URL}/{table}"
    response = requests.post(url, json=data, headers=HEADERS)
    return response.json()
