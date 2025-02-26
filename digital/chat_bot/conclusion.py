from google.cloud import firestore
from llama_index.indices.base import BaseIndex

db = firestore.Client()


def conclusion(user_id):
    previous_messages = get_previous_messages(user_id)
    conclusion_responce = format_history(previous_messages)
    return conclusion_responce

def get_previous_messages(user_id: str) -> list:
    query = (
        db.collection("users")
        .document(user_id)
        .collection("messages")
        .order_by("timestamp", direction=firestore.Query.ASCENDING)
    )
    return [
        {
            "chatgpt_response": doc.to_dict().get("chatgpt_response", "（不明な応答）"),
            "user_message": doc.to_dict().get("user_message", "（不明なメッセージ）"),
        }
        for doc in query.stream()
    ]

def format_history(previous_messages: list) -> str:
    search_keywords = ["SODAに相談する", "相談する", "相談", "SODA"]

    index = next(
        (i for i, d in enumerate(previous_messages[::-1])
        if any(keyword == d.get("user_message", "") for keyword in search_keywords)),
        None
    )

    if index is not None:
        relevant_messages = previous_messages[-(index+1):]
        user_history = "".join(
            f"ユーザー: {d.get('user_message', '（不明なメッセージ）')}\n\n\n"
            f"アシスタント: {d.get('chatgpt_response', '（不明な応答）')}\n\n\n"
            for d in relevant_messages
        )
    else:
        user_history = ""

    return user_history
