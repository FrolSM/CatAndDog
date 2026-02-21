from django.urls import path
from .views import IndexView
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('profile/', IndexView.as_view(), name='profile'),
    path('logout/', LogoutView.as_view(template_name='users/logout.html'), name='logout'),
]
