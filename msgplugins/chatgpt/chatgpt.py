import openai

openai.api_key = "sk-WWTB6z2HAbiSS9slx7jgEZh4eLjF5lIzjVk4kOhh8f6b6fun"
openai.api_base = "https://api.chatanywhere.com.cn/v1"


def gpt_35(question: str, retry_count=0):
    messages = []
    try:
        response = openai.ChatCompletion.create(
            model='gpt-3.5-turbo',
            messages=[{'role': 'user', 'content': question}],
            stream=True,
        )
        completion = {'role': '', 'content': ''}
        for event in response:
            if event['choices'][0]['finish_reason'] == 'stop':
                # print(f'收到的完成数据: {completion}')
                break
            for delta_k, delta_v in event['choices'][0]['delta'].items():
                # print(f'流响应数据: {delta_k} = {delta_v}')
                completion[delta_k] += delta_v
        messages.append(completion)  # 直接在传入参数 messages 中追加消息
        return "\n".join(map(lambda m: m['content'], messages))
    except Exception as err:
        if retry_count > 2:
            return f'糟了，发生了未知错误'
        return gpt_35(question, retry_count+1)


if __name__ == '__main__':
    print(gpt_35("你是谁"))
