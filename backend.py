from flask import Flask, request, jsonify
from flask_cors import CORS
from openai import AsyncOpenAI
import asyncio
from logic import search_law, extract_law_titles, extract_text, search_law_sentence, connect_openai

app = Flask(__name__)
CORS(app)  # CORSを許可（フロントエンドからアクセスできるようにする）

@app.route('/api/law-search', methods=['POST'])
def law_search():
    data = request.json
    keyword = data.get("keyword")
    counseling = data.get("counseling")

    if not keyword or not counseling:
        return jsonify({"error": "キーワードと相談内容を入力してください。"}), 400

    # キーワード検索
    result = search_law(keyword)
    law_title_list = extract_law_titles(result)
    print(law_title_list)
    law_id_list = extract_text(result)
    print(law_id_list)

    # OpenAIに質問
    text = f"労働者の立場になって {keyword} に関する {counseling} の相談に一致する法令は以下の中だとどれか簡潔に答えて: {', '.join(law_title_list)}"
    
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    ai_response = loop.run_until_complete(connect_openai(text))
    #ai_response="労働基準法"
    print(ai_response)

    # 法令本文取得
    law_sentence = ""
    for i, law_title in enumerate(law_title_list):
        if law_title in ai_response:
            law_sentence += search_law_sentence(law_id_list[i])

    # 法令本文の要約
    summary_text = f"労働者の立場になって {keyword} に関する {counseling} の相談に一致するよう以下の法令を法令知識がない人でもわかるようにかみ砕いて解説して: {law_sentence}"
    final_response = loop.run_until_complete(connect_openai(summary_text))

    return jsonify({"result": final_response})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
