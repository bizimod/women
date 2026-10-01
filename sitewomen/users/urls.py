from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    path('login/', views.LoginUser.as_view(), name='login'),  # users:login
    path('logout/', views.logout_user, name='logout'),  # users:login
]

