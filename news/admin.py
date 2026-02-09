from django.contrib import admin, messages
from django.utils.safestring import mark_safe

from .models import Post, Category, Pets, Comment, PostMedia


class PostMediaInline(admin.TabularInline):
    """
    Inline позволяет добавлять фото и видео
    прямо на странице редактирования поста
    """
    model = PostMedia
    extra = 1


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    """
    Админка для модели Post
    """
    fields = ('title', 'text', 'category')  # поля формы создания и редакции
    list_display = ('id', 'title', 'media_preview', 'is_published', 'category')  # поля отображаемые в списке объектов
    list_display_links = ('id', 'title')  # поля линк
    ordering = ['-time', 'title']  # сортировка
    list_editable = ('is_published',)  # разрешение редактировать прям на странице списка
    list_per_page = 10  # пагинация
    actions = ('set_published', 'set_draft')  # доп действия
    list_filter = ('category', 'is_published')  # фильтрация по полям
    readonly_fields = ('media_preview',)  # поля неизменяемое (видное в форме)
    inlines = (PostMediaInline,)
    exclude = ('author',)

    def save_model(self, request, obj, form, change):
        """
            Назначаем автора автоматически
            только при создании поста
            """
        if not change:  # Только при создании новой записи
            obj.author = request.user
        super().save_model(request, obj, form, change)

    @admin.display(description='Медиа')
    def media_preview(self, obj):
        """
        Отображение фото и видео в админке
        """
        html = []

        for media in obj.media.all():
            if media.media_type == PostMedia.MediaType.PHOTO:
                html.append(
                    f'<img src="{media.file.url}" '
                    f'width="100" style="margin:5px;" />'
                )
            else:
                html.append(
                    f'''
                            <video width="160" height="100" controls style="margin:5px;">
                                <source src="{media.file.url}" type="video/mp4">
                                Ваш браузер не поддерживает видео
                            </video>
                            '''
                )

        return mark_safe(''.join(html) or 'Нет медиа')


    @admin.action(description='Опубликовать выбранные записи')
    def set_published(self, request, queryset):
        count = queryset.update(is_published=Post.Status.PUBLISHED)
        self.message_user(request, f'Изменено {count} записей')

    @admin.action(description='Снять с публикации выбранные записи')
    def set_draft(self, request, queryset):
        count = queryset.update(is_published=Post.Status.DRAFT)
        self.message_user(request, f'{count} записей снято с публикации', messages.WARNING)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('id', 'name')


@admin.register(Pets)
class PetsAdmin(admin.ModelAdmin):
    list_display = ('name', 'age')
    search_fields = ('name',)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'post', 'user', 'time_comm')
    list_filter = ('post',)
