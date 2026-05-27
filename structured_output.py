import requests
import json
import os
from dotenv import load_dotenv
from pydantic import BaseModel, ValidationError
from typing import List

load_dotenv()
url = os.getenv('API_URL')
headers = {
    "Authorization": f"Bearer {os.getenv('API_KEY')}",
    "Content-Type": "application/json"
}

class Skill(BaseModel):
    name: str
    level: str  # 初/中/高级

class PersonInfo(BaseModel):
    name: str
    age: int
    skills: List[Skill]

def extract_person_info(text):
    prompt = f"""
从以下文本中提取姓名、年龄、技能及水平，用 JSON 格式返回。

文本：{text}

JSON 格式要求（严格按此结构）：
{{
    "name": "姓名",
    "age": 年龄(整数),
    "skills": [
        {{"name": "技能名", "level": "初/中/高级"}}
    ]
}}

只输出 JSON，不要其他内容。
"""
    messages = [{"role": "user", "content": prompt}]
    payload = {"model": "deepseek-v3-2-251201", "messages": messages}

    for attempt in range(3):  # 最多重试3次
        resp = requests.post(url, json=payload, headers=headers)
        raw = resp.json()["choices"][0]["message"]["content"]
        try:
            data = json.loads(raw)
            person = PersonInfo(**data)  # Pydantic 校验
            return person
        except (json.JSONDecodeError, ValidationError) as e:
            print(f"第{attempt+1}次尝试失败：{e}")
            # 把错误信息反馈给模型
            messages.append({"role": "assistant", "content": raw})
            messages.append({"role": "user", "content": f"输出不符合要求，错误：{e}。请严格按照给定的 JSON 格式重新输出。"})
    return None

# 测试
text = "小明今年25岁，精通 Python（高级），熟悉机器学习（中级）。"
result = extract_person_info(text)
if result:
    print(result.model_dump())