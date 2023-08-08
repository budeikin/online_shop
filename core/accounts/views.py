from django.shortcuts import render, get_object_or_404
from .forms import RegisterForm, LoginForm, EditUserInformation, EditUserProfile
from django.contrib.auth.models import User
from django.shortcuts import redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import Profile
from django.views.generic import TemplateView


# Create your views here.
class ProfileView(TemplateView):
    template_name = 'accounts/profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['profile'] = Profile.objects.get(user_id=self.request.user.id)
        return context


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

            user.set_password(password)
            user.save()

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


def profile_update(request):
    if request.method == 'POST':
        user_form = EditUserInformation(request.POST, instance=request.user)
        profile_form = EditUserInformation(request.POST, instance=request.user.profile)
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
