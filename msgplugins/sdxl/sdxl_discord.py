from dataclasses import dataclass
from selenium import webdriver
from selenium.webdriver.common.by import By

sd_url = 'https://discord.com/channels/1002292111942635562/1101178553900478464'


@dataclass()
class Message:
    msg_id: str
    img_list: list[str]


class SDDiscord:
    driver = webdriver.Chrome()
    driver.get(url=sd_url)

    username = "linyuchen"
    token = 'OTcxNjU4ODc5MzM3MzkwMTEx.GeNwYx.DBZvcdcXF1qdQKhdjG9Sd21BDZqAnclisw2bd0'
    # 注入token
    js = f"""
        const token = "{token}";
        setInterval(() => {{
            document.body.appendChild(document.createElement('iframe')).contentWindow.localStorage.token = `"${{token}}"`;
        }}, 50);
        setTimeout(() => {{
            location.reload();
        }}, 2500);
    """
    driver.execute_script(js)

    driver.implicitly_wait(10)

    def __init__(self):
        pass

    def find_msg(self) -> list[Message]:
        result: list[Message] = []
        # 查找消息列表元素
        chat_messages_ele = self.driver.find_element(by=By.CSS_SELECTOR, value='ol[data-list-id="chat-messages"]')
        message_els = chat_messages_ele.find_elements(by=By.CSS_SELECTOR, value='li')

        for msg_ele in message_els:
            msg_id = msg_ele.get_attribute("id").split("-")[-1]
            txt_ele = msg_ele.find_element(by=By.ID, value=f"message-content-{msg_id}")
            # sd的机器人消息，第一个span是@谁，用这个来判断是不是回复自己,可能有更好的方法识别回复自己的消息
            at_txt = txt_ele.find_element(by=By.TAG_NAME, value="span").text
            # print(at_txt)
            # 如果是回复自己的消息，就把图片内容提取出来
            if at_txt.strip() == f"@{self.username}":
                message = Message(msg_id=msg_id, img_list=[])
                attachment_el = msg_ele.find_element(by=By.ID, value=f"message-accessories-{msg_id}").find_element(
                    by=By.TAG_NAME, value="div")
                img_list = attachment_el.find_elements(by=By.TAG_NAME, value="a")
                for img_ele in img_list:
                    # todo: 需要在url上加上分辨率，不然太大了
                    href = img_ele.get_attribute("href")
                    message.img_list.append(href)
                result.append(message)
        return result
