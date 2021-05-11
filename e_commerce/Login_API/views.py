from django.shortcuts import render, HttpResponseRedirect
from django.urls import reverse
from django.http import HttpResponse

from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate

from Login_API.models import Profile
from Login_API.forms import ProfileForm, SignUpForm

# Messages
from django.contrib import messages


def sign_up(request):
    form = SignUpForm()
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Account Created Successfully')
            return HttpResponseRedirect(reverse('Login_API:login'))
    return render(request, 'Login_API/signup.html', context = {'form' : form})


def log_in(request):
    form = AuthenticationForm()
    if request.method == 'POST':
        form = AuthenticationForm(data = request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username = username, password = password)
            if user is not None:
                login(request, user)
                return HttpResponse('Logged in')
    return render(request, 'Login_API/login.html', context = {'form' : form})


@login_required
def log_out(request):
    logout(request)
    messages.warning(request, 'Logged Out')
    return HttpResponse('Logged out')


@login_required
def user_profile(request):
    profile = Profile.objects.get(user = request.user)
    form = ProfileForm(instance = profile)

    if request.method == 'POST':
        form = ProfileForm(request.POST, instance = profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile Updated Successfully')
            form = ProfileForm(instance = profile)

    return render(request, 'Login_API/change_profile.html', context = {'form' : form})
