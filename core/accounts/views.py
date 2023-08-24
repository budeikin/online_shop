from django.shortcuts import render, get_object_or_404, reverse
from .forms import RegisterForm, LoginForm, EditUserInformation, EditUserProfile, LoginWithPhoneForm, VerifyCodeForm
from django.contrib.auth.models import User
from django.shortcuts import redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import Profile
from django.views.generic import TemplateView
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from random import randint
import ghasedakpack
from django.core.mail import EmailMessage, send_mail
from django.views import View
from django.utils.encoding import force_text, force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from six import text_type
from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy


# from django.contrib.auth.mixins import LoginRequiredMixin


# Create your views here.

class EmailToken(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return (text_type(user.is_active) + text_type(user.id) + text_type(timestamp))


email_generator = EmailToken()


@login_required(login_url='accounts:login')
def profile(reqeust):
    profile = Profile.objects.get(user_id=reqeust.user.id)
    return render(reqeust, 'accounts/profile.html', context={'profile': profile})


class ActivateAccountView(View):
    def get(self, request, uidb64, token):
        id = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(id=id)
        if user and email_generator.check_token(user, token):
            user.is_active = True
            user.save()
            return redirect('accounts:login')


def register(request):
    if request.method == "POST":
        register_form = RegisterForm(request.POST)
        if register_form.is_valid():
            email = register_form.cleaned_data.get('email')
            username = register_form.cleaned_data.get('username')
            first_name = register_form.cleaned_data.get('first_name')
            last_name = register_form.cleaned_data.get('last_name')
            password = register_form.cleaned_data.get('password')

            user = User.objects.create_user(email=email, username=username, first_name=first_name, last_name=last_name,
                                            )
            user.is_active = False
            user.set_password(password)
            user.save()
            domain = get_current_site(request).domain
            uidb64 = urlsafe_base64_encode(force_bytes(user.id))
            url = reverse('accounts:activate', kwargs={'uidb64': uidb64, 'token': email_generator.make_token(user)})
            link = 'http://' + domain + url
            send_mail('actiation account', link, 'budeikin52@gmail.com', [email])
            messages.success(request, 'email sent successfully')
            return redirect('home:home-page')
    else:
        register_form = RegisterForm()

    return render(request, 'accounts/register_page.html', context={'form': register_form})


def login_page(request):
    if request.method == "POST":
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            data = login_form.cleaned_data
            try:
                user = authenticate(request, username=User.objects.get(email=data['username']),
                                    password=data['password'])
            except:
                user = authenticate(request, username=data['username'], password=data['password'])
            if user is not None:
                login(request, user)
                messages.success(request, 'You have successfully logged in', 'success')
                return redirect('home:home-page')
            else:
                messages.warning(request, 'something is wrong', 'danger')
    else:
        login_form = LoginForm()
    return render(request, 'accounts/login_page.html', context={'form': login_form})


def logout_page(request):
    logout(request)
    messages.success(request, 'You have successfully logged out')
    return redirect('home:home-page')


# def profile_page(request):
#     # user = get_object_or_404(Profile,user=request.user)
#     profile = Profile.objects.get(user_id=request.user.id)
#     return render(request, 'accounts/profile.html', context={'profile': profile})

@login_required(login_url='accounts:login')
def profile_update(request):
    if request.method == 'POST':
        user_form = EditUserInformation(request.POST, instance=request.user)
        profile_form = EditUserProfile(request.POST, request.FILES, instance=request.user.profile)
        if user_form and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Information changed successfully', 'success')
            return redirect('accounts:profile')
    else:
        user_form = EditUserInformation(instance=request.user)
        profile_form = EditUserProfile(instance=request.user.profile)

    return render(request, 'accounts/profile_update.html',
                  context={'user_form': user_form, 'profile_form': profile_form})


@login_required(login_url='accounts:login')
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, request.user)
            messages.success(request, 'password successfully changed', 'success')
            return redirect('accounts:profile')
        else:
            messages.error(request, 'information is not valid', 'danger')
            return redirect('accounts:change-password')
    else:
        form = PasswordChangeForm(user=request.user)
    return render(request, 'accounts/change_password.html', context={'form': form})


def login_number(request):
    if request.method == 'POST':
        form = LoginWithPhoneForm(request.POST)
        if form.is_valid():
            global random_code, number
            number = f"{form.cleaned_data['phone_number']}"
            random_code = randint(1000000, 9999999)
            sms = ghasedakpack.Ghasedak("d165bb71994dff32c84e6b0fd4a7c3100171a50881ea0e0690d7bba392de3f14")
            sms.send({
                'message': random_code,
                'receptor': number,
                'linenumber': '10008566'
            })
            return redirect('accounts:login-phone-verify')

    else:
        form = LoginWithPhoneForm()
    return render(request, 'accounts/login_number.html', context={'form': form})


def login_number_verify(request):
    if request.method == 'POST':
        form = VerifyCodeForm(request.POST)
        if form.is_valid():
            if random_code == form.cleaned_data['code']:
                profile = Profile.objects.get(phone_number=number)
                user = User.objects.get(profile__id=profile.id)
                login(request, user)
                messages.success(request, 'welcome', 'success')
                return redirect('home:home-page')
            else:
                messages.success(request, 'code is wrond')
        else:
            messages.success(request, 'form is not valid', 'danger')
    else:
        form = VerifyCodeForm()
    return render(request, 'accounts/verify_code.html', context={'form': form})


class CustomResetPasswordView(auth_views.PasswordResetView):
    template_name = 'accounts/reset_password.html'
    success_url = reverse_lazy('accounts:done-reset-password')
    email_template_name = 'accounts/link.html'


class DoneResetPassword(auth_views.PasswordResetDoneView):
    template_name = 'accounts/done_reset_password.html'


class ConfirmResetPassword(auth_views.PasswordResetConfirmView):
    template_name = 'accounts/confirm_reset_password.html'
    success_url = reverse_lazy('accounts:done-confirm-reset-password')


class DoneConfirmResetPassword(auth_views.PasswordResetCompleteView):
    template_name = 'accounts/reset_password_complete.html'
