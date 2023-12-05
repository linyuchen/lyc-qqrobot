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


@dataclass
class PageLifeCycle:
    page: Page
    last_time: float


class BingAIPlayWright:
    browser: BrowserContext = None
    browser_context_manager = None

    def __init__(self, proxy: str = "", headless=False):
        self.proxy = proxy
        self.headless = headless
        self.timeout = 90
        self.page_lifecycle_time = 5 * 60
        # self.page.pause()
        self.pages: dict[str, PageLifeCycle] = {}

    async def init(self):
        if self.browser:
            return
        self.browser_context_manager = await async_playwright().start()
        self.browser = await self.browser_context_manager.chromium.launch_persistent_context(
            CHROME_DATA_DIR,
            headless=self.headless,
            base_url="https://www.bing.com",
            proxy={
                "server": self.proxy,
            } if self.proxy else None)
        return self

    async def new_page(self):
        return await self.browser.new_page()
        # p = await self.browser.new_page()
        # await p.goto("https://www.bing.com/chat?cc=us")

    async def check_page_lifecycle(self):
        closed_user_ids = []
        for user_id, page in self.pages.items():
            if time.time() - page.last_time > self.page_lifecycle_time:
                await page.page.close()
                closed_user_ids.append(user_id)

        for user_id in closed_user_ids:
            del self.pages[user_id]

    async def __get_page(self, user_id: str):
        if user_id in self.pages:
            task_page = self.pages[user_id]
            task_page.last_time = time.time()
            page = task_page.page
        else:
            page = await self.new_page()
            self.pages[user_id] = PageLifeCycle(page, time.time())
            await page.goto("https://www.bing.com/chat?cc=us", timeout=30000)
            for i in range(30):
                time.sleep(1)
                if await page.query_selector("textarea"):
                    break
            else:
                raise Exception("网络超时")

        return page

    async def send_msg(self, msg: str, uid: str):
        page = await self.__get_page(uid)
        if not await (await page.query_selector("textarea")).is_enabled():
            await page.click("button[aria-label='新主题']")
            await asyncio.sleep(1)
        await page.fill("textarea", msg)
        await page.click("div[class='control submit']")

    async def get_is_responding(self, uid: str) -> bool:
        page = await self.__get_page(uid)
        responding = await (await page.query_selector("#stop-responding-button")).is_enabled()
        return responding

    async def get_msg(self, uid: str):
        for i in range(self.timeout):
            await asyncio.sleep(1)
            if not (await self.get_is_responding(uid)):
                break
        else:
            return "网络超时了~"
        page = await self.__get_page(uid)
        # css选择器 选择ai的文本回复 "cib-message[source='bot'][type='text'] .ac-textBlock"
        replies = await page.query_selector_all("cib-message[source='bot'][type='text'] .ac-textBlock")
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

        async def check_need_reload():
            need_reload_ele = await page.query_selector("#giloadhelpc")
            if need_reload_ele:
                display = await need_reload_ele.evaluate("el => getComputedStyle(el).display")
                return display != "none"

        async def check_complete():
            create_btn = await page.query_selector("#create_btn_c")
            if await create_btn.inner_text() in ["Create", "创建"]:
                return True

        async def check_error() -> str:
            error_ele = await page.query_selector("#girer")
            if error_ele:
                return await error_ele.inner_text()
            return ""

        for i in range(60 * 5):
            await asyncio.sleep(1)
            if error := await check_error():
                await page.close()
                raise Exception(error)
            if await check_complete():
                break
            if await check_need_reload():
                await page.reload()
                await asyncio.sleep(3)
        else:
            await page.close()
            raise Exception("网络超时")

        gir = await page.query_selector("#gir_async")

        await gir.evaluate("""
                () => {
            var images = document.querySelectorAll('#gir_async img');

            function preLoad() {

                var promises = [];

                function loadImage(img) {
                    return new Promise(function(resolve,reject) {
                        if (img.complete) {
                            resolve(img)
                        }
                        img.onload = function() {
                            resolve(img);
                        };
                        img.onerror = function(e) {
                            resolve(img);
                        };
                    })
                }

                for (var i = 0; i < images.length; i++)
                {
                    promises.push(loadImage(images[i]));
                }

                return Promise.all(promises);
            }

            return preLoad();
        }
            """)

        path = tempfile.mktemp(suffix=".png")
        path = Path(path)
        await gir.screenshot(path=path)
        img_list = await gir.query_selector_all("img")
        img_urls = []
        for img in img_list:
            img_url = (await img.get_attribute("src")).split("?")[0]
            if img_url.endswith(".svg"):
                continue
            img_urls.append(img_url)
        await page.close()
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
    error_callback: Callable[[str], None] = None


class BinAITaskPool(threading.Thread):
    def __init__(self, proxy: str = "", headless=True):
        self.proxy = proxy
        self.headless = headless
        self.chat_concurrency = 1
        self.draw_concurrency = 5
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
                await bing.send_msg(chat_task.question, chat_task.user_id)
            except Exception as e:
                traceback.print_exc()
                reply_text = f"发生了错误：{e}"
            else:
                try:
                    reply_text = await bing.get_msg(chat_task.user_id)
                except Exception as e:
                    reply_text = f"网络错误：{e}"
            threading.Thread(target=chat_task.reply_callback, args=(reply_text,), daemon=True).start()

        async def handle_draw_task(draw_task: BingAIDrawTask):
            try:
                draw_resp = await bing.draw(draw_task.prompt)
            except Exception as draw_error:
                # traceback.print_exc()
                if draw_task.error_callback:
                    threading.Thread(target=draw_task.error_callback, args=(f"画图发生了错误：{draw_error}",),
                                     daemon=True).start()
                return
            else:
                threading.Thread(target=draw_task.reply_callback, args=(draw_resp,), daemon=True).start()

        async def listen_draw_task():
            while True:
                async_tasks = []
                for i in range(self.draw_concurrency):
                    if not self.draw_task_queue.empty():
                        t = self.draw_task_queue.get()
                        async_tasks.append(handle_draw_task(t))

                if async_tasks:
                    try:
                        await asyncio.gather(*async_tasks)
                    except Exception as e:
                        traceback.print_exc()
                await asyncio.sleep(1)

        async def listen_chat_task():
            while True:
                async_tasks = []
                for i in range(self.chat_concurrency):
                    if not self.chat_task_queue.empty():
                        t = self.chat_task_queue.get()
                        async_tasks.append(handle_chat_task(t))

                if async_tasks:
                    try:
                        await asyncio.gather(*async_tasks)
                    except Exception as e:
                        traceback.print_exc()
                await bing.check_page_lifecycle()
                await asyncio.sleep(1)

        async def run():
            await bing.init()
            await asyncio.gather(
                listen_draw_task(),
                listen_chat_task()
            )

        try:
            asyncio.run(run())
        except Exception as e:
            traceback.print_exc()
            print(e)


if __name__ == '__main__':
    test = BinAITaskPool(proxy="http://localhost:7890", headless=False)
    test.start()
    time.sleep(2)
    # test.put_task(BingAIChatTask("3", "hello", print))
    # time.sleep(2)
    # test.put_task(BingAIChatTask("1", "你好", print))
    # time.sleep(2)
    # test.put_task(BingAIChatTask("2", "你是谁", print))
    test.put_task(BingAIDrawTask("三只猫", print, print))
    # test.put_task(BingAIDrawTask("两只猫", print))
    test.join()
