import openai
import requests


class ChatGPT:

    def __init__(self,
                 prompt="",
                 api_key: str = "",
                 api_base: str = "",
                 http_proxy: str = "",
                 model: str = "gpt-3.5-turbo-1106"
                 ):
        self.api_key = api_key
        self.api_base = api_base
        self.model = model
        self.question_max = 8000
        self.history_max = 10
        self.prompt = prompt
        self.history = []  # messages
        if http_proxy:
            # Set up the proxy
            proxies = {
                'http': http_proxy,
                'https': http_proxy
            }

            # Apply the proxy to the session
            session = requests.Session()
            session.proxies = proxies
            openai.api_engine = session

        # todo: refactor to use AsyncOpenAI
        self.openai_client = openai.Client(api_key=self.api_key, base_url=self.api_base)

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
        user_message = {'role': 'user', 'content': question}
        messages.append(user_message)

        response = self.openai_client.chat.completions.create(
            model=self.model,
            # prompt=prompt,
            messages=messages,
            stream=True,
        )
        completion = {'role': 'assistant', 'content': ''}
        for event in response:
            choice = event.choices[0]
            if choice.finish_reason == 'stop':
                break
            completion['content'] += choice.delta.content
        self.history.append(user_message)
        self.history.append(completion)
        return completion['content']


if __name__ == '__main__':
    c = ChatGPT("", "sk-x2OlFyj9BDsLyjMH9JWo3J7TJZRptLwy1ccwacsDyCex1dhr", "https://api.chatanywhere.tech/")
    print(c.chat("你好啊"))
