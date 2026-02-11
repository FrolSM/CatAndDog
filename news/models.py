from django.db import models
from django.urls import reverse
from autoslug import AutoSlugField


class PublishedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_published=Post.Status.PUBLISHED)


class Category(models.Model):
    name = models.CharField('Имя категории', max_length=30, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Post(models.Model):
    class Status(models.IntegerChoices):
        DRAFT = 0, 'Черновик'
        PUBLISHED = 1, 'Опубликовано'

    author = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    time = models.DateTimeField(verbose_name='Время создания', auto_now_add=True)
    title = models.CharField(verbose_name='Заголовок', max_length=100, unique=True)
    category = models.ForeignKey(Category, verbose_name='Категория', on_delete=models.CASCADE)
    text = models.TextField(verbose_name='Содержание')
    is_published = models.BooleanField(verbose_name='Статус',
                                       choices=tuple(map(lambda x: (bool(x[0]), x[1]), Status.choices)),
                                       default=Status.PUBLISHED)
    slug = AutoSlugField(editable=False, populate_from='title', unique=True, always_update=True)

    objects = models.Manager()
    published = PublishedManager()

    def like_count(self):
        return self.like_set.count()

    def get_absolute_url(self):
        return reverse('post_detail', kwargs={'slug': self.slug})

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Новость'
        verbose_name_plural = 'Новости'

    @property
    def has_photo(self):
        return self.media.filter(media_type='photo').exists()

    @property
    def has_video(self):
        return self.media.filter(media_type='video').exists()


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    author_comm = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    text = models.TextField('Текст')
    time_comm = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Коментарий'
        verbose_name_plural = 'Коментарии'

    def __str__(self):
        return self.text


class Pets(models.Model):
    name = models.CharField('Кличка', max_length=30, unique=True)
    age = models.IntegerField('Возраст')
    text = models.TextField('О питомце')
    photo = models.FileField('Фото')

    class Meta:
        verbose_name = 'Питомец'
        verbose_name_plural = 'Питомцы'


class Like(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'post')  # один пользователь — один лайк на пост

    def __str__(self):
        return f"{self.user.username} likes {self.post.title}"


class PostMedia(models.Model):
    class MediaType(models.TextChoices):
        PHOTO = 'photo', 'Фото'
        VIDEO = 'video', 'Видео'

    post = models.ForeignKey(Post, related_name='media', on_delete=models.CASCADE)  # related_name позволяет обращаться post.media.all()
    media_type = models.CharField(max_length=5, choices=MediaType.choices)
    file = models.FileField(upload_to='posts/%Y/%m/%d/')
    order = models.PositiveIntegerField(default=0)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('order',)

    def __str__(self):
        return f"{self.post.title} {self.media_type}"
