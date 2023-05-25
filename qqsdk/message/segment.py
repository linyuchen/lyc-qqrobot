from typing import Optional, List, Tuple


class MessageSegment:
    """
    用于封装成发送的消息
    """

    def __init__(self, msg_type: Optional[str] = None, content: Optional[str] = None):
        self.msg_type = msg_type
        self.content = content
        self.origin_data: List[Tuple[str, str]] = []
        if msg_type and content:
            self.origin_data.append((msg_type, content))

    @staticmethod
    def text(content: str):
        return MessageSegment("Plain", content)

    @staticmethod
    def image(image_url: str):
        return MessageSegment("ImageUrl", image_url)

    @staticmethod
    def image_path(path: str):
        return MessageSegment("ImagePath", path)

    def to_data(self, msg_type: str, content: str):
        """
        可以在外部更改此方法
        """
        data = {"type": msg_type}
        if msg_type == "Plain":
            data.update({"text": content})
        elif msg_type == "ImageUrl":
            data.update({"type": "Image", "url": content})
        elif msg_type == "ImagePath":
            data.update({"type": "Image", "path": content})
        return data

    @property
    def data(self) -> List:
        result = []
        for msg_data in self.origin_data:
            result.append(self.to_data(msg_data[0], msg_data[1]))
        return result

    def __add__(self, other: 'MessageSegment') -> 'MessageSegment':
        ms = MessageSegment()
        ms.origin_data = self.origin_data
        ms.origin_data.append((other.msg_type, other.content))
        return ms
