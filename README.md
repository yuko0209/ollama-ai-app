# ollama-ai-app
Ollamaを使った自作AIアプリケーションの開発プロジェクト


---

# 🛸 ローカルRAG（宇宙サウナAI）開発ドキュメント

## 概要
* **目的**：外部にデータを送らず、Mac内だけで独自データを読み込ませて回答させるシステム（RAG）の構築
* **環境**：Docker（Python 3.11-slim） ＋ Mac本体（Ollama / Llama 3）
* **GitHub管理**：イシュー #5 ➡️ ブランチ feature/setup-rag

---

## 📂 フォルダ構成（最終形）
```text
ollama-ai-app/
├── Dockerfile        # 隔離部屋（コンテナ）の設計図
├── app.py            # RAGを実行するメインプログラム
└── secret_info.txt   # AIに読み込ませる「秘密のメモ」
```

---

## 🛠️ 各ファイルのコード

### 1. `secret_info.txt`（独自データ）
```text
私の秘密の趣味は「宇宙サウナ」です。
宇宙サウナとは、無重力空間で星空を眺めながら整う、2026年に大流行中の最新アクティビティです。
```

### 2. `Dockerfile`（環境の自動化）
```dockerfile
FROM python:3.11-slim
WORKDIR /app
# RAGに必要なLangChain関連ライブラリを自動インストール
RUN pip install --no-cache-dir ollama langchain-community langchain-core
COPY . .
CMD ["python", "app.py"]
```

### 3. `app.py`（RAGメインロジック）
```python
import ollama
import os

# 1. 独自の秘密メモを読み込む
with open("secret_info.txt", "r", encoding="utf-8") as f:
    secret_data = f.read()

# 2. ユーザーからの質問
user_question = "私の秘密の趣味と、それがどんなものか教えて？"

# 3. データをプロンプトに組み込む（RAGの核）
prompt = f"""以下の参考資料を必ず読んで、資料に書かれている内容を元に質問に答えてください。
資料に書かれていないことは、推測して答えないでください。

【参考資料】
{{secret_data}}

【質問】
{{user_question}}
"""

print("🤔 AIが秘密のメモを読み込んで考えています...")

# 4. 環境変数から接続先を取得（MacのVMネットワーク壁を越えるプロ設計）
ollama_host = os.environ.get('OLLAMA_HOST', 'http://localhost:11434')
client = ollama.Client(host=ollama_host)

response = client.chat(model='llama3', messages=[
    {{'role': 'user', 'content': prompt}}
])

print("\n🤖 【AIからの回答】:")
print(response['message']['content'])
```

---

## 🚀 再現・実行するための「魔法のコマンド」

### ステップ1：部屋の組み立て（ビルド）
```bash
docker build -t ollama-python-app .
```

### ステップ2：AIの実行（ラン）
```bash
docker run --rm -e OLLAMA_HOST=http://docker.internal ollama-python-app
```

---

## 🎓 今回学んだエンジニアの重要知識
* **RAGの基本**：AI自体を追加学習させなくても、プログラム側で「資料」をプロンプトに挟み込んで渡せば、独自の知識を喋らせることができる。
* **MacのDockerの壁**：Mac의 Dockerは「見えない仮想マシン」の中で動くため、Mac本体のアプリ（Ollama）と通信させるには host.docker.internal という住所指定が必要になる。
* **環境変数の活用**：コードに直接URLを書き込まず、-e OLLAMA_HOST=... のように外から切り替えられるようにするのが、プロの保守性の高いコード設計。
