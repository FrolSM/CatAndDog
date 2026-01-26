from celery import shared_task
from django.utils import timezone
from datetime import timedelta
from django.core.mail import send_mail
from django.contrib.auth import get_user_model

from .models import Post

User = get_user_model()


@shared_task
def weekly_posts_digest():
    week_ago = timezone.now() - timedelta(days=7)

    posts_count = Post.objects.filter(
        time__gte=week_ago
    ).count()

    if posts_count == 0:
        return "Нет новых постов"

    recipients = User.objects.filter(
        is_active=True,
        email__isnull=False
    ).values_list("email", flat=True)

    send_mail(
        subject="Еженедельная сводка",
        message=f"За последнюю неделю опубликовано постов: {posts_count}",
        from_email=None,
        recipient_list=list(recipients),
        fail_silently=False,
    )

    return f"Отправлено писем: {len(recipients)}"
