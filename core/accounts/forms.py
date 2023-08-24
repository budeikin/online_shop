from django import forms
from django.contrib.auth.models import User
from .models import Profile
from django.contrib.auth.password_validation import validate_password


class RegisterForm(forms.Form):
    username = forms.CharField(max_length=255, widget=forms.TextInput(attrs={'placeholder': 'enter username'}))
    email = forms.EmailField()
    first_name = forms.CharField(max_length=50)
    last_name = forms.CharField(max_length=50)
    password = forms.CharField(max_length=50, widget=forms.PasswordInput())
    confirm_password = forms.CharField(max_length=50, widget=forms.PasswordInput())

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError('this user already exists')
        return username

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('this email already has been saved')
        return email

    def clean_confirm_password(self):
        password1 = self.cleaned_data.get('password')
        password2 = self.cleaned_data.get('confirm_password')
        if password2 == password1:
            try:
                validate_password(password1)
            except forms.ValidationError as error:
                self.add_error('password', error)
            return password1

        else:
            raise forms.ValidationError(
                "password and confirm_password does not match"
            )


class LoginForm(forms.Form):
    username = forms.CharField(max_length=50, label='username or email')
    password = forms.CharField(max_length=50, widget=forms.PasswordInput())


class EditUserInformation(forms.ModelForm):
    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name']


class EditUserProfile(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['phone_number', 'address', 'avatar']


class LoginWithPhoneForm(forms.Form):
    phone_number = forms.IntegerField()

    # def clean_phone_number(self):
    #     phone_num = self.cleaned_data.get('phone_number')
    #     if len(phone_num) < 11:
    #         return ValueError('phone number must has 11 number')
    #     return phone_num


class VerifyCodeForm(forms.Form):
    code = forms.IntegerField()
