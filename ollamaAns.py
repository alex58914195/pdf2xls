import requests
# 调用ollama
# ollama_url、model_name为可选参数

def ollamaAns(question,text,ollama_url = 'http://10.8.0.3:11434',model_name = 'qwen2.5:7b'):
    # # Ollama服务的URL和端口
    # ollama_url = 'http://xxxx:11434'
    # #指定要使用的模型
    # model_name = 'qwen2.5:14b'
        # 要生成文本的提示
    prompt = '开启新的话题，根据下文告诉我'+question+'，直接给出回答不需要任何其他多余语言，也不要包含'+question+'：'+text
    # 用以下格式告诉我：项目名称：XXXXX，换行，四至范围：XXXXX，换行，文件印发日期：XXXXX，换行，项目用地性质：XXXXX
    # 构建请求数据
    data = {
        'model': model_name,
        'prompt': prompt,
        'stream': False  # 如果设置为True，将返回流式响应
    }

    # 发送POST请求
    response = requests.post(f'{ollama_url}/api/generate', json=data)
    # 检查响应状态码
    if response.status_code == 200:
        # 打印生成的文本
        # print(response.json()['response'])
        pass
    else:
        print(f'请求失败，状态码：{response.status_code}')
    return response

if __name__=="__main__":
    print("ollamaAns.py is running") 
    ans=ollamaAns('项目名称', '本项目为xxx土地储备项目。') # 调用ollamaAns函数，传入问题和上下文文本
    # ans=ans.json()['response'] # 将响应转换为JSON格式并获取生成的文本
    # print(ans) 

