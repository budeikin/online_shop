from django.urls import path
from .views import register, login_page, logout_page, ProfileView

app_name = 'accounts'

urlpatterns = [
    path('register/', register, name='register'),
    path('login/', login_page, name='login'),
    path('logout/', logout_page, name='logout'),
    path('profile/', ProfileView.as_view(), name='profile'),
]
