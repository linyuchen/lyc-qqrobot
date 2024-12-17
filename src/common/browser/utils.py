from asyncio import sleep
from playwright.async_api import Page


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
    await sleep(result * 0.2)
