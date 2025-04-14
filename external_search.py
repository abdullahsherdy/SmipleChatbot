from duckduckgo_search import DDGS
import wikipedia
import google.generativeai as genai
from dotenv import load_dotenv
import os

load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)

def search_wikipedia(query):
    try:
        wikipedia.set_lang("ar")
        return wikipedia.summary(query, sentences=2)
    except:
        return None

def search_gemini(query):
    try:
        model = genai.GenerativeModel("gemini-pro")
        res = model.generate_content(f"أجب باختصار حول: {query}")
        return res.text if query.lower() in res.text.lower() else None
    except Exception as e:
        print("Gemini error:", e)
        return None

def search_duckduckgo(query):
    try:
        with DDGS() as ddgs:
            results = list(ddgs.text(query, max_results=2))
        return results[0]['body'] if results else None
    except:
        return None

def external_fallback(query):
    return search_wikipedia(query) or search_gemini(query) or search_duckduckgo(query) or "❌ لم أتمكن من العثور على إجابة."

def is_museum_related(q):
    keywords = ["متحف", "فرعونية", "آثار", "توت", "رمسيس", "الأهرامات", "تمثال", "قاعة", "حتشبسوت"]
    return any(k in q.lower() for k in keywords)
