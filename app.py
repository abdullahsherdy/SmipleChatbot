from flask import Flask, render_template, request, jsonify
from local_match import search_local_response, save_question, last_user_tag, get_detailed_response
from external_search import external_fallback, is_museum_related
from deep_translator import GoogleTranslator
import langdetect

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

        # Detect and translate if needed
        lang = langdetect.detect(user_message)
        message_ar = GoogleTranslator(source='auto', target='ar').translate(user_message) if lang != "ar" else user_message

        # Check if user wants more detail
        if get_detailed_response(message_ar):
            return jsonify({"response": get_detailed_response(message_ar)})

        # Local check (intents or previous questions)
        response, tag = search_local_response(message_ar)
        if response:
            return jsonify({"response": GoogleTranslator(source="ar", target=lang).translate(response) if lang != "ar" else response})

        # External fallback
        if is_museum_related(message_ar):
            response = external_fallback(message_ar)
            save_question(message_ar, response)
        else:
            response = "❌ هذا السؤال خارج نطاق تخصصي، أنا هنا لمساعدتك فيما يخص المتحف المصري فقط."

        final_response = GoogleTranslator(source="ar", target=lang).translate(response) if lang != "ar" else response
        return jsonify({"response": final_response})

    except Exception as e:
        print(f"❌ خطأ: {e}")
        return jsonify({"response": "❌ حدث خطأ في النظام، حاول لاحقًا."}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)
