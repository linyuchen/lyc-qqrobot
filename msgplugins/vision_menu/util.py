from pathlib import Path
from tempfile import mktemp

import fitz

from PIL import Image
from fitz import Document
from reportlab.lib.pagesizes import A3
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.platypus import Table, TableStyle, SimpleDocTemplate, Spacer

from common.stringplus import split_lines


pdfmetrics.registerFont(
    TTFont('zh', Path(__file__).parent.parent.parent / "common" / "fonts" / "仓耳舒圆体.ttf"))


def create_menu_image(data: list[list[str, str, str]]) -> Path:
    for line in data:
        desc = line[1]
        example = line[2]
        desc_new = []
        for desc_line in desc.splitlines():
            desc_new.append("\n".join(split_lines(desc_line, 10)))
        line[1] = "\n".join(desc_new)
        example_new = []
        for example_line in example.splitlines():
            example_new.append("\n".join(split_lines(example_line, 10)))
        line[2] = "\n".join(example_new)

    pdf_path = Path(mktemp(suffix=".pdf"))
    # c = canvas.Canvas(str(pdf_path), pagesize=letter)
    c = SimpleDocTemplate(str(pdf_path), pagesize=A3, topMargin=5, bottomMargin=0)
    # c.setFont("zh", 18)

    data = [['命令', '说明', '示例']] + data

    # table = Table(data)

    style = TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.whitesmoke),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),  # 设置表格内容垂直居中
        ('FONT', (0, 0), (-1, -1), 'zh', 22),
        ('PADDING', (0, 0), (-1, -1), 20),
        # ('BACKGROUND', (0, 0), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)])
    # table.setStyle(style)

    # table.wrapOn(c, 0, 0)
    # table.drawOn(c, 100, 100)
    elements = []
    for i in range(0, len(data), 80):
        part_of_data = data[i:i + 80]
        tbl = Table(part_of_data)
        tbl.setStyle(style)
        elements.append(tbl)

    c.build(elements)

    doc = fitz.open(str(pdf_path))
    image_paths = []
    for page in doc:
        pix = page.get_pixmap()
        image_path = mktemp(suffix=".png")
        pix.save(image_path)
        image_paths.append(image_path)
    menu_image_path = Path(__file__).parent / "menu.png"
    # 多张图片合成一张图片
    image_list = [Image.open(i) for i in image_paths]
    image_width, image_height = image_list[0].size
    total_width = image_width
    total_height = image_height * len(image_list)
    new_image = Image.new('RGBA', (total_width, total_height), (255, 255, 255, 50))
    y_offset = 0
    for im in image_list:
        new_image.paste(im, (0, y_offset))
        y_offset += im.size[1]
    bg_image = Image.open(Path(__file__).parent / "bg.png").convert('RGBA')
    bg_image = bg_image.resize((total_width, total_height))
    # 创建一个相同尺寸的透明图层
    transparent_layer = Image.new('RGBA', bg_image.size, (255, 255, 255, 0))  # 完全透明

    # 混合背景图像和透明图层
    alpha = 0.2  # 设置透明度系数，例如0.5（可以根据需要调整）
    blended_image = Image.blend(new_image, transparent_layer, alpha)

    # 将混合后的图像粘贴到new_image上
    bg_image.paste(blended_image, (0, 0), blended_image)
    bg_image.save(menu_image_path)
    # bg_image.paste(new_image, (0, 0), new_image)
    # bg_image.save(menu_image_path)

    return menu_image_path


if __name__ == '__main__':
    test_data = [['画图', 'AI画图大森撒看阿龙\n但凡阿是扥收到', '画图 一只会飞的喵\n画图xxxx']] * 50
    p = create_menu_image(test_data)
    print(p)
