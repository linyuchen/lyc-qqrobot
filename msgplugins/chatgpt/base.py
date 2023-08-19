import openai


class ChatGPT:

    def __init__(self,
                 prompt="",
                 api_key: str = "",
                 api_base: str = "",
                 model: str = "gpt-3.5-turbo-0613"):
        self.api_key = api_key
        self.api_base = api_base
        self.model = model
        self.question_max = 8000
        self.history_max = 10
        self.prompt = prompt
        self.history = []  # messages

    def get_prompt(self):
        return self.prompt

    def set_prompt(self, prompt_text: str = ""):
        self.prompt = prompt_text

    def del_prompt(self):
        self.set_prompt()

    def clear_history(self):
        self.history.clear()

    def chat(self, question: str) -> str:
        if len(self.history) > self.history_max:
            del self.history[:3]
        messages = self.history[:]
        messages.insert(0, {'role': 'system', 'content': self.prompt})
        if len(question) > self.question_max:
            question = question[0:(self.question_max // 2)] + question[-(self.question_max // 2):]
        messages.append({'role': 'user', 'content': question})

        response = openai.ChatCompletion.create(
            model=self.model,
            api_key=self.api_key,
            api_base=self.api_base,
            # prompt=prompt,
            messages=messages,
            stream=True,
        )
        completion = {'role': '', 'content': ''}
        res = []
        for event in response:
            if event['choices'][0]['finish_reason'] == 'stop':
                # print(f'收到的完成数据: {completion}')
                break
            for delta_k, delta_v in event['choices'][0]['delta'].items():
                # print(f'流响应数据: {delta_k} = {delta_v}')
                completion[delta_k] += delta_v
        res.append(completion)  # 直接在传入参数 messages 中追加消息
        res = "\n".join(map(lambda m: m['content'], res))
        self.history.append({'role': 'assistant', 'content': res})
        return res
