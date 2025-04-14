import json
from difflib import get_close_matches

QUESTIONS_FILE = "questions.json"
INTENTS_FILE = "intents.json"

try:
    with open(QUESTIONS_FILE, "r", encoding="utf-8") as f:
        questions_data = json.load(f)
except:
    questions_data = {}

try:
    with open(INTENTS_FILE, "r", encoding="utf-8") as f:
        intents_data = json.load(f)
except:
    intents_data = {"intents": []}

last_user_tag = None

def is_valid_question(q):
    return len(q) > 2 and not q.isdigit()

def save_question(q, a):
    if is_valid_question(q) and a not in ["❌ لم أتمكن من العثور على إجابة.", "مع السلامة", "إلى اللقاء", "سلام"]:
        questions_data[q] = a
        with open(QUESTIONS_FILE, "w", encoding="utf-8") as f:
            json.dump(questions_data, f, ensure_ascii=False, indent=4)

def fuzzy_match(q, data):
    keys = list(data.keys())
    matches = get_close_matches(q.lower(), keys, n=1, cutoff=0.6)
    return data[matches[0]] if matches else None

def search_local_response(question):
    global last_user_tag
    for intent in intents_data["intents"]:
        patterns = intent.get("patterns", [])
        if get_close_matches(question, patterns, n=1, cutoff=0.6):
            last_user_tag = intent.get("tag")
            return intent.get("responses", [""])[0], last_user_tag

    answer = fuzzy_match(question, questions_data)
    return (answer, None) if answer else (None, None)

def get_detailed_response(question):
    detail_words = ["شرح", "تفصيل", "تفصيلي", "أكتر", "expand", "more", "وضح"]
    if any(w in question.lower() for w in detail_words) and last_user_tag:
        for intent in intents_data.get("intents", []):
            if intent.get("tag") == last_user_tag and "detailed_response" in intent:
                return intent["detailed_response"]
    return None
