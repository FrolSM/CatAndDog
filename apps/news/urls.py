from django.urls import path
from .views import *

urlpatterns = [
    path('', PostsList.as_view(), name='post_list'),
    path('post/create/', PostCreate.as_view(), name='post_create'),
    path('post/<slug:slug>/', PostDetail.as_view(), name='post_detail'),
    path('contacts/', ContactsView.as_view(), name='contacts'),
    path('pets/', PetsList.as_view(), name='pets_list'),
    path('post/<slug:slug>/comment/', PostComment.as_view(), name='post_comment'),
    path('post/<slug:slug>/like/', like_post, name='like_post'),
    path('post/<slug:slug>/count/', get_like_count, name='get_like_count'),
    path('rules_creating_post/', RulesCreatingPostView.as_view(), name='rules_creating_post'),
    path('post/<slug:slug>/update/', PostUpdate.as_view(), name='post_update'),
    path('post/<slug:slug>/delete/', PostDelete.as_view(), name='post_delete'),
    path('post/<slug:slug>/comment/<int:pk>/update/', UpdateComment.as_view(), name='post_comment_update'),
    path('post/<slug:slug>/comment/<int:pk>/delete/', DeleteComment.as_view(), name='comment_delete'),
]
