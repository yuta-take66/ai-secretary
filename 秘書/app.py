import streamlit as st
from dotenv import load_dotenv
import os
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage, AIMessage

# .envファイルの読み込み
load_dotenv()

st.set_page_config(page_title="My AI Secretary", page_icon="🤖", layout="centered")

st.title("🤖 あなたの専属AI秘書")

# APIキーの確認
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    st.warning("⚠️ `.env` ファイルに `GEMINI_API_KEY` が設定されていません。ファイルを開いて設定し、画面をリロードしてください。")
    st.stop()

# チャット履歴の初期化
if "messages" not in st.session_state:
    st.session_state.messages = [
        AIMessage(content="こんにちは！ご主人様の秘書です。まずは私にどのようなタスクを任せたいか教えてください！")
    ]

# LLMの初期化
@st.cache_resource
def get_llm():
    return ChatGoogleGenerativeAI(
        model="gemini-2.0-flash", # 処理速度重視なら gemini-1.5-flash に変更可能
        temperature=0.7,
        google_api_key=api_key
    )

llm = get_llm()

# チャット履歴の表示
for msg in st.session_state.messages:
    role = "user" if isinstance(msg, HumanMessage) else "assistant"
    with st.chat_message(role):
        st.markdown(msg.content)

# ユーザー入力
if prompt := st.chat_input("秘書に指示を出す..."):
    # ユーザーのメッセージを追加
    st.session_state.messages.append(HumanMessage(content=prompt))
    with st.chat_message("user"):
        st.markdown(prompt)

    # 秘書の応答を取得
    with st.chat_message("assistant"):
        with st.spinner("考え中..."):
            try:
                # LLMに会話履歴を渡して応答を生成
                # （後ほどここに「ツール」を持たせたエージェント処理を追加します）
                response = llm.invoke(st.session_state.messages)
                st.markdown(response.content)
                st.session_state.messages.append(AIMessage(content=response.content))
            except Exception as e:
                st.error(f"エラーが発生しました: {e}")
