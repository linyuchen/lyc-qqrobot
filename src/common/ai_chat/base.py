from litellm import completion


class AIChat:

    def __init__(self,
                 prompt="",
                 api_key: str = "",
                 base_url: str = "",
                 model: str = "",  # 参考 https://docs.litellm.ai/docs/providers
                 history_max=10,
                 ):
        self.api_key = api_key
        self.base_url = base_url
        self.model = model
        self.history_max = history_max
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
        # if len(question) > self.question_max:
        #     question = question[0:(self.question_max // 2)] + question[-(self.question_max // 2):]
        user_message = {'role': 'user', 'content': question}
        messages.append(user_message)

        response = completion(
            api_key=self.api_key,
            base_url=self.base_url,
            model=self.model,
            messages=messages,
            stream=True,
        )
        reply = {'role': 'assistant', 'content': ''}
        for event in response:
            choice = event.choices[0]
            if choice.finish_reason == 'stop':
                break
            reply['content'] += choice.delta.content
        self.history.append(user_message)
        self.history.append(reply)
        return reply['content']
