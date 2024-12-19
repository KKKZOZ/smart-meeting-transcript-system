# -*- coding: utf-8 -*-
import oss2
from datetime import datetime
from app.core.config import get_settings


# 用于上传文件，例如在录音完就将录音文件上传，或者用户选择上传时先将其传至云端
def upload(file_url):
    """
    上传文件到OSS，并设置权限为公共读写。

    参数:
        file_url (str): 本地文件路径，包括文件名和后缀。

    返回:
        tuple: (是否成功上传, 是否成功修改权限)，均为布尔值。
    """
    try:
        # 配置访问密钥
        settings = get_settings()
        access_key_id = settings.ALIBABA_ACCESS_KEY_ID  # 替换为你的AccessKey ID
        access_key_secret = (
            settings.ALIBABA_ACCESS_KEY_SECRET
        )  # 替换为你的AccessKey Secret

        # 配置OSS参数
        auth = oss2.Auth(access_key_id, access_key_secret)
        endpoint = "oss-cn-beijing.aliyuncs.com"
        bucket_name = "software-project510"

        # 创建Bucket对象
        bucket = oss2.Bucket(auth, endpoint, bucket_name)

        # 提取目标文件的OSS路径
        object_name = file_url.split("/")[-1]
        # 获取当前时间
        current_time = datetime.now()

        # 格式化输出当前时间为 "年-月-日 时:分:秒" 格式
        formatted_file = (
            "Audio/" + current_time.strftime("%Y-%m-%d") + "-" + object_name
        )

        # 上传文件
        bucket.put_object_from_file(formatted_file, file_url)
        upload_success = True

        # 修改文件权限
        bucket.put_object_acl(formatted_file, oss2.OBJECT_ACL_PUBLIC_READ_WRITE)
        acl_success = True

    except Exception as e:
        # 打印错误信息
        print(f"错误: {e}")
        upload_success = False
        acl_success = False
    file1 = "https://software-project510.oss-cn-beijing.aliyuncs.com/" + formatted_file
    return upload_success, acl_success, file1


# # 测试函数
# file_path = '../audio/english.mp3'  # 替换为你的本地文件路径
# result = upload(file_path)
# print(f"上传成功: {result[0]}, 权限修改成功: {result[1]}")
