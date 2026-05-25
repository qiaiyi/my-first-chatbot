import streamlit as st
import requests
import os
from dotenv import load_dotenv

load_dotenv()

def summarize(text, style="标准"):
    url = os.getenv("API_URL")
    headers = {
        "Authorization": f"Bearer {os.getenv('API_KEY')}",
        "Content-Type": "application/json"
    }
    prompt = f"""
请总结以下文章，要求：
- 用 {style} 风格
- 包含：一句话概括、三个要点、一个关键引用
- 总字数不超过 200 字

文章：
{text}
"""
    payload = {
        "model": "deepseek-v3-2-251201",
        "messages": [{"role": "user", "content": prompt}]
    }
    resp = requests.post(url, json=payload, headers=headers)
    return resp.json()["choices"][0]["message"]["content"]

st.title("📝 文章总结器")
style = st.selectbox("总结风格", ["标准", "幽默", "学术", "小学生能看懂"])
text = st.text_area("请粘贴需要总结的文章", height=300)

if st.button("生成总结"):
    if text.strip():
        with st.spinner("AI 正在总结..."):
            result = summarize(text, style)
        st.success("总结完成")
        st.markdown(result)
    else:
        st.warning("请先输入文章内容")