from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django_filters.views import FilterView
from .filters import PostFilter
from .models import *
from .forms import PostForm, CommentForm
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.core.cache import cache


class PostsList(FilterView):
    model = Post
    # ordering = '-time'
    context_object_name = 'posts'
    template_name = 'news/post_list.html'
    paginate_by = 5
    filterset_class = PostFilter

    def get_queryset(self):
        return Post.published.all().order_by('-time')

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

    def get_object(self, *args, **kwargs):

        obj = cache.get(f'post-{self.kwargs["slug"]}', None)
        if not obj:
            obj = super().get_object(queryset=self.queryset)
            cache.set(f'post-{self.kwargs["slug"]}', obj)

        return obj


class PostCreate(UserPassesTestMixin, CreateView):
    form_class = PostForm
    model = Post
    template_name = 'news/post_create_or_update.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['create_or_edit'] = 'Добавление' if self.request.path == '/post/create/' else 'Редактирование'
        return context

    def test_func(self):
        return self.request.user.groups.filter(name='authors').exists()

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostUpdate(UpdateView):
    form_class = PostForm
    model = Post
    template_name = 'news/post_create_or_update.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['create_or_edit'] = 'Добавление' if self.request.path == '/post/create/' else 'Редактирование'
        return context


class PostDelete(DeleteView):
    model = Post
    template_name = 'news/post_delete.html'


def contacts(request):
    return render(request, 'news/contacts.html')


class PetsList(ListView):
    model = Pets
    context_object_name = 'pets'
    template_name = 'news/pets.html'


class PostComment(LoginRequiredMixin, CreateView):
    model = Comment
    form_class = CommentForm
    template_name = 'news/comment.html'

    def form_valid(self, form):
        comment = form.save(commit=False)
        comment.user = self.request.user
        comment.post = Post.objects.get(pk=self.kwargs['pk'])
        comment.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('post_detail', kwargs={'slug': self.object.post.slug})


@login_required
def like_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    like, created = Like.objects.get_or_create(user=request.user, post=post)
    if not created:
        like.delete()  # если лайк уже был — удаляем (toggle)
    return JsonResponse({
        'liked': created,
        'count': post.like_count()
    })


def get_like_count(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    return JsonResponse({'count': post.like_count()})


def rules_creating_post(request):
    return render(request, 'news/rules_creating_post.html')
