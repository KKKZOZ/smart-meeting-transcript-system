from sparkai.llm.llm import ChatSparkLLM, ChunkPrintHandler
from sparkai.core.messages import ChatMessage
from app.core.config import get_settings


def summary_generate(transcription_content, summary_type):
    """
    使用讯飞星火大语言模型对会议记录进行总结。

    :param transcription_content: 会议记录文本
    :return: 总结后的文本
    """
    settings = get_settings()
    spark_api_url = settings.SPARKAI_URL
    spark_app_id = settings.SPARKAI_APP_ID
    spark_api_key = settings.SPARKAI_API_KEY
    spark_api_secret = settings.SPARKAI_API_SECRET
    spark_llm_domain = settings.SPARKAI_DOMAIN

    # 初始化大语言模型客户端
    spark = ChatSparkLLM(
        spark_api_url=spark_api_url,
        spark_app_id=spark_app_id,
        spark_api_key=spark_api_key,
        spark_api_secret=spark_api_secret,
        spark_llm_domain=spark_llm_domain,
        streaming=False,
    )

    # 构造提示词
    prompt = f"你是一位专业的会议记录总结者。请基于以下提供的会议记录内容，撰写一份简洁明了的总结报告。请注意保持总结的专业性和客观性，避免不必要的细节，确保总结内容简明扼要且易于理解。要求：{summary_type}。会议记录内容如下：{transcription_content}"

    # 构造用户消息
    # messages = [ChatMessage(role="user", content=prompt)]
    # result = spark.generate(messages)
    # answer = result.generations[0][0].text

    messages = [ChatMessage(role="user", content=prompt)]
    handler = ChunkPrintHandler()
    data = spark.generate([messages], callbacks=[handler])

    for generation_list in data.generations:
        for generation in generation_list:
            content = generation.message.content
            print(content)

            return content
