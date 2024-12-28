from app.core.config import settings
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI

def llm_extract(records):
    # 获取API信息
    api_key = settings.OPENAI_API_KEY
    base_url = settings.OPENAI_API_BASE

    # 定义Prompt
    template = """
    请从<begin>、<end>间的会议记录中提取出所有任务项，要求如下:
    1. 用JSON列表的格式输出任务项
    2. 语言与会议记录相同
    3. 任务项包括任务描述、负责人、截止日期
    4. 任务项中的某部分在会议记录中未提及用null填充
    <begin>
    {content}
    <end>
    """
    content = records
    prompt = PromptTemplate.from_template(template).format(content=content)

    # 创建OpenAI实例
    llm = ChatOpenAI(api_key=api_key, base_url=base_url)

    # 执行模型调用
    response = llm.invoke(prompt)
    return response.content