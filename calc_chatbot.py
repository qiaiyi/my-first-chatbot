import streamlit as st
import requests
import json
import os
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()
url = os.getenv("API_URL")
headers = {
    "Authorization": f"Bearer {os.getenv('API_KEY')}",
    "Content-Type": "application/json"
}

# 定义工具：计算器
tools = [
    {
        "type": "function",
        "function": {
            "name": "calculator",
            "description": "执行基本的四则运算，例如 2+3*4",
            "parameters": {
                "type": "object",
                "properties": {
                    "expression": {
                        "type": "string",
                        "description": "数学表达式，如 '345 * 678'"
                    }
                },
                "required": ["expression"]
            }
        }
    }
]

def process_chat(messages):
    """
    处理对话，支持工具调用。
    - messages: 当前的对话历史（会被原地修改，以保留完整上下文）
    - 返回：模型最终回复的文本内容
    """
    # 第一次调用模型，可能触发工具调用
    payload = {
        "model": "deepseek-v3-2-251201",
        "messages": messages,
        "tools": tools,
        "tool_choice": "auto"
    }
    resp = requests.post(url, json=payload, headers=headers)
    msg = resp.json()["choices"][0]["message"]

    # 如果模型要求调用工具
    if msg.get("tool_calls"):
        # 1. 先将包含 tool_calls 的 assistant 消息加入历史
        messages.append(msg)

        # 2. 执行工具并将结果加入历史
        for tool_call in msg["tool_calls"]:
            func_name = tool_call["function"]["name"]
            args = json.loads(tool_call["function"]["arguments"])

            if func_name == "calculator":
                # ⚠️ eval 仅用于演示，生产环境请替换为安全的表达式求值库
                result = eval(args["expression"])
                messages.append({
                    "role": "tool",
                    "tool_call_id": tool_call["id"],
                    "content": str(result)
                })

        # 3. 再次调用模型（无需 tools，因为已经完成工具执行）
        final_payload = {
            "model": "deepseek-v3-2-251201",
            "messages": messages
        }
        final_resp = requests.post(url, json=final_payload, headers=headers)
        final_msg = final_resp.json()["choices"][0]["message"]
        final_content = final_msg["content"]

        # 4. 将最终的 assistant 回复加入历史
        messages.append({"role": "assistant", "content": final_content})
        return final_content

    else:
        # 没有工具调用，直接使用第一次回复
        content = msg["content"]
        messages.append({"role": "assistant", "content": content})
        return content

# ==================== Streamlit 界面 ====================
st.set_page_config(page_title="🧮 计算器聊天机器人", page_icon="🤖")
st.title("🧮 能算数的聊天助手")
st.caption("我是 DeepSeek，支持四则运算。试试问我“计算 345 * 678”吧！")

# 初始化对话历史
if "messages" not in st.session_state:
    st.session_state.messages = []

# 显示历史消息（只显示 user 和 assistant 角色）
for msg in st.session_state.messages:
    if msg["role"] in ("user", "assistant"):
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

# 接收用户输入
if prompt := st.chat_input("请输入你的问题..."):
    # 显示用户消息
    with st.chat_message("user"):
        st.markdown(prompt)

    # 将用户消息加入历史
    st.session_state.messages.append({"role": "user", "content": prompt})

    # 调用核心处理函数（内部会自动追加 assistant/tool 消息到历史）
    with st.spinner("思考中..."):
        try:
            reply = process_chat(st.session_state.messages)
        except Exception as e:
            reply = f"⚠️ 出错了：{e}"

    # 显示助手的最终回复
    with st.chat_message("assistant"):
        st.markdown(reply)