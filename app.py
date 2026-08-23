import os
import ollama

# 1. 秘密のメモファイルを読み込む
with open("secret_info.txt", "r", encoding="utf-8") as f:
    secret_data = f.read()

# 2. ユーザーからの質問
user_question = "私の秘密の趣味と、それがどんなものか教えて？"

# 3. メモの内容をプロンプトに組み込む
prompt = f"""以下の参考資料を必ず読んで、資料に書かれている内容を元に質問に答えてください。
資料に書かれていないことは、推測して答えないでください。

【参考資料】
{secret_data}

【質問】
{user_question}
"""

print("🤔 AIが秘密のメモを読み込んで考えています...")

# 環境変数 OLLAMA_HOST から接続先を取得し、設定されていない場合はデフォルトの localhost を使用します
ollama_host = os.environ.get('OLLAMA_HOST', 'http://localhost:11434')
client = ollama.Client(host=ollama_host)
response = client.chat(model='llama3', messages=[
    {'role': 'user', 'content': prompt}
])

print("\n🤖 【AIからの回答】:")
print(response['message']['content'])
