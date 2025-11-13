from django.urls import path
from .views import *

urlpatterns = [
    path('', PostsList.as_view(), name='post_list'),
    path('post/create/', PostCreate.as_view(), name='post_create'),
    path('post/<slug:slug>/', PostDetail.as_view(), name='post_detail'),
    path('contacts/', contacts, name='contacts'),
    path('pets/', PetsList.as_view(), name='pets_list'),
    path('<int:pk>/comment/', PostComment.as_view(), name='post_comment'),
    path('post/<int:post_id>/like/', like_post, name='like_post'),
    path('post/<int:post_id>/count/', get_like_count, name='get_like_count'),
    path('rules/', rules_creating_post, name='rules_creating_post'),
]
