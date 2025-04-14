import json
import os
from fuzzywuzzy import fuzz

# Load intents from JSON
with open('intents.json', 'r', encoding='utf-8') as file:
    intents = json.load(file)

# Load saved questions/responses
QA_FILE = "saved_qas.json"
if not os.path.exists(QA_FILE):
    with open(QA_FILE, 'w', encoding='utf-8') as f:
        json.dump({}, f, ensure_ascii=False, indent=4)

def search_intents(user_input):
    for intent in intents['intents']:
        for pattern in intent['patterns']:
            if fuzz.partial_ratio(user_input, pattern) > 80:
                return intent['responses'][0], intent['tag']
    return None, None

def get_detailed_response(tag):
    for intent in intents['intents']:
        if intent['tag'] == tag:
            return intent['responses'][0]
    return None

def save_question(question, answer):
    with open(QA_FILE, 'r', encoding='utf-8') as f:
        qas = json.load(f)

    qas[question] = answer

    with open(QA_FILE, 'w', encoding='utf-8') as f:
        json.dump(qas, f, ensure_ascii=False, indent=4)

def search_local_questions(user_input):
    with open(QA_FILE, 'r', encoding='utf-8') as f:
        qas = json.load(f)

    for q, a in qas.items():
        if fuzz.partial_ratio(user_input, q) > 80:
            return a

    return None
