from django.urls import path
from .views import register, login_page, logout_page, profile, profile_update, change_password, login_number, \
    login_number_verify, ActivateAccountView

app_name = 'accounts'

urlpatterns = [
    path('register/', register, name='register'),
    path('activate/<uidb64>/<token>/', ActivateAccountView.as_view(), name='activate'),
    path('login/', login_page, name='login'),
    path('login_number/', login_number, name='login-phone'),
    path('login_verify/', login_number_verify, name='login-phone-verify'),
    path('logout/', logout_page, name='logout'),
    path('profile/', profile, name='profile'),
    path('profile/edit/', profile_update, name='edit-profile'),
    path('profile/change-pass/', change_password, name='change-password'),
]
