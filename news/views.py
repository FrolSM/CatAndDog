from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from django_filters.views import FilterView
from rest_framework.permissions import IsAdminUser
from rest_framework.viewsets import ModelViewSet
from .filters import PostFilter
from .models import *
from .forms import PostForm, CommentForm, PostMediaFormSet
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.core.cache import cache
from django.utils.http import urlencode
from .serializers import PostSerializer
from django.views.decorators.http import require_POST, require_GET


class PostsList(FilterView):
    model = Post
    context_object_name = 'posts'
    template_name = 'news/post_list.html'
    paginate_by = 5
    filterset_class = PostFilter
    cache_timeout = 120

    # кеширование набора записей (QuerySet) с учётом параметров запроса
    def get_queryset(self):
        params = self.request.GET.dict()
        cache_key = f'post-queryset-{urlencode(params)}' if params else 'post-queryset'

        queryset = cache.get(cache_key)
        if queryset is None:
            queryset = Post.published.all().order_by('-time').select_related('category', 'author')
            cache.set(cache_key, queryset, self.cache_timeout)

        return queryset

    # как работает фильтр(но в проекте ипользуем FilterView)
    # def get_queryset(self):
    #     queryset = super().get_queryset()
    #     self.post_filtered = PostFilter(self.request.GET, queryset=queryset)
    #     return self.post_filtered.qs
    #
    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context['filter'] = self.post_filtered
    #     return context


class PostDetail(DetailView):
    model = Post
    template_name = 'news/post.html'
    context_object_name = 'post'
    cache_timeout = 120
    slug_field = 'slug'
    slug_url_kwarg = 'slug'

    # кеширование одного поста
    def get_object(self, *args, **kwargs):
        obj = cache.get(f'post-{self.kwargs["slug"]}', None)
        if not obj:
            obj = super().get_object(queryset=self.queryset)
            cache.set(f'post-{self.kwargs["slug"]}', obj, self.cache_timeout)
        return obj


class PostCreate(UserPassesTestMixin, CreateView):
    form_class = PostForm
    model = Post
    template_name = 'news/post_create_or_update.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['create_or_edit'] = 'Добавление'

        if self.request.POST:
            context['media_formset'] = PostMediaFormSet(
                self.request.POST, self.request.FILES, queryset=PostMedia.objects.none()
            )
        else:
            context['media_formset'] = PostMediaFormSet(queryset=PostMedia.objects.none())

        return context

    def test_func(self):
        return self.request.user.groups.filter(name='authors').exists()

    def form_valid(self, form):
        context = self.get_context_data()
        media_formset = context['media_formset']

        form.instance.author = self.request.user
        response = super().form_valid(form)

        if media_formset.is_valid():
            for media_form in media_formset:
                if media_form.cleaned_data and not media_form.cleaned_data.get('DELETE', False):
                    PostMedia.objects.create(
                        post=self.object,
                        media_type=media_form.cleaned_data['media_type'],
                        file=media_form.cleaned_data['file']
                    )
        return response


class PostUpdate(UserPassesTestMixin, UpdateView):
    form_class = PostForm
    model = Post
    template_name = 'news/post_create_or_update.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['create_or_edit'] = 'Редактирование'

        if self.request.POST:
            context['media_formset'] = PostMediaFormSet(
                self.request.POST, self.request.FILES, queryset=self.object.media.all()
            )
        else:
            context['media_formset'] = PostMediaFormSet(queryset=self.object.media.all())

        return context

    def test_func(self):
        return self.get_object().author == self.request.user or self.request.user.is_staff

    def form_valid(self, form):
        context = self.get_context_data()
        media_formset = context['media_formset']

        response = super().form_valid(form)

        if media_formset.is_valid():
            # Сохраняем новые файлы и удаляем отмеченные
            for media_form in media_formset:
                if media_form.cleaned_data:
                    if media_form.cleaned_data.get('DELETE', False):
                        if media_form.instance.pk:
                            media_form.instance.delete()
                    elif not media_form.instance.pk:
                        PostMedia.objects.create(
                            post=self.object,
                            media_type=media_form.cleaned_data['media_type'],
                            file=media_form.cleaned_data['file']
                        )

        return response


class PostDelete(UserPassesTestMixin, DeleteView):
    model = Post
    template_name = 'news/post_delete.html'
    success_url = reverse_lazy('post_list')

    def test_func(self):
        return self.request.user.is_staff


class ContactsView(TemplateView):
    template_name = 'news/contacts.html'


class PetsList(ListView):
    model = Pets
    context_object_name = 'pets'
    template_name = 'news/pets.html'


class PostComment(LoginRequiredMixin, CreateView):
    model = Comment
    form_class = CommentForm
    template_name = 'news/comment.html'

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.author_comm = self.request.user
        self.object.post = get_object_or_404(Post, slug=self.kwargs['slug'])
        self.object.save()
        return redirect(self.get_success_url())

    def get_success_url(self):
        return reverse_lazy('post_detail', kwargs={'slug': self.object.post.slug})


class UpdateComment(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Comment
    form_class = CommentForm
    template_name = 'news/comment_update.html'

    def test_func(self):
        return self.get_object().author_comm == self.request.user or self.request.user.is_staff

    def get_object(self, queryset=None):
        return get_object_or_404(
            Comment,
            pk=self.kwargs['pk'],
            post__slug=self.kwargs['slug']
        )

    def get_success_url(self):
        return self.get_object().post.get_absolute_url()


@require_POST
@login_required
def like_post(request, slug):
    post = get_object_or_404(Post, slug=slug)
    like, created = Like.objects.get_or_create(user=request.user, post=post)
    if not created:
        like.delete()  # если лайк уже был — удаляем (toggle)
    return JsonResponse({
        'liked': created,
        'count': post.like_count()
    })


@require_GET
def get_like_count(request, slug):
    post = get_object_or_404(Post, slug=slug)
    return JsonResponse({'count': post.like_count()})


class RulesCreatingPostView(TemplateView):
    template_name = 'news/rules_creating_post.html'


class PostViewSet(ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = (IsAdminUser,)
    filterset_fields = ('author', 'category', 'is_published')

    def perform_create(self, serializer):
        post = serializer.save(author=self.request.user)
        for f in self.request.FILES.getlist('photos'):
            PostMedia.objects.create(post=post, media_type='photo', file=f)
        for f in self.request.FILES.getlist('videos'):
            PostMedia.objects.create(post=post, media_type='video', file=f)

    def perform_update(self, serializer):
        post = serializer.save()
        for f in self.request.FILES.getlist('photos'):
            PostMedia.objects.create(post=post, media_type='photo', file=f)
        for f in self.request.FILES.getlist('videos'):
            PostMedia.objects.create(post=post, media_type='video', file=f)
