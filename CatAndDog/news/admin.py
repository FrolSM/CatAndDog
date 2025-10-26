from django.contrib import admin
from .models import Post, Category, Pets, Comment


admin.site.register(Post)
admin.site.register(Category)
admin.site.register(Pets)
admin.site.register(Comment)
