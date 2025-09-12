from django.urls import path
from .views import IndexView
from django.contrib.auth.views import LogoutView
from .views import upgrade_me

urlpatterns = [
    path('', IndexView.as_view(), name='profile'),
    path('logout/', LogoutView.as_view(template_name='sign/logout.html'), name='logout'),
    path('upgrade/', upgrade_me, name='upgrade')
]
