from django.urls import path
from .views import IndexView
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('', IndexView.as_view(), name='profile'),
    path('logout/', LogoutView.as_view(template_name='sign/logout.html'), name='logout'),
]
