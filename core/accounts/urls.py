from django.urls import path
from .views import register, login_page, logout_page, profile, profile_update, change_password, login_with_phone_number

app_name = 'accounts'

urlpatterns = [
    path('register/', register, name='register'),
    path('login/', login_page, name='login'),
    path('login_with_phone_number/', login_with_phone_number, name='login-phone'),
    path('logout/', logout_page, name='logout'),
    path('profile/', profile, name='profile'),
    path('profile/edit/', profile_update, name='edit-profile'),
    path('profile/change-pass/', change_password, name='change-password'),
]
