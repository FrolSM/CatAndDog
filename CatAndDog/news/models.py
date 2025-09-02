from django_ckeditor_5.fields import CKEditor5Field
from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse


class Users(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user


class Category(models.Model):
    name = models.CharField(max_length=30, unique=True)

    def __str__(self):
        return self.name


class Post(models.Model):
    author = models.ForeignKey(Users, on_delete=models.CASCADE)
    time = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=50)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    text = CKEditor5Field()


    def get_absolute_url(self):
        return reverse('post_detail', args=[str(self.id)])


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    time_comm = models.DateTimeField(auto_now_add=True)


class Pets(models.Model):
    name = models.CharField(max_length=30, unique=True)
    age = models.DateTimeField()
    text = models.TextField()
    photo = CKEditor5Field()

