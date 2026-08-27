import ollama
import os

with open("secret_info.txt", "r", encoding="utf-8") as f:
    secret_data = f.read()

print("🤖 [記憶機能つき] 宇宙サウナAIが起動しました！")
print("💬 前の会話を覚えています。終了するには 'exit' と入力してください。\n")

# 【重要】Docker環境かMacローカル環境かを自動判定するプロ設計
is_docker = os.path.exists('/.dockerenv')
default_host = 'http://host.docker.internal:11434' if is_docker else 'http://localhost:11434'
ollama_host = os.environ.get('OLLAMA_HOST', default_host)
client = ollama.Client(host=ollama_host)

# 過去の会話をすべて記憶しておくための箱
chat_history = []

while True:
    user_question = input("🙋 あなた: ")
    
    if user_question.lower() == 'exit':
        print("👋 バイバイ！またね！")
        break
        
    if not user_question.strip():
        continue

    prompt = f"""以下の参考資料を必ず読んで、資料に書かれている内容を元に質問に答えてください。
資料に書かれていないことは、推測して答えないでください。
また、回答は必ず【日本語】で出力してください。

【参考資料】
{secret_data}

【質問】
{user_question}
"""

    # ユーザーの発言を履歴に追加
    chat_history.append({'role': 'user', 'content': prompt})

    print("🤔 AIがこれまでの会話を思い出して考えています...")

    try:
        # 会話履歴を丸ごとAIに渡す
        response = client.chat(model='llama3', messages=chat_history)
        ai_reply = response['message']['content']

        print(f"\n🤖 AI: {ai_reply}\n")

        # AIの返答も履歴に追加
        chat_history.append({'role': 'assistant', 'content': ai_reply})
        
    except Exception as e:
        print(f"\n❌ エラーが発生しました: {e}")
        print("Mac本体のOllamaアプリが起動しているか確認してください。\n")
        break
