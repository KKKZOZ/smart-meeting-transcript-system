from sparkai.llm.llm import ChatSparkLLM,ChunkPrintHandler
from sparkai.core.messages import ChatMessage
# import json
#from app.core.config import get_settings

# settings = get_settings()
# spark_api_url = settings.SPARKAI_URL
# spark_app_id = settings.SPARKAI_APP_ID
# spark_api_key = settings.SPARKAI_API_KEY
# spark_api_secret = settings.SPARKAI_API_SECRET
# spark_llm_domain = settings.SPARKAI_DOMAIN

# SPARKAI_URL = "wss://spark-api.xf-yun.com/v4.0/chat"
# SPARKAI_APP_ID = "cf1e08a3"
# SPARKAI_API_SECRET = "MWY2NDg2N2Y1OWE5ZWM3NGNjN2UwNjhi"
# SPARKAI_API_KEY = "1a288cd0de7af88398293d92784b6bb4"
# SPARKAI_DOMAIN = "4.0Ultra"


def summary_generate(transcription_content,summary_type):
    """
    使用讯飞星火大语言模型对会议记录进行总结。

    :param transcription_content: 会议记录文本
    :return: 总结后的文本
    """
    # settings = get_settings()
    # spark_api_url = settings.SPARKAI_URL
    # spark_app_id = settings.SPARKAI_APP_ID
    # spark_api_key = settings.SPARKAI_API_KEY
    # spark_api_secret = settings.SPARKAI_API_SECRET
    # spark_llm_domain = settings.SPARKAI_DOMAIN

    spark_api_url = "wss://spark-api.xf-yun.com/v4.0/chat"
    spark_app_id = "cf1e08a3"
    spark_api_secret = "MWY2NDg2N2Y1OWE5ZWM3NGNjN2UwNjhi"
    spark_api_key = "1a288cd0de7af88398293d92784b6bb4"
    spark_llm_domain = "4.0Ultra"

    # 初始化大语言模型客户端
    spark = ChatSparkLLM(
        spark_api_url=spark_api_url,
        spark_app_id=spark_app_id,
        spark_api_key=spark_api_key,
        spark_api_secret=spark_api_secret,
        spark_llm_domain=spark_llm_domain,
        streaming=False,
    )

    #构造提示词
    prompt = (
        f"你是一位专业的会议记录总结者。请基于以下提供的会议记录内容，撰写一份简洁明了的总结报告。请注意保持总结的专业性和客观性，避免不必要的细节，确保总结内容简明扼要且易于理解。要求：{summary_type}。会议记录内容如下：{transcription_content}"
    )

    # 构造用户消息
    # messages = [ChatMessage(role="user", content=prompt)]
    # result = spark.generate(messages)
    # answer = result.generations[0][0].text

    messages = [ChatMessage(
        role="user",
        content=prompt
    )]
    handler = ChunkPrintHandler()
    data = spark.generate([messages], callbacks=[handler])

    for generation_list in data.generations:
        for generation in generation_list:
            content = generation.message.content
            print(content)

            return content


# if __name__ == "__main__":
    # summary_generate("张经理：大家好，感谢大家抽出时间参加这次会议。今天的主要议题是讨论客户服务流程的改进。首先，我想听听大家对目前服务流程的看法。李主管：我认为我们目前的响应时间还有待提高。有些客户反馈，他们的咨询没有得到及时回复。王专员：我同意李主管的观点。此外，我们的服务流程可以更加标准化，比如设立常见问题解答库，这样能提高我们解决问题的效率。赵助理：我觉得我们可以利用一些客服软件，实现多渠道接入，这样客户可以通过他们喜欢的方式与我们沟通。刘分析师：我分析了客户反馈数据，发现很多客户对我们的售后服务满意度不高。我们可以考虑延长售后服务时间，并提供更灵活的解决方案。张经理：很好，大家提出了很多有建设性的意见。那么，我们来布置一下任务。李主管，您负责牵头优化响应时间，制定具体措施，并监督执行。李主管：好的，我会尽快拿出方案。张经理：王专员，您负责建立常见问题解答库，并与相关部门协作，确保内容的准确性和实用性。王专员：明白了，我会着手进行。张经理：赵助理，您调研一下市场上的客服软件，看看哪款更适合我们，并准备一份推荐报告。赵助理：好的，我会尽快完成调研。张经理：刘分析师，您继续监控客户反馈数据，为我们提供改进方向。同时，协助李主管优化售后服务流程。刘分析师：没问题，我会持续关注。张经理：好的，今天的会议就到这里。请大家按照分工，积极推进任务。谢谢大家！", "简要概述")
