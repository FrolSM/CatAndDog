from django.db.models.signals import post_save, post_delete
from django.core.cache import cache
from django.dispatch import receiver
from .models import Post, PostMedia, Comment


# очищение кеша при сохранении или удалении объекта модели (отдельного поста или queryset)
@receiver([post_save, post_delete], sender=Post)
def cache_post(sender, instance, *args, **kwargs):
    cache.delete(f'post-{instance.slug}')
    cache.delete_pattern('post-queryset*')


@receiver([post_save, post_delete], sender=PostMedia)
def cache_post_media(sender, instance, *args, **kwargs):
    cache.delete(f'post-{instance.post.slug}')


@receiver([post_save, post_delete], sender=Comment)
def cache_comment(sender, instance, *args, **kwargs):
    cache.delete(f'post-{instance.post.slug}')