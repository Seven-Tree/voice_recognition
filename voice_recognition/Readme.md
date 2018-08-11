# 语音转文字： API调用程序技术细节
## 讯飞API
### 官方文档 [https://doc.xfyun.cn/rest_api/%E8%AF%AD%E9%9F%B3%E5%90%AC%E5%86%99.html](https://doc.xfyun.cn/rest_api/%E8%AF%AD%E9%9F%B3%E5%90%AC%E5%86%99.htm)
### 设置
- 讯飞账户中需要将运行程序的电脑加入ip白名单
- 

### 一些限制
- 免费版每天限制500条？？（记不清了）
- base64 编码和 urlencode 后大小不超过**2M**，原始音频时长不超过**60s**
- 格式？
- 音频参数	数值
    - 音频长度（Input Length）	≤60s
    - 采样率（Sampling Rate）	支持**8KHz和16KHz**
    - 采样精度（Bit Depth）	16bits
    - 声道（Channel）	**单声道**
    - 语音起点（begin of the speech）	小于参数vad_bos
    - 音频终点（end of the speech）	小于参数vad_eos
- 音频中如果语音停顿过长，停顿后面的部分就不再识别了。
## Goolge API
### 设置
官方并不Quick的 [Quickstart](https://cloud.google.com/speech-to-text/docs/quickstart-client-libraries#client-libraries-install-python)，大致需要
- 在Google CLoud 平台 Set up a GCP Console project.
- 设置  environment variable GOOGLE_APPLICATION_CREDENTIALS
- 安装 Google Cloud SDK
- 安装 the client library
### 不足
- 中文明显不如讯飞
- 每个账户总计60分钟后就开始计费，0.6美分/15秒。
- 客户端电脑设置比较麻烦


