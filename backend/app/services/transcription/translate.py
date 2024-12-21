# -*- coding: utf-8 -*-
import random
from hashlib import md5
import requests

from app.core.config import get_settings


def translate(content, language, to_language):
    # Set your own appid/appkey.
    settings = get_settings()
    appid = settings.BAIDU_APP_ID
    appkey = settings.BAIDU_APP_KEY

    # For list of language codes, please refer to `https://api.fanyi.baidu.com/doc/21`
    from_lang = language
    to_lang = to_language

    endpoint = "http://api.fanyi.baidu.com"
    path = "/api/trans/vip/translate"
    url = endpoint + path
    query = content

    # Generate salt and sign
    def make_md5(s, encoding="utf-8"):
        return md5(s.encode(encoding)).hexdigest()

    salt = random.randint(32768, 65536)
    sign = make_md5(appid + query + str(salt) + appkey)

    # Build request
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    payload = {
        "appid": appid,
        "q": query,
        "from": from_lang,
        "to": to_lang,
        "salt": salt,
        "sign": sign,
    }

    # Send request
    r = requests.post(url, params=payload, headers=headers)
    result = r.json()
    # print(json.dumps(result, indent=4, ensure_ascii=False))
    translated_text = "\n".join(item["dst"] for item in result["trans_result"])
    # Show response
    return translated_text
