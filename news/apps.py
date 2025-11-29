from django.apps import AppConfig


class NewsConfig(AppConfig):
    verbose_name = 'app news'
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'news'

    def ready(self):
        import news.signals
