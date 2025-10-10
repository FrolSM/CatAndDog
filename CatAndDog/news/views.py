from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import *
from .forms import PostForm
from django.shortcuts import render, get_object_or_404
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
