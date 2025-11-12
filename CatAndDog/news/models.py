from django.db import models
from django.urls import reverse
from django.utils.text import slugify


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
    time = models.DateTimeField(auto_now_add=True)
    title = models.CharField(verbose_name='Заголовок', max_length=100)
    category = models.ForeignKey(Category, verbose_name='Категория', on_delete=models.CASCADE)
    text = models.TextField(verbose_name='Содержание')
    photo = models.ImageField(upload_to='photos/%Y/%m/%d/', default=None, blank=True, null=True, verbose_name='Добавить фото')
    video = models.FileField(upload_to='video/%Y/%m/%d/', default=None, blank=True, null=True, verbose_name='Добавить видео')
    is_published = models.BooleanField(choices=Status.choices, default=Status.DRAFT)
    slug = models.SlugField(unique=True, db_index=True, blank=True, max_length=100)

    objects = models.Manager()
    published = PublishedManager()

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.title)
            self.slug = base_slug
            # Проверяем уникальность
            while Post.objects.filter(slug=self.slug).exists():
                self.slug = f"{base_slug}-{Post.objects.filter(slug__startswith=base_slug).count() + 1}"
        super().save(*args, **kwargs)

    def like_count(self):
        return self.like_set.count()

    def get_absolute_url(self):
        return reverse('post_detail', kwargs={'slug': self.slug})

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
