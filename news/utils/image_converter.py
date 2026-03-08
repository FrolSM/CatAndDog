from PIL import Image
from io import BytesIO
from django.core.files.base import ContentFile
import os


def convert_to_webp(file):
    """
    Конвертирует изображение в формат WebP
    с уменьшением размера (thumbnail)
    """
    img = Image.open(file)

    # уменьшаем размер до 1200x1200 пикселей
    img.thumbnail((1200, 1200))

    # конвертируем в RGB (нужно для прозрачных PNG)
    if img.mode in ("RGBA", "P"):
        img = img.convert("RGB")

    # сохраняем в буфер
    buffer = BytesIO()
    img.save(buffer, format="WEBP", quality=80)

    # новое имя файла с .webp
    name = os.path.splitext(file.name)[0] + ".webp"

    return ContentFile(buffer.getvalue(), name=name)