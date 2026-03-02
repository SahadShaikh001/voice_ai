from supabase import create_client
from app.config import SUPABASE_URL, SUPABASE_KEY

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

def save_conversation(user_text, ai_response):
    supabase.table("conversations").insert({
        "user_text": user_text,
        "ai_response": ai_response
    }).execute()