from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import *


class PostsList(ListView):
    model = Post
    ordering = '-time'
    context_object_name = 'posts'
    # paginate_by = 10


class PostDetail(DetailView):
    model = Post
    template_name = 'flatpages/post.html'
    context_object_name = 'post'


