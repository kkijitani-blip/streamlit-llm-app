import streamlit as st
import os  # 環境変数（APIキー）を扱うためのライブラリ
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage

# 1. .envファイルからOpenAI APIキーを読み込む
load_dotenv()

# 2. LLMからの回答を返す関数を定義
def get_ai_response(user_input, expert_type):
    # .envから読み込んだAPIキーを明示的に取得
    api_key = os.getenv("OPENAI_API_KEY")
    
    # APIキーが読み込めていない場合のチェック
    if not api_key:
        return "エラー：APIキーが見つかりません。.envファイルを確認してください。"

    # LangChainを使ってLLM（GPT）を呼び出す準備
    # api_keyを直接渡すことで、Streamlitの内部エラーを回避します
    llm = ChatOpenAI(
        model="gpt-4o-mini", 
        openai_api_key=api_key
    ) 
    
    # ラジオボタンの選択値に応じてシステムメッセージを変える
    if expert_type == "プロの料理人":
        system_content = "あなたは世界的に有名なプロの料理人です。食材の活かし方や美味しいレシピを親切に教えてください。"
    else:
        system_content = "あなたは経験豊富なITコンサルタントです。最新技術や業務効率化について、専門的な視点でアドバイスしてください。"
        
    messages = [
        SystemMessage(content=system_content),
        HumanMessage(content=user_input)
    ]
    
    try:
        # LLMにプロンプトを渡し、回答を取得
        response = llm.invoke(messages)
        return response.content
    except Exception as e:
        return f"エラーが発生しました: {e}"

# --- Streamlit UIの設定 ---
st.title("AI専門家相談チャット")
st.write("このアプリでは、選択した専門家からアドバイスをもらうことができます。")

# 3. ラジオボタンで専門家を選択
expert_choice = st.radio("相談したい専門家を選んでください：", ["プロの料理人", "ITコンサルタント"])

# 4. 入力フォームを用意
user_text = st.text_input("相談内容を入力してください：")

# 実行ボタンが押された時の処理
if st.button("相談する"):
    if user_text:
        with st.spinner("AIが回答を考えています..."):
            # 関数を利用して回答を表示
            answer = get_ai_response(user_text, expert_choice)
            st.subheader(f"{expert_choice}からの回答")
            st.write(answer)
    else:
        st.warning("相談内容を入力してください。")