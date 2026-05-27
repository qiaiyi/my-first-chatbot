import requests
import json
import os
from dotenv import load_dotenv

load_dotenv()
url = os.getenv('API_URL')
headers = {
    "Authorization": f"Bearer {os.getenv('API_KEY')}",
    "Content-Type": "application/json"
}

# 定义工具（函数）
tools = [
    {
        "type": "function",
        "function": {
            "name": "calculator",
            "description": "执行基本的四则运算",
            "parameters": {
                "type": "object",
                "properties": {
                    "expression": {
                        "type": "string",
                        "description": "数学表达式，如 2+3*4"
                    }
                },
                "required": ["expression"]
            }
        }
    }
]

def call_model(messages):
    payload = {
        "model": "deepseek-v3-2-251201",
        "messages": messages,
        "tools": tools,
        "tool_choice": "auto"  # 模型自行决定是否调用工具
    }
    resp = requests.post(url, json=payload, headers=headers)
    return resp.json()

# 模拟对话
messages = [{"role": "user", "content": "请帮我计算 345 * 678"}]
response = call_model(messages)
msg = response["choices"][0]["message"]

if msg.get("tool_calls"):
    tool_call = msg["tool_calls"][0]
    func_name = tool_call["function"]["name"]
    args = json.loads(tool_call["function"]["arguments"])
    print(f"模型请求调用工具：{func_name}({args})")

    # 执行计算器
    if func_name == "calculator":
        result = eval(args["expression"])  # 注意：演示用，实际需安全处理
        print(f"计算结果：{result}")
        
        messages.append(msg)

        # 将工具执行结果返回给模型
        messages.append({
            "role": "tool",
            "tool_call_id": tool_call["id"],
            "content": str(result)
        })
        # 再次调用模型，生成最终回复
        final_resp = call_model(messages)
        final_msg = final_resp["choices"][0]["message"]["content"]
        print(f"模型最终回复：{final_msg}")
else:
    print(f"模型直接回复：{msg['content']}")