from replicate import Client

from common.utils.baidu_translator import is_chinese, trans


class AIReplicateClient:
    def __init__(self, api_token: str):
        self.api_token = api_token

    def __trans_zh_prompt(self, prompt: str):
        if is_chinese(prompt):
            prompt = trans(prompt)
        return prompt

    def gen_qrcode(self, content: str, prompt: str):
        output = Client(api_token=self.api_token).run(
            "dannypostma/cog-visual-qr:7653601d0571fa6342ba4fa93a0962adebd1169e9e2329eefeb5729cac645d42",
            input={"qr_code_content": content, "prompt": self.__trans_zh_prompt(prompt)}
        )
        return output

    def gen_sdxl(self, prompt: str):
        output = Client(api_token=self.api_token).run(
            "stability-ai/sdxl:a00d0b7dcbb9c3fbb34ba87d2d5b46c56969c84a628bf778a7fdaec30b1b99c5",
            input={"prompt": self.__trans_zh_prompt(prompt)}
        )
        return output
