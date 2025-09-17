from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import *
from .forms import PostForm
from django.urls import reverse_lazy
from django.shortcuts import render
from django.contrib.auth.mixins import UserPassesTestMixin


class PostsList(ListView):
    model = Post
    ordering = '-time'
    context_object_name = 'posts'
    template_name = 'news/post_list.html'
    # paginate_by = 10


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
