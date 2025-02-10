import json
import uuid

import httpx


url = 'https://wss.lke.cloud.tencent.com/v1/qbot/chat/sse'

class TXChatSSEClient:
    def __init__(self, app_key: str, session_id: str = None, prompt: str = ''):
        self.app_key = app_key
        self.visitor_biz_id = 'lyc-bot'
        self.session_id = session_id or str(uuid.uuid4())
        self.prompt = prompt

    async def chat(self, content: str) -> str:
        req_data = {
            'content': content,
            'bot_app_key': self.app_key,
            'visitor_biz_id': self.visitor_biz_id,
            'session_id': self.session_id,
            'system_role': self.prompt
        }
        resp_content = ''
        async with httpx.AsyncClient(timeout=None) as client:
            async with client.stream('POST', url, data=json.dumps(req_data)) as resp:
                async for line in resp.aiter_lines():
                    if line.startswith("data:"):
                        data = line.split("data:", 1)[1]
                        data = json.loads(data)
                        # if data['payload']['is_final']:
                        resp_content = data['payload'].get('content', '')
        return resp_content.strip()
