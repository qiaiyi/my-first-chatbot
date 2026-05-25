import streamlit as st
import requests
import json
import os
from dotenv import load_dotenv

load_dotenv()

def extract_resume(text):
    url = os.getenv("API_URL")
    headers = {
        "Authorization": f"Bearer {os.getenv('API_KEY')}",
        "Content-Type": "application/json"
    }
    prompt = f"""
从以下简历文本中提取关键信息，用 JSON 格式返回。

简历：
{text}

JSON 格式要求：
{{
    "name": "姓名",
    "email": "邮箱",
    "phone": "电话",
    "education": [{{"school": "学校", "degree": "学历", "year": "毕业年份"}}],
    "skills": ["技能1", "技能2"],
    "work_experience": [{{"company": "公司", "position": "职位", "duration": "时长"}}]
}}
只输出 JSON，不要任何额外说明。
"""
    payload = {
        "model": "deepseek-v3-2-251201",
        "messages": [{"role": "user", "content": prompt}]
    }
    resp = requests.post(url, json=payload, headers=headers)
    return resp.json()["choices"][0]["message"]["content"]

st.title("📄 简历信息提取器")
sample = """
张三 | zhang@email.com | 13800138000
教育：北京大学 计算机科学 本科 2022
技能：Python, 机器学习, SQL
工作经历：ABC科技 数据分析师 2022.07-至今
"""
text = st.text_area("请粘贴简历文本", sample, height=300)

if st.button("提取信息"):
    if text.strip():
        with st.spinner("AI 正在提取..."):
            raw = extract_resume(text)
        try:
            data = json.loads(raw)
            st.success("提取成功")
            st.json(data)
        except json.JSONDecodeError:
            st.error("JSON 解析失败，原始输出：")
            st.code(raw)
    else:
        st.warning("请先输入简历文本")