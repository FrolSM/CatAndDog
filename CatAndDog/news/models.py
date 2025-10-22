from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse


class Users(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user


class Category(models.Model):
    name = models.CharField('Имя категории', max_length=30, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Post(models.Model):
    author = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    time = models.DateTimeField(auto_now_add=True)
    title = models.CharField(verbose_name='Заголовок', max_length=50)
    category = models.ForeignKey(Category, verbose_name='Категория', on_delete=models.CASCADE)
    text = models.TextField(verbose_name='Текст')
    photo = models.ImageField(upload_to='photos/%Y/%m/%d/', default=None, blank=True, null=True, verbose_name='Фото')
    video = models.FileField(upload_to='video/%Y/%m/%d/', default=None, blank=True, null=True, verbose_name='Видео')
    rating = models.IntegerField(default=0)

    def like(self):
        self.rating += 1
        self.save()

    # def dislike(self):
    #     self.rating -= 1
    #     self.save()

    def get_absolute_url(self):
        return reverse('post_detail', args=[str(self.id)])

    class Meta:
        verbose_name = 'Новость'
        verbose_name_plural = 'Новости'


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    text = models.TextField('Текст')
    time_comm = models.DateTimeField(auto_now_add=True)


class Pets(models.Model):
    name = models.CharField('Кличка', max_length=30, unique=True)
    age = models.IntegerField('Возраст')
    text = models.TextField('О питомце')
    photo = models.FileField('Фото')

    class Meta:
        verbose_name = 'Питомец'
        verbose_name_plural = 'Питомцы'

