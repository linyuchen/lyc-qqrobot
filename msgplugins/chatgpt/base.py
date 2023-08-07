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
        self.question_max_len = 4000
        self.history_max = 10
        self.prompt = {'role': 'system', 'content': prompt}
        self.history = []  # messages
        self.add_prompt()

    def add_prompt(self):
        if self.prompt not in self.history:
            self.history.insert(0, self.prompt)

    def del_prompt(self):
        if self.prompt in self.history:
            self.history.remove(self.prompt)

    def chat(self, question: str) -> str:
        messages = self.history
        if len(messages) > self.history_max:
            del messages[:3]

        if len(question) > self.question_max_len:
            question = question[0:self.question_max_len / 2] + question[-self.question_max_len / 2:]
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
        messages.append({'role': 'assistant', 'content': res})
        return res
