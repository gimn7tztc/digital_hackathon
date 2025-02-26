# import asyncio
# import os
# import requests
# import json
# from dotenv import load_dotenv
# from openai import AsyncOpenAI
from docx import Document 

# # Key.env ファイルを読み込む
# load_dotenv("Key.env")

# 環境変数から API キーを取得
#OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_API_KEY = ""
if not OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY が設定されていません。Key.env を確認してください。")

# 非同期クライアントの作成
client = AsyncOpenAI(api_key=OPENAI_API_KEY)

# キーワード検索
def search_law(keyword):
    code = "020"
    base_url = "https://laws.e-gov.go.jp/api/2/keyword"
    params = {
        "keyword": keyword,
        "category_cd": code
    }
    response = requests.get(base_url, params=params)
    response.raise_for_status()

    data = response.json()

    return data

# 法令本文取得
def search_law_sentence(law_id):

    file_type = "docx"  
    url = f"https://elaws.e-gov.go.jp/api/2/law_file/{file_type}/{law_id}"
    filename = "law_document.docx"

    # ファイルをダウンロード
    response = requests.get(url)

    if response.status_code == 200:
        with open(filename, "wb") as file:
            file.write(response.content)
        print(f"ファイルが {filename} としてダウンロードされました。")
    else:
        print(f"ダウンロード失敗: HTTP {response.status_code}")
        exit()

    # Wordファイルのテキストを抽出
    def extract_text_from_docx(file_path):
        doc = Document(file_path)
        text = "\n".join([para.text for para in doc.paragraphs])
        return text

    # テキストを取得
    text = extract_text_from_docx(filename)
    limit_text = text[:1500]

    return limit_text


# キーワード検索結果から法令タイトル取得
def extract_law_titles(result):
    law_titles = []
    if isinstance(result, dict):
        if "law_title" in result:
            law_titles.append(str(result["law_title"]))
        for value in result.values():
            law_titles.extend(extract_law_titles(value))
    elif isinstance(result, list):
        for item in result:
            law_titles.extend(extract_law_titles(item))
    return law_titles

# キーワード検索結果から法令ID取得
def extract_text(result):

    law_id = [item["law_info"]["law_id"] for item in result["items"]]
    
    return law_id

# async def connect_openai(text):

#     # OpenAI API のリアルタイム接続を確立（モデル名は例です）
#     async with client.beta.realtime.connect(model="gpt-4o-mini-realtime-preview-2024-12-17") as connection:
#         # セッション更新：テキストモダリティのみを有効化
#         await connection.session.update(session={"modalities": ["text"]})
#         # ユーザーからのメッセージを会話に追加
#         await connection.conversation.item.create(
#             item={
#                 "type": "message",
#                 "role": "user",
#                 "content": [{"type": "input_text", "text": text}]
#             }
#         )

#         # 回答生成の指示
#         await connection.response.create()

#         open_ai = []
#         # イベントループ：テキスト生成（デルタ）を逐次出力
#         async for event in connection:
#             if event.type == "response.text.delta":
#                 # 生成されたテキストを連結して表示
#                 #print(event.delta, end="", flush=True)
#                 open_ai.append(event.delta)
                
#             if event.type == "response.done":
#                 print("\n応答が完了しました。")
#                 break
        
#         output = "".join(open_ai)
#         #print(output) 

#     return output


# async def main():

#     keyword ="賃金"
#     counseling = "残業代未払い"
#     # キーワード検索
#     result = search_law(keyword)

#     # 法令タイトル取得
#     law_title_list = extract_law_titles(result)
#     law_title_list_str = "," .join(law_title_list)
#     print(law_title_list_str)
#     text ="労働者の立場になって"+ keyword+ "に関する" + counseling + "の相談に一致する法令は以下の中だとどれか簡潔に答えて"+ law_title_list_str

#     # OpenAIに質問を投げかける
#     output = await connect_openai(text)
#     #output = "労働時間に関する相談に一致する法令は「労働基準法」です。"
#     print(output)

#     # 法令ID取得
#     law_id_list = extract_text(result)
#     law_id_list_str = ",".join(law_id_list)
#     print(law_id_list_str)

#     # OpenAIからの返答から法令本文を取得する
#     i = 0
#     law_sentence=""
#     for law_title in law_title_list:
#         if law_title in output:
#             mach_law_id = law_id_list[i]
#             # 法令本文取得
#             law_sentence += search_law_sentence(mach_law_id)
#         i =+i  

#     print(law_sentence)

#     # 相談内容にそった法令本文の要約
#     sentence = "労働者の立場になって" + keyword + "に関する" + counseling + "の相談に一致するよう以下の法令を中学生でもわかるように解説して" + law_sentence

#     # OpenAIに質問を投げかける
#     output = await connect_openai(sentence)
#     print(output)
