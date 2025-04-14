import wikipedia
import duckduckgo_search

# Related keywords to validate museum context
museum_keywords = ["متحف", "التحنيط", "فرعوني", "تمثال", "آثار", "مومياء", "مصر القديمة", "معرض"]

def is_museum_related(user_input):
    return any(keyword in user_input for keyword in museum_keywords)

def search_wikipedia(query):
    try:
        wikipedia.set_lang("ar")
        summary = wikipedia.summary(query, sentences=2)
        return f"📚 من ويكيبيديا:", summary
    except Exception as e:
        return None

def search_duckduckgo(query):
    try:
        results = duckduckgo_search.ddg(query, region='wt-wt', safesearch='Moderate', max_results=1)
        if results:
            result = results[0]
            return f"🔎 من DuckDuckGo:", result.get("body") or result.get("snippet")
    except Exception as e:
        return None
