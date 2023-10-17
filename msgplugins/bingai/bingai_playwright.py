import asyncio
import queue
import tempfile
import threading
import time
import traceback
from dataclasses import dataclass
from pathlib import Path
from typing import Callable

from playwright.async_api import async_playwright, Page, BrowserContext

CHROME_DATA_DIR = tempfile.gettempdir() + "/playwright_chrome_data_bingai"


@dataclass
class BingAIImageResponse:
    preview: Path
    img_urls: list[str]


class BingAIPlayWright:

    def __init__(self, proxy: str = "", headless=False):
        self.proxy = proxy
        self.headless = headless
        self.timeout = 90
        # self.page.pause()
        self.pages: dict[str, Page] = {}
        self.page: Page | None = None

    async def new_page(self):
        p = await async_playwright().start()
        browser = await p.chromium.launch_persistent_context(
            CHROME_DATA_DIR,
            headless=self.headless,
            base_url="https://www.bing.com",
            proxy={
                "server": self.proxy,
            } if self.proxy else None)
        return await browser.new_page()
        # p = await self.browser.new_page()
        # await p.goto("https://www.bing.com/chat?cc=us")

    async def change_page(self, user_id: str):
        self.page = await self.__get_page(user_id)

    async def __get_page(self, user_id: str):
        if user_id in self.pages:
            return self.pages[user_id]
        else:
            page = await self.new_page()
            self.pages[user_id] = page
            await page.goto("https://www.bing.com/chat?cc=us", timeout=30000)
            for i in range(30):
                time.sleep(1)
                if await page.query_selector("textarea"):
                    break
            else:
                raise Exception("网络超时")

            return page

    async def send_msg(self, msg: str):
        if not await (await self.page.query_selector("textarea")).is_enabled():
            await self.page.click("button[aria-label='新主题']")
            await asyncio.sleep(1)
        await self.page.fill("textarea", msg)
        await self.page.click("div[class='control submit']")

    @property
    async def is_responding(self) -> bool:
        responding = await (await self.page.query_selector("#stop-responding-button")).is_enabled()
        return responding

    async def get_msg(self):
        for i in range(self.timeout):
            await asyncio.sleep(1)
            if not (await self.is_responding):
                break
        else:
            return "网络超时了~"

        # css选择器 选择ai的文本回复 "cib-message[source='bot'][type='text'] .ac-textBlock"
        replies = await self.page.query_selector_all("cib-message[source='bot'][type='text'] .ac-textBlock")
        last_reply = replies[-1]
        # 移除里面的sup标签
        await last_reply.evaluate("el => el.querySelectorAll('sup').forEach(e => e.remove())")
        return await last_reply.inner_text()

    async def draw(self, prompt: str):
        page = await self.new_page()
        await page.goto("https://www.bing.com/images/create/")
        await page.fill("#sb_form_q", prompt)
        await page.click("#create_btn_c")
        await asyncio.sleep(5)
        for i in range(60 * 5):
            await asyncio.sleep(1)
            create_btn = await page.query_selector("#create_btn_c")
            if await create_btn.inner_text() == "Create":
                break
        else:
            raise Exception("网络超时")

        gir = await page.query_selector("#gir_async")
        path = tempfile.mktemp(suffix=".png")
        path = Path(path)
        await gir.screenshot(path=path)
        img_list = await gir.query_selector_all("img")
        img_urls = []
        for img in img_list:
            img_url = (await img.get_attribute("src")).split("?")[0]
            img_urls.append(img_url)
        return BingAIImageResponse(path, img_urls)


@dataclass
class BingAIChatTask:
    user_id: str
    question: str
    reply_callback: Callable[[str], None]


@dataclass
class BingAIDrawTask:
    prompt: str
    reply_callback: Callable[[BingAIImageResponse], None]


class BinAITaskPool(threading.Thread):
    def __init__(self, proxy: str = "", headless=True):
        self.proxy = proxy
        self.headless = headless
        super().__init__(daemon=True)
        self.chat_task_queue: queue.Queue[BingAIChatTask] = queue.Queue()
        self.draw_task_queue: queue.Queue[BingAIDrawTask] = queue.Queue()

    def put_task(self, task: BingAIChatTask | BingAIDrawTask):
        if isinstance(task, BingAIChatTask):
            self.chat_task_queue.put(task)
        elif isinstance(task, BingAIDrawTask):
            self.draw_task_queue.put(task)

    def run(self):
        bing = BingAIPlayWright(proxy=self.proxy, headless=self.headless)

        async def handle_chat_task(chat_task: BingAIChatTask):
            try:
                await bing.change_page(chat_task.user_id)
                await bing.send_msg(chat_task.question)
            except Exception as e:
                traceback.print_exc()
                reply_text = f"发生了错误：{e}"
            else:
                try:
                    reply_text = await bing.get_msg()
                except Exception as e:
                    reply_text = f"网络错误：{e}"
            threading.Thread(target=chat_task.reply_callback, args=(reply_text,), daemon=True).start()

        async def handle_draw_task(draw_task: BingAIDrawTask):
            draw_resp = await bing.draw(draw_task.prompt)
            threading.Thread(target=draw_task.reply_callback, args=(draw_resp,), daemon=True).start()

        async def handle_task():
            async_tasks = []
            for i in range(2):
                if not self.chat_task_queue.empty():
                    t = self.chat_task_queue.get()
                    async_tasks.append(handle_chat_task(t))
            for i in range(2):
                if not self.draw_task_queue.empty():
                    t = self.draw_task_queue.get()
                    async_tasks.append(handle_draw_task(t))
            if async_tasks:
                await asyncio.gather(*async_tasks)

        while True:
            try:
                asyncio.run(handle_task())
            except Exception as e:
                traceback.print_exc()
                print(e)
                time.sleep(1)


if __name__ == '__main__':
    test = BinAITaskPool(proxy="http://localhost:7890", headless=False)
    test.start()
    while True:
        uid = input("user_id:")
        question = input("请输入问题：")
        print("思考中...")
        if question.startswith("画"):
            test.put_task(BingAIDrawTask(question[1:], print))
        else:
            test.put_task(BingAIChatTask(uid, question, print))
