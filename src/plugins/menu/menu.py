import base64
from pathlib import Path

from nonebot import get_loaded_plugins
from playwright.async_api import async_playwright

from src.common import DATA_DIR
from src.plugins.menu.ignore import ignore_plugin_ids

cur_dir = Path(__file__).parent
menu_image_path = DATA_DIR / 'menu.png'
menu_bg_image_path = cur_dir / 'bg.jpg'
header_image_path = cur_dir / 'header.jpg'
footer_image_path = cur_dir / 'footer.jpg'

template_path = cur_dir / 'template.html'


def read_img_base64(path: Path) -> str:
    img_b64 = base64.b64encode(path.read_bytes()).decode('utf8')
    img_b64 = f'data:image/jpg;base64,{img_b64}'
    return img_b64


def create_menu_item(name: str, desc: str, usage: str, color_index: int) -> str:
    template = f'''
        <div class="menuItem">
            <div class="itemLeft itemLeftColor{color_index}">{name}</div>
            <div class="itemRight itemRightColor{color_index}">
                <div class="description">
                    <label class="descriptionLabel">插件介绍：</label>{desc}
                </div>
                <div class="usage">
                    <label class="usageLabel">指令用法：</label>{usage}
                </div>
            </div>
        </div>
    '''
    return template


def get_plugins():
    plugins = get_loaded_plugins()
    plugins = sorted(plugins, key=lambda x: x.metadata.name if x.metadata else x.id_)
    plugins = [plugin for plugin in plugins if plugin.metadata and plugin.id_ not in ignore_plugin_ids]
    return plugins


def generate_menu():
    template_text = template_path.read_text(encoding='UTF8')
    header_img_b64 = read_img_base64(header_image_path)
    template_text = template_text.replace('{{header_img}}', header_img_b64)
    bg_img_b64 = read_img_base64(menu_bg_image_path)
    template_text = template_text.replace('{{bg_img}}', bg_img_b64)
    footer_img_b64 = read_img_base64(footer_image_path)
    template_text = template_text.replace('{{footer_img}}', footer_img_b64)

    menu_text = ''
    plugins = get_plugins()
    for index, plugin in enumerate(plugins):
        color_index = index % 4 + 1
        plugin_name = plugin.metadata.name
        plugin_description = plugin.metadata.description.replace('\n', '<br>')
        plugin_usage = plugin.metadata.usage.replace('\n', '<br>')
        menu_text += create_menu_item(plugin_name, plugin_description, plugin_usage, color_index)

    template_text = template_text.replace('{{menu_items}}', menu_text)
    # Path(DATA_DIR / 'menu.html').write_text(template_text, encoding='UTF8')
    return template_text


async def generate_image():
    html = generate_menu()
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(viewport={"width": 600, "height": 600})
        page = await context.new_page()
        await page.set_content(html)
        # await page.screenshot(path=menu_image_path)
        await (await page.query_selector('body')).screenshot(path=menu_image_path)
