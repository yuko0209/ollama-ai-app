import ollama
import os

with open("secret_info.txt", "r", encoding="utf-8") as f:
    secret_data = f.read()

print("🤖 宇宙サウナAIチャットボットが起動しました！")
print("💬 質問をどうぞ！（終了するには 'exit' と入力してください）\n")

is_docker = os.path.exists('/.dockerenv')
default_host = 'http://host.docker.internal:11434' if is_docker else 'http://localhost:11434'
ollama_host = os.environ.get('OLLAMA_HOST', default_host)
client = ollama.Client(host=ollama_host)

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

    print("🤔 AIが考えています...")

    response = client.chat(model='llama3', messages=[
        {'role': 'user', 'content': prompt}
    ])

    print(f"\n🤖 AI: {response['message']['content']}\n")
