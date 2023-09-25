import tempfile
import time
from pathlib import Path
from urllib.parse import quote
from contextlib import contextmanager

from PIL import Image
from playwright.sync_api import sync_playwright, Page

CHROME_DATA_DIR = tempfile.gettempdir() + "/playwright_chrome_data"


@contextmanager
def new_page(url: str) -> Page:
    with sync_playwright() as p:
        browser = p.chromium.launch_persistent_context(CHROME_DATA_DIR, headless=False)
        page = browser.new_page()
        try:
            page.goto(url, timeout=30000)
        except Exception as e:
            error_msg = f"{e}"
            pass
        yield page
        page.close()
        browser.close()


# with new_page("https://www.zhihu.com/signin") as page:
#     input("登录知乎后按回车")


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


def search_baidu(keyword: str) -> Path:
    keyword = quote(keyword.encode("utf8"))

    url = f"https://www.baidu.com/s?wd={keyword}"
    with new_page(url) as page:
        e = page.locator("css=#content_left")
        e.evaluate("""
        e = document.getElementById("content_left")
        e.style.paddingLeft = "10px";
        e.style.paddingRight = "10px";
        document.getElementById("head").style.display="none";
        try{
            document.getElementById("searchTag").style.display="none";
        }catch{}
        """)
        path = Path(tempfile.mktemp(suffix=".png"))
        e.screenshot(path=path)
        page.close()
        return path


def github_readme(url: str) -> Path | None:
    with new_page(url) as page:
        e = page.locator("css=#readme")
        if e.count() == 0:
            return None
        path = Path(tempfile.mktemp(suffix=".png"))
        e.screenshot(path=path)
        page.close()
        return path


class ZhihuPreviewer:

    @staticmethod
    def hidden_elements(page: Page):
        # 隐藏赞数栏
        result = page.evaluate("""
            for(let i = 0; i <= document.body.scrollHeight; i+=500){
                setTimeout(function(){
                    window.scrollTo(0, i);
                    if (i >= (document.body.scrollHeight - 500)){
                        e = document.getElementsByClassName("ContentItem-actions");
                        for (let i = 0; i < e.length; i++) {
                            e[i].style.display = "none";
                            //e[i].remove()
                        }
                        window.scrollTo(0, 0);
                    }
                }, 200 * (i/500))
            }
            result = document.body.scrollHeight / 500
        """)
        time.sleep(result * 0.2)

    def zhihu_question(self, url: str) -> Path | None:
        with new_page(url) as page:
            self.hidden_elements(page)
            question = page.locator("css=.QuestionHeader .QuestionHeader-main")
            if question.count() == 0:
                return None
            question = question.first

            question_path = Path(tempfile.mktemp(suffix=".png"))
            question.screenshot(path=question_path)
            time.sleep(1)

            answer = page.locator("css=.QuestionAnswer-content")
            if answer.count() == 0:
                return None
            answer_path = Path(tempfile.mktemp(suffix=".png"))
            answer.screenshot(path=answer_path)

            # 合并图片
            merged_path = merge_images([question_path, answer_path])
            page.close()
            question_path.unlink()
            answer_path.unlink()
            return merged_path

    def zhihu_zhuanlan(self, url: str) -> Path | None:

        with new_page(url) as page:
            self.hidden_elements(page)
            author = page.locator("css=.Post-Header")
            if author.count() == 0:
                return None
            author_path = Path(tempfile.mktemp(suffix=".png"))
            author.screenshot(path=author_path)

            content = page.locator("css=.Post-RichTextContainer")
            if not content.count():
                return None
            content.evaluate(
                """
                e = document.getElementsByClassName("Post-RichTextContainer")[0]
                e.style.paddingTop = "50px";
                e.style.paddingLeft = "10px";
                e.style.paddingRight = "20px";
                """
            )

            content_path = Path(tempfile.mktemp(suffix=".png"))
            content.screenshot(path=content_path)

            merged_path = merge_images([author_path, content_path])
            page.close()
            author_path.unlink()
            content_path.unlink()
            return merged_path
