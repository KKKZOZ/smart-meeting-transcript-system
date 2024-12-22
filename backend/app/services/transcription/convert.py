#!/usr/bin/env python
# coding=utf-8

import datetime
import json
import time

import requests
from aliyunsdkcore.auth.credentials import AccessKeyCredential
from aliyunsdkcore.client import AcsClient
from aliyunsdkcore.request import CommonRequest
from app.core.config import get_settings


# https://software-project510.oss-cn-beijing.aliyuncs.com/test/hello.md


# 简单请求
def create_common_request(domain, version, protocolType, method, uri):
    request = CommonRequest()
    request.set_accept_format("json")
    request.set_domain(domain)
    request.set_version(version)
    request.set_protocol_type(protocolType)
    request.set_method(method)
    request.set_uri_pattern(uri)
    request.add_header("Content-Type", "application/json")
    return request


# 初始化
def init_parameters(file_url):
    body = dict()
    body["AppKey"] = "ZqgRbr5G72cnsUut"

    # 基本请求参数
    input = dict()
    input["SourceLanguage"] = "auto"
    input["TaskKey"] = "task" + datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    input["FileUrl"] = file_url
    body["Input"] = input

    # AI相关参数，按需设置即可
    parameters = dict()

    # 音视频转换相关
    # transcoding = dict()
    # 将原音视频文件转成mp3文件，用以后续浏览器播放
    # transcoding['TargetAudioFormat'] = 'mp3'
    # transcoding['SpectrumEnabled'] = False
    # parameters['Transcoding'] = transcoding

    # 语音识别控制相关
    transcription = dict()
    # 角色分离 ： 可选
    transcription["DiarizationEnabled"] = True
    diarization = dict()
    diarization["SpeakerCount"] = 0
    transcription["Diarization"] = diarization
    parameters["Transcription"] = transcription

    # 文本翻译控制相关 ： 可选
    parameters["TranslationEnabled"] = False
    translation = dict()
    translation["TargetLanguages"] = ["en"]  # 假设翻译成英文
    parameters["Translation"] = translation

    # 章节速览相关 ： 可选，包括： 标题、议程摘要
    parameters["AutoChaptersEnabled"] = False

    # 智能纪要相关 ： 可选，包括： 待办、关键信息(关键词、重点内容、场景识别)
    parameters["MeetingAssistanceEnabled"] = False
    meetingAssistance = dict()
    meetingAssistance["Types"] = ["Actions", "KeyInformation"]
    parameters["MeetingAssistance"] = meetingAssistance

    # 摘要控制相关 ： 可选，包括： 全文摘要、发言人总结摘要、问答摘要(问答回顾)
    parameters["SummarizationEnabled"] = False
    summarization = dict()
    summarization["Types"] = [
        "Paragraph",
        "Conversational",
        "QuestionsAnswering",
        "MindMap",
    ]
    parameters["Summarization"] = summarization

    # ppt抽取和ppt总结 ： 可选
    parameters["PptExtractionEnabled"] = False

    # 口语书面化 ： 可选
    parameters["TextPolishEnabled"] = False

    body["Parameters"] = parameters
    return body


# 回调
def poll_task_status(task_id, interval=10):
    """
    轮询任务状态，直到任务完成。

    参数:
        task_id (str): 创建任务返回的 TaskId。
        interval (int): 轮询间隔（秒）。

    返回:
        dict: 任务完成时的 JSON 响应。
    """
    # 配置访问密钥
    settings = get_settings()
    access_key_id = settings.ALIBABA_ACCESS_KEY_ID  # 替换为你的AccessKey ID
    access_key_secret = settings.ALIBABA_ACCESS_KEY_SECRET  # 替换为你的AccessKey Secret
    credentials = AccessKeyCredential(access_key_id, access_key_secret)
    client = AcsClient(region_id="cn-beijing", credential=credentials)

    uri = f"/openapi/tingwu/v2/tasks/{task_id}"
    request = create_common_request(
        domain="tingwu.cn-beijing.aliyuncs.com",
        version="2023-09-30",
        protocolType="https",
        method="GET",
        uri=uri,
    )

    while True:
        try:
            response = client.do_action_with_exception(request)
            response_data = json.loads(response)

            # 打印当前任务状态（可选）
            print(
                f"轮询中，任务状态: {response_data.get('Data', {}).get('TaskStatus', 'UNKNOWN')}"
            )

            # 检查任务状态
            if response_data.get("Data", {}).get("TaskStatus") == "COMPLETED":
                print("任务已完成！")
                return response

        except Exception as e:
            print(f"轮询时发生错误: {e}")

        # 间隔轮询
        time.sleep(interval)


# json转txt(change
def splicing(before_response):
    try:
        # 从返回的 JSON 中提取 URL
        r = json.loads(before_response)
        transcription_url = r.get("Data", {}).get("Result", {}).get("Transcription", "")

        # 下载 JSON 文件并解析
        response = requests.get(transcription_url)
        transcription_data = response.json()  # 使用 .json() 方法解析返回的 JSON 内容

        # 将所有 Words 存储到一个列表中，并记录发言人和时间
        all_words = []

        # 遍历所有段落
        for paragraph in transcription_data["Transcription"]["Paragraphs"]:
            speaker_id = paragraph["SpeakerId"]
            for word in paragraph["Words"]:
                all_words.append(
                    {
                        "SpeakerId": speaker_id,
                        "Start": word["Start"],
                        "Text": word["Text"],
                    }
                )

        # 按照时间顺序对所有的单词进行排序
        all_words.sort(key=lambda x: x["Start"])

        # 按发言人分组文本
        speaker_text = {}
        for word in all_words:
            speaker_id = word["SpeakerId"]
            if speaker_id not in speaker_text:
                speaker_text[speaker_id] = []
            speaker_text[speaker_id].append(word["Text"])

        # 按照时间顺序生成最终的文本
        result_text = []
        current_speaker = None
        current_sentence = []
        for word in all_words:
            speaker_id = word["SpeakerId"]
            # 如果当前发言人和上一个发言人不一样，就输出上一发言人的内容
            if speaker_id != current_speaker:
                if current_sentence:
                    result_text.append(
                        f"发言人{current_speaker}: {''.join(current_sentence)}"
                    )
                current_speaker = speaker_id
                current_sentence = [word["Text"]]
            else:
                current_sentence.append(word["Text"])

        # 最后一个发言人的内容也要输出
        if current_sentence:
            result_text.append(f"发言人{current_speaker}: {''.join(current_sentence)}")
        speaker_count = len(speaker_text)
        # 将所有发言人的文本合并为最终的字符串并返回
        return "\n".join(result_text), speaker_count

    except Exception as e:
        print(f"An error occurred: {e}")


def splicing_second(before_response, speakers_json):
    try:
        # 解析 JSON 字符串为 Python 列表
        speakers = json.loads(speakers_json)

        # 创建一个字典，将索引作为键，发言人作为值
        speakers_dict = {index + 1: speaker for index, speaker in enumerate(speakers)}

        print(speakers_dict)
        # 从返回的 JSON 中提取 URL
        r = json.loads(before_response)
        transcription_url = r.get("Data", {}).get("Result", {}).get("Transcription", "")

        # 下载 JSON 文件并解析
        response = requests.get(transcription_url)
        transcription_data = response.json()  # 使用 .json() 方法解析返回的 JSON 内容

        # 将所有 Words 存储到一个列表中，并记录发言人和时间
        all_words = []

        # 遍历所有段落
        for paragraph in transcription_data["Transcription"]["Paragraphs"]:
            speaker_id = paragraph["SpeakerId"]
            for word in paragraph["Words"]:
                all_words.append(
                    {
                        "SpeakerId": speaker_id,
                        "Start": word["Start"],
                        "Text": word["Text"],
                    }
                )

        # 按照时间顺序对所有的单词进行排序
        all_words.sort(key=lambda x: x["Start"])

        # 按发言人分组文本
        speaker_text = {}
        for word in all_words:
            speaker_id = word["SpeakerId"]
            if speaker_id not in speaker_text:
                speaker_text[speaker_id] = []
            speaker_text[speaker_id].append(word["Text"])

        # 按照时间顺序生成最终的文本
        result_text = []
        current_speaker = None
        current_sentence = []
        for word in all_words:
            speaker_id = word["SpeakerId"]
            # 如果当前发言人和上一个发言人不一样，就输出上一发言人的内容
            if speaker_id != current_speaker:
                if current_sentence:
                    # 使用 speakers_dict 来替代原来的发言人编号
                    speaker_name = speakers_dict.get(
                        int(current_speaker), f"发言人{current_speaker}"
                    )
                    result_text.append(f"{speaker_name}: {''.join(current_sentence)}")
                current_speaker = speaker_id
                current_sentence = [word["Text"]]
            else:
                current_sentence.append(word["Text"])

        # 最后一个发言人的内容也要输出
        if current_sentence:
            speaker_name = speakers_dict.get(
                int(current_speaker), f"发言人{current_speaker}"
            )
            result_text.append(f"{speaker_name}: {''.join(current_sentence)}")

        # 将所有发言人的文本合并为最终的字符串并返回
        return "\n".join(result_text)

    except Exception as e:
        print(f"An error occurred: {e}")
        return ""


# 创建语音转文字任务
def create_task(file_url):
    """
    创建Tingwu离线任务。

    参数:
        access_key_id (str): 阿里云AccessKey ID。
        access_key_secret (str): 阿里云AccessKey Secret。
        region_id (str): 地区ID，例如 'cn-beijing'。
        file_url (str): 要处理的文件名（OSS中的路径）。

    返回:
        dict: 请求响应的JSON结果。
    """
    try:
        # 配置访问密钥
        settings = get_settings()
        access_key_id = settings.ALIBABA_ACCESS_KEY_ID  # 替换为你的AccessKey ID
        access_key_secret = (
            settings.ALIBABA_ACCESS_KEY_SECRET
        )  # 替换为你的AccessKey Secret
        # 初始化客户端
        credentials = AccessKeyCredential(access_key_id, access_key_secret)
        client = AcsClient(region_id="cn-beijing", credential=credentials)

        # 初始化参数
        body = init_parameters(file_url)

        # 构建请求
        request = create_common_request(
            domain="tingwu.cn-beijing.aliyuncs.com",
            version="2023-09-30",
            protocolType="https",
            method="PUT",
            uri="/openapi/tingwu/v2/tasks",
        )
        request.add_query_param("type", "offline")
        request.set_content(json.dumps(body).encode("utf-8"))

        # 发送请求并解析响应
        response = client.do_action_with_exception(request)

        return response

    except Exception as e:
        print(f"任务创建失败: {e}")
        return None


# if __name__ == "__main__":
#     response_task = create_task('Audio/2024-12-06-student.m4a')
#     response_Trans = poll_task_status(response_task)
#     # splicing(response_Trans)
#     print(response_Trans)
