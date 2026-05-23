import streamlit as st
import requests
import os
from dotenv import load_dotenv
import json
from datetime import datetime

# 保存对话
def save_history(messages, filename="chat_history.json"):
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(messages, f, ensure_ascii=False, indent=2)

# 加载对话
def load_history(filename="chat_history.json"):
    try:
        with open(filename, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return None

load_dotenv()

st.set_page_config(page_title="🤖 AI 聊天助手")
st.title("🤖 我的第一个 AI 聊天机器人")

# ==================== 新增：侧边栏控件 ====================
with st.sidebar:
    st.header("⚙️ 对话设置")
    # 温度参数滑块（范围 0.0 ~ 1.5，默认 0.7）
    temperature = st.slider(
        "温度参数 (Temperature)",
        min_value=0.0,
        max_value=1.5,
        value=0.7,
        step=0.05,
        help="较低的值使输出更确定，较高的值使输出更多样"
    )
    # 清空对话按钮
    if st.button("🗑️ 清空对话", use_container_width=True):
        # 重置对话历史，仅保留系统提示词
        st.session_state.messages = [
            {"role": "system", "content": "你是一个友好、乐于助人的 AI 助手。"}
        ]
        st.rerun()  # 刷新页面，清空聊天显示

if st.sidebar.button("💾 保存对话"):
    save_history(st.session_state.messages)
    st.sidebar.success("对话已保存！")

if st.sidebar.button("📂 加载对话"):
    loaded = load_history()
    if loaded:
        st.session_state.messages = loaded
        st.sidebar.success("对话已加载！")
        st.rerun()

# 初始化对话历史（若未初始化）
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": "你是一个友好、乐于助人的 AI 助手。"}
    ]

# 显示历史消息（跳过 system 提示词）
for msg in st.session_state.messages:
    if msg["role"] != "system":
        with st.chat_message(msg["role"]):
            st.write(msg["content"])

# 用户输入
user_input = st.chat_input("在这里输入你的问题...")
if user_input:
    # 添加并显示用户消息
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.write(user_input)

    # 调用 API
    url = os.getenv("API_URL")  
    headers = {
        "Authorization": f"Bearer {os.getenv('API_KEY')}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "deepseek-v3-2-251201",   # 保持您原有的模型名
        "messages": st.session_state.messages,
        "temperature": temperature,        # 新增：动态传入温度参数
    }

    resp = requests.post(url, json=payload, headers=headers)
    data = resp.json()
    reply = data["choices"][0]["message"]["content"]

    # 添加并显示助手回复
    st.session_state.messages.append({"role": "assistant", "content": reply})
    with st.chat_message("assistant"):
        st.write(reply)