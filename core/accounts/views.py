from django.shortcuts import render
from .forms import RegisterForm
from django.contrib.auth.models import User
from django.shortcuts import redirect



# Create your views here.

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
