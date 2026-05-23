import requests
import os
from dotenv import load_dotenv

load_dotenv()

# 直接从环境变量读取完整的 API URL
url = os.getenv("API_URL")   
headers = {
    "Authorization": f"Bearer {os.getenv('API_KEY')}",
    "Content-Type": "application/json"
}

user_input = input("请输入你的问题：")

payload = {
    "model": "deepseek-v3-2-251201",  # 火山引擎 DeepSeek-V3 的正确模型名
    "messages": [
        {"role": "user", "content": user_input}
    ]
}

resp = requests.post(url, json=payload, headers=headers)
data = resp.json()

if "choices" in data:
    content = data["choices"][0]["message"]["content"]
    print("🤖 模型回复：")
    print(content)
else:
    print("❌ 请求失败，错误信息：", data)