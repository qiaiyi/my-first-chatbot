# 🤖 我的第一个 AI 聊天机器人

## 功能
- 多轮对话
- 自定义系统人设
- 温度参数调节
- 对话保存与加载
- 友好的 Web 界面

## 技术栈
- Python + Streamlit
- DeepSeek API（OpenAI 兼容格式）
- python-dotenv 管理密钥

## 运行方式
1. pip install -r requirements.txt
2. 创建 .env 文件，填写 API_KEY 和 BASE_URL
3. streamlit run chat_app.py