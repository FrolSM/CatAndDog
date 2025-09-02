from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import *
from .forms import PostForm
from django.urls import reverse_lazy


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


class PostCreate(CreateView):
    form_class = PostForm
    model = Post
    template_name = 'news/post_create.html'


class PostUpdate(UpdateView):
    form_class = PostForm
    model = Post
    template_name = 'news/post_update.html'


class PostDelete(DeleteView):
    model = Post
    template_name = 'news/post_delete.html'

