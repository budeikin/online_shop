from django.urls import path
from .views import register, login_page, logout_page, profile, profile_update, change_password, login_number, \
    login_number_verify, ActivateAccountView, CustomResetPasswordView, DoneResetPassword, ConfirmResetPassword, \
    DoneConfirmResetPassword, favorite_products,history

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
    path('reset_pass/', CustomResetPasswordView.as_view(), name='reset-password'),
    path('reset_pass/done/', DoneResetPassword.as_view(), name='done-reset-password'),
    path('confirm/<uidb64>/<token>/', ConfirmResetPassword.as_view(), name='confirm-reset-password'),
    path('confirm/done/', DoneConfirmResetPassword.as_view(), name='done-confirm-reset-password'),
    path('favorite_products/', favorite_products, name='favorite_products'),
    path('history/', history, name='history'),
]
