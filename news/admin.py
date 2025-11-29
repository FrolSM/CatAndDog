from django.contrib import admin
from .models import Post, Category, Pets, Comment


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}


admin.site.register(Category)
admin.site.register(Pets)
admin.site.register(Comment)
