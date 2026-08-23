import ollama

# Dockerの中からMac本体のOllamaを安全に呼び出す設定
client = ollama.Client(host='http://host.docker.internal:11434')

response = client.chat(model='llama3', messages=[
    {'role': 'user', 'content': 'Docker環境からこんにちは！一言挨拶をください。'}
])

print(response['message']['content'])
