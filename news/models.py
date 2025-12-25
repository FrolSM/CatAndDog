from django.db import models
from django.urls import reverse
from autoslug import AutoSlugField
from unidecode import unidecode


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
    photo = models.ImageField(upload_to='photos/%Y/%m/%d/', default=None, blank=True, null=True, verbose_name='Добавить фото')
    video = models.FileField(upload_to='video/%Y/%m/%d/', default=None, blank=True, null=True, verbose_name='Добавить видео')
    is_published = models.BooleanField(verbose_name='Статус', choices=tuple(map(lambda x: (bool(x[0]), x[1]), Status.choices)),
                                       default=Status.PUBLISHED)
    slug = AutoSlugField(editable=False, populate_from='title', unique=True, always_update=True)

    objects = models.Manager()
    published = PublishedManager()

    # def save(self, *args, **kwargs):
    #     if self.title and not self.slug:
    #         self.slug = unidecode(self.title)
    #     super().save(*args, **kwargs)

    def like_count(self):
        return self.like_set.count()

    def get_absolute_url(self):
        return reverse('post_detail', kwargs={'slug': self.slug})

    def is_liked_by(self, user):
        return self.likes.filter(user=user).exists()

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Новость'
        verbose_name_plural = 'Новости'


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
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
