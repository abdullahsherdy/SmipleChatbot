import os
import json
import random
import torch
from dotenv import load_dotenv

import google.generativeai as genai

from model import NeuralNet
from nltk_utils import bag_of_words, tokenize

# Load environment
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=GEMINI_API_KEY)

# Load intents
with open('intents.json', 'r', encoding='utf-8') as json_data:
    intents = json.load(json_data)

# Load local model
FILE = "data.pth"
data = torch.load(FILE)
input_size = data["input_size"]
hidden_size = data["hidden_size"]
output_size = data["output_size"]
all_words = data['all_words']
tags = data['tags']
model_state = data["model_state"]

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
model = NeuralNet(input_size, hidden_size, output_size).to(device)
model.load_state_dict(model_state)
model.eval()

TOUR_GUIDE_PROMPT = """
أنت مرشد سياحي ذكي في المتحف المصري.
أجب على السؤال التالي بدقة وبأسلوب ودود، مع توضيحات تاريخية إن أمكن.
السؤال: "{question}"
"""

def get_local_response(msg):
    sentence = tokenize(msg)
    X = bag_of_words(sentence, all_words)
    X = X.reshape(1, X.shape[0])
    X = torch.from_numpy(X).to(device)

    output = model(X)
    _, predicted = torch.max(output, dim=1)
    tag = tags[predicted.item()]

    probs = torch.softmax(output, dim=1)
    prob = probs[0][predicted.item()]
    if prob.item() > 0.75:
        for intent in intents['intents']:
            if tag == intent["tag"]:
                return random.choice(intent['responses'])
    return None  # Fallback if not confident


def get_gemini_response(msg):
    try:
        prompt = TOUR_GUIDE_PROMPT.format(question=msg)
        model = genai.GenerativeModel("gemini-pro")
        response = model.generate_content(prompt)
        return response.text.strip() if response.text else None
    except Exception as e:
        print(f"[Gemini Error] {e}")
        return None


def get_response(msg):
    local_reply = get_local_response(msg)
    if local_reply:
        return local_reply

    gemini_reply = get_gemini_response(msg)
    if gemini_reply:
        return gemini_reply

    return "❌ لم أتمكن من فهم سؤالك. هل يمكنك إعادة صياغته؟"


# CLI test
if __name__ == "__main__":
    print("📜 Museum Chatbot is online! (type 'quit' to exit)")
    while True:
        sentence = input("🧑‍💻 You: ")
        if sentence.lower() == "quit":
            break
        response = get_response(sentence)
        print("🤖 Bot:", response)
