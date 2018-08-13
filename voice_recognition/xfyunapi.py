# !/usr/bin/python
# -*- coding: UTF-8 -*-
import urllib3
from urllib.request import urlopen

import time
import urllib
import json
import hashlib
import base64


def main():
    f = open(r"sample_7.wav", 'rb')
    file_content = f.read()
    base64_audio = base64.b64encode(file_content)
    body = urllib.parse.urlencode({'audio': base64_audio})
    body = body.encode('utf-8')

    url = 'http://api.xfyun.cn/v1/service/v1/iat'

    api_key = '008d375d21d042a7af90dc31520ae6f5'
    param = {"engine_type": "sms16k", "aue": "raw"}

    x_appid = '5b6e5b3e'
    audio_str = json.dumps(param).replace(' ', '')
    x_param = base64.b64encode(audio_str.encode('utf-8'))


    # x_time = int(int(round(time.time() * 1000)) / 1000)
    # txt = api_key + str(x_time) + base64.b64encode(x_param).decode('utf-8');
    # newtxt = base64.b64encode(txt.encode('utf-8'))
    # x_checksum = hashlib.md5(newtxt).hexdigest()
    # time_now = str(int(time.time()))
    # checksum = (api_key + time_now + x_param).encode('utf8')
    # x_checksum = hashlib.md5(checksum).hexdigest()

    # 配置参数编码为base64字符串，过程：字典→明文字符串→utf8编码→base64(bytes)→base64字符串
    Param_str = json.dumps(param)  # 得到明文字符串
    Param_utf8 = Param_str.encode('utf8')  # 得到utf8编码(bytes类型)
    Param_b64 = base64.b64encode(Param_utf8)  # 得到base64编码(bytes类型)
    Param_b64str = Param_b64.decode('utf8')  # 得到base64字符串

    # 构造HTTP请求的头部
    time_now = str(int(time.time()))
    checksum = (api_key + time_now + Param_b64str).encode('utf8')
    checksum_md5 = hashlib.md5(checksum).hexdigest()

    x_header = {
        "X-Appid": x_appid,
        "X-CurTime": time_now,
        "X-Param": Param_b64str,
        "X-CheckSum": checksum_md5
    }

    print(time_now)
    # x_header = {'X-Appid': x_appid,
    #             'X-CurTime': x_time,
    #             'X-Param': x_param,
    #             'X-CheckSum': x_checksum}


    req = urllib.request.Request(url, body, x_header)
    result = urllib.request.urlopen(req)
    result = result.read().decode('utf-8')
    print(result)
    # print(result["data"])
    type(result)
    return

if __name__ == '__main__':
    main()