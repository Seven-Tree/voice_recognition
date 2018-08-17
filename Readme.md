# 语音转文字： API调用程序技术细节
## listen_to_me.py
### 功能
实时监听语句，返回文本。
### 使用前
#### 安装调用的库
- pyaudio（调用系统麦克风） http://people.csail.mit.edu/hubert/pyaudio/   
    - Windows: 
    ```
    python -m pip install pyaudio
    ```
    - Mac:
    ```
    brew install portaudio 
    pip install pyaudio
    ```
    - Debian/Ubuntu:
    ```
    sudo apt-get install python-pyaudio python3-pyaudio
    # OR
    pip install pyaudio
    ```

- speech_recognition (Library for performing speech recognition, with support for several engines and APIs, 但是我们只用其中前期准备的部分，因为这个包不支持讯飞API.以后可以尝试一下把讯飞API写进去。)  https://pypi.org/project/SpeechRecognition/

    > First, make sure you have all the requirements listed in the “Requirements” section.The easiest way to install this is using `pip install SpeechRecognition`. Otherwise, download the source distribution from PyPI, and extract the archive. In the folder, run `python setup.py install`.


### 使用
- 主函数 listen_to_me(threshold=3000)。threshold用来定义多大音量是说话而不是噪音，可以根据所处环境手动调整一下。
- listen_to_me里的`audio = r.listen(source)`会在有说话声时开始录音，说完之后停止录音（无声超过0.8秒即认为说完，这个0.8秒的时长可以手动调整。其中无声的部分不会被保存）。
- 程序的循环现在简单的用了一个 `while True` 语句。想要终止程序可以在 Terminal 按Control+C 即可退出循环。

### 结构说明
- speech_recognition 监听麦克风，当音量超过设定的噪音阈值时，开始录音，没有声音后自动停止。生成一个wav格式的数据对象。
- 将wav发送给讯飞API，等待讯飞返回一个json格式的数据，提取其中的文本。
- 重复此循环

### 想法
- speech_recognition中有一个listen_in_background()程序，可以新开一个thread在后台一直跑，可以尝试。

## 讯飞API
### 官方文档
https://doc.xfyun.cn/rest_api/%E8%AF%AD%E9%9F%B3%E5%90%AC%E5%86%99.htm
### 设置
- 讯飞账户中需要将运行程序的电脑加入ip白名单
- 免费版只能设置5个不同IP
- HTTP post 需要APPID 和 APIKey

### 一些限制
- 免费版每天限制500条
- base64 编码和 urlencode 后大小不超过**2M**，原始音频时长不超过**60s**
- 格式 (mp3, wave, m4a, flac, opus)
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
官方并不 Quick 的 [Quickstart](https://cloud.google.com/speech-to-text/docs/quickstart-client-libraries#client-libraries-install-python)，大致需要
- 在Google CLoud 平台 Set up a GCP Console project.
- 设置  environment variable GOOGLE_APPLICATION_CREDENTIALS
- 安装 Google Cloud SDK
- 安装 the client library
### 不足
- 中文识别准确度明显不如讯飞
- 每个账户总计60分钟后就开始计费，0.6美分/15秒。
- 客户端电脑设置比较麻烦


