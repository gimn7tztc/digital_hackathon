from langchain.chat_models import ChatOpenAI
from logic import search_law, extract_law_titles, extract_text, search_law_sentence

def keyword_serch(keyword):
    # キーワード検索
    result = search_law(keyword)
    law_title_list = extract_law_titles(result)
    law_id_list = extract_text(result)

    # OpenAIに質問
    text = f"労働者の立場になって {keyword} に関する相談に一致する法令は以下の中だとどれか簡潔に答えて: {', '.join(law_title_list)}"
    
    gpt_responce = generate_response(text)

    # 法令本文取得
    law_sentence = ""
    for i, law_title in enumerate(law_title_list):
        if law_title in gpt_responce:
            law_sentence += search_law_sentence(law_id_list[i])

    # 法令本文の要約
    summary_text = f"労働者の立場になって {keyword} に関する相談に一致するよう以下の法令を法令知識がない人でもわかるようにかみ砕いて解説して: {law_sentence}"
    
    return_keyword = generate_response(summary_text)

    return return_keyword



def generate_response(text: str) -> str:
    """ChatGPT へ直接リクエストを送信し、応答を取得"""
    chatgpt = ChatOpenAI(
        model_name="gpt-3.5-turbo",
        temperature=0.7,
        max_tokens=512
    )

    response = chatgpt.predict(text)
    return response

