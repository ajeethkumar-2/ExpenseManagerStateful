from django.contrib.auth import views as auth_views
from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import *



class LoginView(auth_views.LoginView):
    form_class = LoginForm
    template_name = 'registration/login.html'
    success_url = 'home'


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(request, email=user.email, password=raw_password)
            if user is not None:
                messages.success(request, 'Account Created Successfully')
                login(request, user)
            else:
                print("user is not authenticated")
            return redirect('home')
    else:
        form = SignUpForm()
    return render(request, 'registration/signup.html', {'form': form})
