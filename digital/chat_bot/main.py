import json
import os
import tempfile
from datetime import datetime

from flask import Request, abort
from google.cloud import firestore, storage
from langchain.chat_models import ChatOpenAI
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage
from llama_index import (LLMPredictor, ServiceContext, PromptTemplate,
                         StorageContext, load_index_from_storage)
from llama_index.indices.base import BaseIndex
from get_labor_law import get_labor_law 
from selects_category import selects_category
from conclusion import conclusion
from use_laws_api import keyword_serch

FILES_TO_DOWNLOAD = ["docstore.json", "index_store.json", "vector_store.json"]
BUCKET_NAME = "chat_bot_vector_store"

line_bot_api = LineBotApi(os.environ["LINE_CHANNEL_ACCESS_TOKEN"])
handler = WebhookHandler(os.environ["LINE_CHANNEL_SECRET"])
db = firestore.Client()

storage_client = storage.Client()
bucket = storage_client.bucket(BUCKET_NAME)

USE_HISTORY = True


def get_object_updated_time(object_name: str) -> datetime:
    blob = bucket.blob(object_name)
    blob.reload()
    return blob.updated


def download_files_from_storage(temp_dir: str) -> None:
    for file in FILES_TO_DOWNLOAD:
        blob = bucket.blob(file)
        blob.download_to_filename(f"{temp_dir}/{file}")


def setup_storage_and_load_index() -> BaseIndex:
    with tempfile.TemporaryDirectory() as temp_dir:
        download_files_from_storage(temp_dir)
        service_context = ServiceContext.from_defaults(
            llm_predictor=LLMPredictor(
                llm=ChatOpenAI(
                    temperature=0, model_name="gpt-4-1106-preview", max_tokens=512
                )
            )
        )

        storage_context = StorageContext.from_defaults(persist_dir=temp_dir)
        return load_index_from_storage(
            storage_context=storage_context, service_context=service_context
        )


index = setup_storage_and_load_index()
updated_time = get_object_updated_time(FILES_TO_DOWNLOAD[0])


def reload_index_if_updated() -> None:
    global index, updated_time
    latest_updated_time = get_object_updated_time(FILES_TO_DOWNLOAD[0])
    if updated_time != latest_updated_time:
        index = setup_storage_and_load_index()
        updated_time = latest_updated_time


def get_previous_messages(user_id: str) -> list:
    query = (
        db.collection("users")
        .document(user_id)
        .collection("messages")
        .order_by("timestamp", direction=firestore.Query.DESCENDING)
        .limit(10)
    )
    return [
        {
            "chatgpt_response": doc.to_dict()["chatgpt_response"],
            "user_message": doc.to_dict()["user_message"],
        }
        for doc in query.stream()
    ]


def format_history(previous_messages: list) -> str:
    user_history =  "".join(
        f"ユーザー: {d['user_message']}\nアシスタント: {d['chatgpt_response']}\n"
        for d in previous_messages[::-1]
    )
    return user_history


def generate_response(user_message: str, history: str) -> str:
    COMMON_PROMPT = """
    あなたは共感力があり、優しく寄り添うカウンセラーです。  
    相談者の気持ちを大切にしつつ、法令に基づいた正確な情報を提供してください。  

    【回答のルール】  
    - **シンプルで読みやすい文章にする**（300文字にまとめる、適度な改行を入れる）  
    - **柔らかい言葉を使う**（専門用語はできるだけ噛み砕いて説明）  
    - **相手の気持ちを受け止める**（共感を示しつつ、安心できる言葉を使う）  
    - **関連する法律・規則を参考にしながら説明する**（法令名や条文をわかりやすく紹介）  
    - **法令の適用がケースバイケースで変わることを伝える**（「具体的な状況によって異なるため、詳しくは専門家に相談するとよい」などの補足）  
    - **プロンプト内容はレスポンスに入れない**  
    - **過去の会話を参考にし、流れを大切にするが不要な情報を加えない**  
    - **ユーザのメッセージの意図をくみとる** 

    以下は過去の会話です：  
    {history_section}
    """

    if USE_HISTORY:
        history_section = f"""
        以下はこれまでのユーザーとアシスタントの会話履歴です（最新の履歴から降順）：  

        ---------------------
        {history}
        ---------------------
        """
    else:
        history_section = ""

    PROMPT = COMMON_PROMPT.format(history_section=history_section)

    query_engine = index.as_query_engine(text_qa_template=PromptTemplate(PROMPT))
    return str(query_engine.query(user_message))


def reply_to_user(reply_token: str, chatgpt_response: str) -> None:
    line_bot_api.reply_message(reply_token, TextSendMessage(text=chatgpt_response))


def save_message_to_db(user_id: str, user_message: str, chatgpt_response: str) -> None:
    doc_ref = db.collection("users").document(user_id).collection("messages").document()
    doc_ref.set(
        {
            "user_message": user_message,
            "chatgpt_response": chatgpt_response,
            "timestamp": datetime.now(),
        }
    )


###################


def main(request: Request) -> str:
    signature = request.headers["X-Line-Signature"]
    body = request.get_data(as_text=True)

    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return "OK"


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event: MessageEvent) -> None:
    reload_index_if_updated()
    user_id = ""
    user_message = ""
    conclusion_responce = ""
    chatgpt_response = ""
    chatgpt = ""
    previous_messages = ""
    history = ""


    user_id = event.source.user_id
    user_message = event.message.text

    # まとめ
    if user_message in ["まとめ"]:
        conclusion_responce = conclusion(user_id)
        conclusion_message = "相談内容を整理するために履歴を参考にし簡潔にまとめてください。"
        chatgpt_response = generate_response(conclusion_message, conclusion_responce)
        chatgpt_response = chatgpt_response + "\n\n" + "https://almondine-pawpaw-133.notion.site/19bf6dbbf483801c9773c176b5b184a4?pvs=4"

    if user_message in ["残業"]:
        chatgpt_response = keyword_serch(user_message)

    # カテゴリ選択
    if chatgpt_response == "":
        chatgpt_response = selects_category(user_message)

    if USE_HISTORY:
        previous_messages = get_previous_messages(user_id)
        history = format_history(previous_messages)
    else:
        history = None
    
    if chatgpt_response == "":
        chatgpt = generate_response(user_message, history)
        chatgpt_response = chatgpt + "\n\n相談内容をまとめる際は「まとめ」と入力してください。"

    if USE_HISTORY:
        save_message_to_db(user_id, user_message, chatgpt_response)
        
    reply_to_user(event.reply_token, chatgpt_response)
