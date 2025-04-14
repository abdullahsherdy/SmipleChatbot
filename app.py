from flask import Flask, render_template, request, jsonify
from deep_translator import GoogleTranslator
import langdetect
from chat import get_gemini_response
from local_match import search_intents, get_detailed_response, search_local_questions, save_question
from external_search import search_wikipedia, search_duckduckgo, is_museum_related

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('base.html')

@app.route('/get_response', methods=['POST'])
def get_bot_response():
    try:
        data = request.get_json(force=True)
        user_message = data.get("message", "").strip()

        if not user_message:
            return jsonify({"response": "❌ لم يتم استقبال رسالة صالحة!"}), 400

        detected_lang = langdetect.detect(user_message)
        translated_message = GoogleTranslator(source='auto', target='ar').translate(user_message) if detected_lang != "ar" else user_message

        response, tag = search_intents(translated_message)

        if not response:
            response = search_local_questions(translated_message)

        if not response:
            if is_museum_related(translated_message):
                response = search_wikipedia(translated_message)
                if not response:
                    response = get_gemini_response(translated_message)
                if not response:
                    response = search_duckduckgo(translated_message)
            else:
                response = "❌ هذا السؤال خارج نطاق تخصصي، أنا هنا لمساعدتك فيما يخص المتحف المصري فقط."

            save_question(translated_message, response)

        return jsonify({"response": response})

    except Exception as e:
        return jsonify({"response": f"حدث خطأ أثناء المعالجة: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(debug=True)
