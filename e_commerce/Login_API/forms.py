from django.forms import ModelForm
from Login_API.models import User, Profile
from django.contrib.auth.forms import UserCreationForm
from django import forms


class ProfileForm(ModelForm):
    class Meta:
        model = Profile
        exclude = ('user',)

class SignUpForm(UserCreationForm):
    email = forms.EmailField(required = True, label = '', widget = forms.TextInput(attrs = {'placeholder' : 'Your Email'}))
    password1 = forms.CharField(required = True, label = '', widget = forms.PasswordInput(attrs = {'placeholder' : 'Your Password'}))
    password2 = forms.CharField(required = True, label = '', widget = forms.PasswordInput(attrs = {'placeholder' : 'Confirm Your Password'}))
    class Meta:
        model = User
        fields = ('email', 'password1', 'password2',)
