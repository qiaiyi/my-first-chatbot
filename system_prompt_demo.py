import requests
import os
from dotenv import load_dotenv

load_dotenv()

# 直接从环境变量读取完整的 API URL（例如：https://ark.cn-beijing.volces.com/api/v3/chat/completions）
url = os.getenv("API_URL")
headers = {
    "Authorization": f"Bearer {os.getenv('API_KEY')}",
    "Content-Type": "application/json"
}

# 系统提示词——定义模型人设
system_prompt = "你是一个说话温柔的知心大姐姐，喜欢用温柔的方式安抚他人，每次安抚完情绪都会给出有用的建议。"

messages = [{"role": "system", "content": system_prompt}]

print("🤖 温柔姐姐（输入 quit 退出）")
while True:
    user_input = input("你：")
    if user_input.lower() == "quit":
        break
    messages.append({"role": "user", "content": user_input})
    
    payload = {
        "model": "deepseek-v3-2-251201",   # 火山引擎 DeepSeek-V3 的正确模型名
        "messages": messages
    }
    
    try:
        resp = requests.post(url, json=payload, headers=headers)
        data = resp.json()
        
        # 检查响应是否包含 choices 字段
        if "choices" in data:
            reply = data["choices"][0]["message"]["content"]
            messages.append({"role": "assistant", "content": reply})
            print(f"🤖：{reply}")
        else:
            print(f"❌ API 返回错误：{data}")
            break
    except Exception as e:
        print(f"❌ 请求异常：{e}")
        break