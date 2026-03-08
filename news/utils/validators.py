from django.core.exceptions import ValidationError

def validate_media_type(file):
    """Проверка формата файла"""
    valid = ('.jpg', '.jpeg', '.png', '.webp', '.mp4', '.webm')
    if not file.name.lower().endswith(valid):
        raise ValidationError("Unsupported file format")


def validate_file_size(file):
    """Проверка размера файла"""
    max_photo = 5 * 1024 * 1024  # 5 MB для фото
    max_video = 30 * 1024 * 1024  # 30 MB для видео

    ext = file.name.lower().split('.')[-1]
    if ext in ('jpg', 'jpeg', 'png', 'webp') and file.size > max_photo:
        raise ValidationError("Photo size must be <= 5 MB")
    if ext in ('mp4', 'webm') and file.size > max_video:
        raise ValidationError("Video size must be <= 30 MB")