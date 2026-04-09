import os
import subprocess
from django.core.files.base import ContentFile


def convert_video(file, output_format="mp4", max_width=1280, max_height=720):
    """
    Конвертирует видео в нужный формат (mp4/webm)
    и уменьшает разрешение для экономии места
    """
    # исходный путь
    input_path = file.temporary_file_path() if hasattr(file, 'temporary_file_path') else file.file.name

    # новое имя
    base, ext = os.path.splitext(file.name)
    output_name = f"{base}.{output_format}"

    # временный путь для ffmpeg
    tmp_output = f"/tmp/{os.path.basename(output_name)}"

    # ffmpeg команда
    # -y: перезаписывать без вопроса
    # -vf scale: уменьшение размера
    # -c:v libx264: кодек H.264
    command = [
        "ffmpeg",
        "-i", input_path,
        "-vf", f"scale='min({max_width},iw)':'min({max_height},ih)':force_original_aspect_ratio=decrease",
        "-c:v", "libx264",
        "-preset", "fast",
        "-crf", "23",  # качество 0-51, меньше — лучше качество
        "-c:a", "aac",
        "-b:a", "128k",
        "-y",
        tmp_output
    ]

    subprocess.run(command, check=True)

    # читаем результат и создаем ContentFile для Django
    with open(tmp_output, "rb") as f:
        content = ContentFile(f.read(), name=output_name)

    # удаляем временный файл
    os.remove(tmp_output)

    return content