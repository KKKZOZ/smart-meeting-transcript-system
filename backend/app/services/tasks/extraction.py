import json
import re
from app.core.config import settings
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI


def extract_and_check_task_json(response: str) -> str:
    """
    从LLM的响应中提取待办事项的JSON，并检查是否合法，失败时返回None
    合法则增加searchExecutor: ''用于对应前端的功能
    """
    # 使用正则表达式提取JSON列表
    json_pattern = r"\[.*?\]"  # 匹配JSON列表的正则表达式
    match = re.search(json_pattern, response, re.DOTALL)

    if not match:
        return None

    # 提取到的JSON列表部分
    json_str = match.group(0)

    try:
        # 解析JSON字符串
        json_list = json.loads(json_str)

        # 检查每个对象是否只包含 "content", "executor", "dueDate" 这三个键
        for obj in json_list:
            if not isinstance(obj, dict):
                return None

            # 获取当前对象的所有键
            keys = set(obj.keys())
            expected_keys = {"content", "executor", "dueDate"}

            # 检查是否完全匹配
            if keys != expected_keys:
                return None

            # 增加searchExecutor: ''用于对应前端的功能
            obj["searchExecutor"] = ""

        return json_list

    except json.JSONDecodeError:
        return None


def llm_extract(records: str, meeting_time: str) -> str:
    """
    从会议记录中提取任务项
    """
    # 获取API信息
    api_key = settings.OPENAI_API_KEY
    base_url = settings.OPENAI_API_BASE

    # 定义Prompt
    template = """
    请从<begin>、<end>间的会议记录中提取出所有任务项，要求如下：
    1.  用JSON列表的格式输出任务项
    2.  JSON列表的每一项的形式为{json_type}
    3.  JSON中键对应的值使用的语言与会议记录相同
    4.  任务项中的某部分在会议记录中未提及用空字符串""填充
    5.  会议举行的时间为{meeting_time}
    <begin>
    {content}
    <end>
    """
    json_type = """
        {
            "content": "任务描述",
            "executor": "任务负责人",
            "dueDate": "yyyy-MM-dd HH:MM"
        }
    """
    prompt = PromptTemplate.from_template(template).format(
        json_type=json_type, meeting_time=meeting_time, content=records
    )
    # 创建OpenAI实例
    llm = ChatOpenAI(api_key=api_key, base_url=base_url)

    # 执行模型调用
    response = llm.invoke(prompt)

    # 提取JSON并检查，失败重试一次
    res_json = extract_and_check_task_json(response.content)
    if res_json is None:
        response = llm.invoke(prompt)
        res_json = extract_and_check_task_json(response.content)
    return res_json
