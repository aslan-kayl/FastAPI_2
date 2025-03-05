import base64
import os
from uuid import uuid4


def save_image_from_base64(base64_string: str, output_dir: str = "static/images") -> str:
    # Если строка содержит префикс типа "data:image/png;base64,...", извлекаем MIME-тип и данные
    if "," in base64_string:
        header, base64_data = base64_string.split(",", 1)
        # Пример header: "data:image/png;base64"
        if "image/" in header:
            mime = header.split(";")[0].split("/")[1]  # например, "png" или "svg+xml"
            # Если MIME содержит "+xml", можно задать соответствующее расширение
            if "+xml" in mime:
                ext = mime.split("+")[0]
            else:
                ext = mime
        else:
            ext = "png"
    else:
        base64_data = base64_string
        ext = "png"

    # Декодируем base64 в байты
    image_data = base64.b64decode(base64_data)

    # Генерируем уникальное имя файла с правильным расширением
    filename = f"{uuid4().hex}.{ext}"

    # Убеждаемся, что директория существует
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Полный путь к файлу
    filepath = os.path.join(output_dir, filename)

    # Сохраняем изображение
    with open(filepath, "wb") as f:
        f.write(image_data)

    return filepath
