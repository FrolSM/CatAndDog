from django.urls import path
from .views import *

urlpatterns = [
    path('', PostsList.as_view(), name='post_list'),
    path('post/<int:pk>/', PostDetail.as_view(), name='post_detail'),
    path('post/create/', PostCreate.as_view(), name='post_create'),
    path('contacts/', contacts, name='contacts'),
    path('pets/', PetsList.as_view(), name='pets_list'),
    path('<int:pk>/like/', like, name='like'),
    # path('<int:pk>/dislike/', dislike, name='dislike'),
]
