import requests
import os
from dotenv import load_dotenv

load_dotenv()

url = os.getenv("API_URL")
headers = {
    "Authorization": f"Bearer {os.getenv('API_KEY')}",
    "Content-Type": "application/json"
}

def test_prompt(system_msg, user_msg):
    payload = {
        "model": "deepseek-v3-2-251201",
        "messages": [
            {"role": "system", "content": system_msg},
            {"role": "user", "content": user_msg}
        ]
    }
    resp = requests.post(url, json=payload, headers=headers)
    return resp.json()["choices"][0]["message"]["content"]

# 实验 1：不同角色对比，使用时输入扮演角色
system_templates = {

}


question = "我被狗咬了怎么办？"
for role, sys_msg in system_templates.items():
    print(f"\n===== {role} =====")
    print(test_prompt(sys_msg, question))

# Few-shot：把示例直接放在 user 消息里
def test_few_shot():
    prompt = """
请把下面的句子转换成“表情符号 + 一句话总结”的格式。

示例：
输入：今天考试得了满分，很开心。
输出：😄 考试满分，心情大好！

输入：下班路上堵了两个小时。
输出：😤 堵车两小时，心累。

现在请转换下面的句子：
输入：周末和朋友吃了火锅，还看了电影。
"""
    return test_prompt("你是一个擅长用表情符号总结的助手", prompt)

print("\n===== Few-shot 测试 =====")
print(test_few_shot())

# 分步骤 + 限制条件
system = "你是一个严谨的分析助手，总是按要求一步步思考。"

user = """
请分析下面这段话的情感，并按要求输出。

文本：“等了半年终于升职了，但同时也意味着要承担更多压力，有点紧张。”

请严格按以下步骤：
第一步：用一句话总结这段话的主旨。
第二步：分别列出正面情绪和负面情绪（各不超过3个词）。
第三步：用1-10打分，1=非常消极，10=非常积极。

最终输出格式：
主旨：
正面情绪：
负面情绪：
情感分数：
"""
print("\n===== 分步骤 + 限制 =====")
print(test_prompt(system, user))

# 输出表格
user_table = """
列出三种主流大模型（GPT-4、Claude 3、Gemini），对比它们的：
- 开发商
- 最大上下文窗口
- 是否开源
用 Markdown 表格输出。
"""
print("\n===== 表格输出 =====")
print(test_prompt("你是一个 AI 技术分析师", user_table))

# 输出 JSON
user_json = """
请用 JSON 格式介绍 Python 语言，包含以下字段：
- name: 语言名称
- designed_by: 设计者
- first_appeared: 首次发布年份
- typing: 类型系统（static/dynamic）
- popular_frameworks: 热门框架列表（至少3个）
只输出 JSON，不要其他说明。
"""
print("\n===== JSON 输出 =====")
print(test_prompt("你是一个精确的 JSON 输出器，只输出合法 JSON", user_json))