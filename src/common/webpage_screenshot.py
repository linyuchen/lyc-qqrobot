import asyncio
import tempfile
import time
from contextlib import asynccontextmanager
from pathlib import Path
from urllib.parse import quote

from PIL import Image
from playwright.async_api import async_playwright, Page

from src.common import DATA_DIR

CHROME_DATA_DIR = DATA_DIR / "playwright_screenshot"


@asynccontextmanager
async def new_page(url: str, proxy: str = "", headless=True) -> Page:
    async with async_playwright() as p:
        browser = await p.chromium.launch_persistent_context(CHROME_DATA_DIR, headless=headless, proxy={
            "server": proxy,
        } if proxy else None, viewport={"width": 1920, "height": 1080})
        page = await browser.new_page()
        try:
            await page.goto(url, timeout=30000)
        except Exception as e:
            error_msg = f"{e}"
            pass
        yield page
        await page.close()
        await browser.close()


async def load_all(page: Page):
    result = await page.evaluate("""
        for(let i = 0; i <= document.body.scrollHeight; i+=500){
            setTimeout(function(){
                window.scrollTo(0, i);
                if (i >= (document.body.scrollHeight - 500)){

                    window.scrollTo(0, 0);
                }
            }, 200 * (i/500))
        }
        result = document.body.scrollHeight / 500
    """)
    time.sleep(result * 0.2)


def merge_images(img_paths: list[Path]) -> Path:
    imgs = [Image.open(img_path) for img_path in img_paths]
    width = max([img.size[0] for img in imgs])
    height = sum([img.size[1] for img in imgs])
    merged_img = Image.new("RGB", (width, height), (255, 255, 255))
    y = 0
    for img in imgs:
        merged_img.paste(img, (0, y))
        y += img.size[1]
    merged_path = Path(tempfile.mktemp(suffix=".png"))
    merged_img.save(merged_path)
    return merged_path


async def screenshot_search_baidu(keyword: str) -> Path:
    keyword = quote(keyword.encode("utf8"))

    url = f"https://www.baidu.com/s?wd={keyword}"
    async with new_page(url) as page:
        e = page.locator("css=#content_left")
        await e.evaluate("""
        e = document.getElementById("content_left")
        e.style.paddingLeft = "10px";
        e.style.paddingRight = "10px";
        document.getElementById("head").style.display="none";
        try{
            document.getElementById("searchTag").style.display="none";
        }catch{}
        """)
        path = Path(tempfile.mktemp(suffix=".png"))
        await e.screenshot(path=path)
        await page.close()
        return path


async def screenshot_github_readme(url: str, http_proxy: str = "") -> Path | None:
    async with new_page(url, http_proxy, headless=True) as page:
        e = page.locator("css=.markdown-body")
        if e.count() == 0:
            return None
        await e.evaluate(
            """
            let readme = document.getElementsByClassName("markdown-body")[0]
            readme.style.padding = "40px";
            let nav = document.querySelector("nav[aria-label='Repository files']")
            nav.parentElement.remove()
            """
        )
        path = Path(tempfile.mktemp(suffix=".png"))
        await e.screenshot(path=path)
        await page.close()
        return path


class ZhihuPreviewer:

    @staticmethod
    async def hidden_elements(page: Page):
        await page.evaluate(
            """
            let closeLoginBtn = document.getElementsByClassName("Modal-closeButton")[0]
            if (closeLoginBtn){
                closeLoginBtn.click()
            }
            let e = document.getElementsByClassName("ContentItem-actions");
            for (let i = 0; i < e.length; i++) {
                e[i].style.display = "none";
                //e[i].remove()
            }

            """
        )

    async def screenshot_zhihu_question(self, url: str) -> Path | None:
        async with new_page(url, headless=False) as page:
            await self.hidden_elements(page)
            question = page.locator("css=.QuestionHeader .QuestionHeader-main")
            if question.count() == 0:
                return None
            question = question.first

            question_path = Path(tempfile.mktemp(suffix=".png"))
            await question.screenshot(path=question_path)
            time.sleep(1)

            answer = page.locator("css=.AnswerItem")
            if answer.count() == 0:
                return None
            answer = answer.first
            await answer.evaluate(
                """
                e = document.getElementsByClassName("AnswerItem")[0]
                e.style.paddingLeft = "30px";
                """
            )
            answer_path = Path(tempfile.mktemp(suffix=".png"))
            await answer.screenshot(path=answer_path)

            # 合并图片
            merged_path = merge_images([question_path, answer_path])
            await page.close()
            question_path.unlink()
            answer_path.unlink()
            return merged_path

    async def screenshot_zhihu_zhuanlan(self, url: str) -> Path | None:

        async with new_page(url, headless=False) as page:
            await self.hidden_elements(page)
            await load_all(page)
            author = page.locator("css=.Post-Header")
            if author.count() == 0:
                return None
            author_path = Path(tempfile.mktemp(suffix=".png"))
            await author.screenshot(path=author_path)

            content = page.locator("css=.Post-RichTextContainer")
            if not content.count():
                return None
            await content.evaluate(
                """
                e = document.getElementsByClassName("Post-RichTextContainer")[0]
                e.style.paddingTop = "50px";
                e.style.paddingLeft = "10px";
                e.style.paddingRight = "20px";
                """
            )

            content_path = Path(tempfile.mktemp(suffix=".png"))
            await content.screenshot(path=content_path)

            merged_path = merge_images([author_path, content_path])
            await page.close()
            author_path.unlink()
            content_path.unlink()
            return merged_path

    @staticmethod
    async def login():
        try:
            async with new_page("https://www.zhihu.com/signin", headless=False) as page:
                input("登录知乎后按回车")
        except Exception as e:
            error = e
            print(e)


async def screenshot_moe_wiki(keyword: str) -> Path | None:
    async with new_page(f"https://zh.moegirl.org.cn/{keyword}") as page:
        close_btn = page.locator("css=.n-base-close.n-base-close--absolute.n-card-header__close")
        if await close_btn.count() > 0:
            await close_btn.first.click()
            time.sleep(1)
        await load_all(page)
        content = await page.query_selector("#mw-content-text")
        if not content:
            return
        await content.evaluate(
            """
            e = document.getElementById("mw-content-text")
            e.style.paddingLeft = "40px";
            e.style.paddingRight = "40px";
            """
        )
        path = Path(tempfile.mktemp(suffix=".png"))
        await content.screenshot(path=path)
        await page.close()
        return path


async def screenshot_wx_article(url: str) -> Path | None:
    async with new_page(url) as page:
        content = page.locator("css=#img-content")
        if content.count() == 0:
            return
        await load_all(page)
        await content.evaluate(
            """
            e = document.getElementById("img-content")
            e.style.paddingLeft = "40px";
            e.style.paddingRight = "40px";
            """
        )
        path = Path(tempfile.mktemp(suffix=".png"))
        await content.screenshot(path=path)
        await page.close()
        return path


if __name__ == '__main__':
    asyncio.run(ZhihuPreviewer().login())

