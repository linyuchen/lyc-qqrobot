from pathlib import Path
from tempfile import mktemp

from PIL import Image
from fitz import Document
from reportlab.lib.pagesizes import letter
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.platypus import Table, TableStyle, SimpleDocTemplate, Spacer

import fitz


pdfmetrics.registerFont(
    TTFont('zh', Path(__file__).parent.parent.parent / "common" / "fonts" / "仓耳今楷01-9128-W05.ttf"))


def create_menu_image(data: list[list[str, str, str]]) -> Path:
    pdf_path = Path(mktemp(suffix=".pdf"))
    # c = canvas.Canvas(str(pdf_path), pagesize=letter)
    c = SimpleDocTemplate(str(pdf_path), pagesize=letter, topMargin=5, bottomMargin=0)
    # c.setFont("zh", 18)

    data = [['命令', '说明', '示例']] + data

    # table = Table(data)

    style = TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.whitesmoke),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONT', (0, 0), (-1, -1), 'zh', 22),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        # ('BACKGROUND', (0, 0), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)])
    # table.setStyle(style)

    # table.wrapOn(c, 0, 0)
    # table.drawOn(c, 100, 100)
    elements = []
    for i in range(0, len(data), 40):
        part_of_data = data[i:i + 40]
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
    new_image = Image.new('RGBA', (total_width, total_height))
    y_offset = 0
    for im in image_list:
        new_image.paste(im, (0, y_offset))
        y_offset += im.size[1]
    new_image.save(menu_image_path)

    return menu_image_path


if __name__ == '__main__':
    test_data = [['画图', 'AI画图大森撒扥看阿龙\n但凡阿是扥收到', '画图 一只会飞的喵\n画图xxxx']] * 50
    p = create_menu_image(test_data)
    print(p)
