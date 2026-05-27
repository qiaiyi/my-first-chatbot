from pydantic import BaseModel, Field
from typing import List

# 定义简历模型
class Education(BaseModel):
    school: str
    degree: str
    year: int = Field(ge=1900, le=2030)  # 年份范围限制

class WorkExperience(BaseModel):
    company: str
    position: str
    duration: str

class Resume(BaseModel):
    name: str
    email: str
    phone: str
    education: List[Education]
    skills: List[str]
    work_experience: List[WorkExperience]

# 测试校验
data = {
    "name": "张三",
    "email": "zhang@example.com",
    "phone": "13800138000",
    "education": [
        {"school": "北京大学", "degree": "本科", "year": 2022}
    ],
    "skills": ["Python", "AI"],
    "work_experience": [
        {"company": "ABC科技", "position": "数据分析师", "duration": "2022-至今"}
    ]
}

resume = Resume(**data)  # 自动校验
print(resume.model_dump())  # 转为字典输出

# 故意传入错误数据
bad_data = data.copy()
bad_data["education"][0]["year"] = 2050
try:
    Resume(**bad_data)
except Exception as e:
    print(f"❌ 校验失败：{e}")