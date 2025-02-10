import litellm
from .sse import TXChatSSEClient

class TXCloudLLM(litellm.CustomLLM):
    async def acompletion(self, *args, **kwargs):
        app_key = kwargs.get('api_key')
        session_id = kwargs.get('optional_params').get('session_id')
        messages = kwargs.get('messages', [])
        # 提取提示词
        prompt = ''
        for message in messages:
            if message['role'] == 'system':
                prompt += message['content'] + '\n'
        client = TXChatSSEClient(app_key, session_id, prompt)
        return await client.chat(messages[-1]['content'])

