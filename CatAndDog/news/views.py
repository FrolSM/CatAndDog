from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django_filters.views import FilterView
from .filters import PostFilter
from .models import *
from .forms import PostForm, CommentForm
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin


class PostsList(FilterView):
    model = Post
    ordering = '-time'
    context_object_name = 'posts'
    template_name = 'news/post_list.html'
    paginate_by = 1
    filterset_class = PostFilter

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


class PostCreate(UserPassesTestMixin, CreateView):
    form_class = PostForm
    model = Post
    template_name = 'news/post_create.html'

    def test_func(self):
        return self.request.user.groups.filter(name='authors').exists()

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostUpdate(UpdateView):
    form_class = PostForm
    model = Post
    template_name = 'news/post_update.html'


class PostDelete(DeleteView):
    model = Post
    template_name = 'news/post_delete.html'


def contacts(request):
    return render(request, 'news/contacts.html')


class PetsList(ListView):
    model = Pets
    context_object_name = 'pets'
    template_name = 'news/pets.html'


def like(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.like()
    post.save()
    return render(request, 'news/post.html', {'post': post})

# def dislike(request, pk):
#     post = get_object_or_404(Post, pk=pk)
#     post.dislike()
#     post.save()
#     return render(request, 'flatpages/post.html', {'post': post})


class PostComment(LoginRequiredMixin, CreateView):
    form_class = CommentForm
    model = Comment
    template_name = 'news/comment.html'

    def form_valid(self, form):
        comment = form.save(commit=False)
        comment.user = self.request.user
        comment.post = Post.objects.get(pk=self.kwargs['pk'])
        comment.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('post_detail', kwargs={'pk': self.kwargs['pk']})
