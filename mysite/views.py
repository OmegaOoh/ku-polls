from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from .form import UserRegisterForm
from django.contrib.messages import error


def signup(request):
    """Register a new user."""
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            # get named fields from the form data
            username = form.cleaned_data.get('username')
            # password input field is named 'password1'
            raw_passwd = form.cleaned_data.get('password1')
            email = form.cleaned_data.get('email')
            user = authenticate(username=username,password=raw_passwd, email=email)
            login(request, user)
            return redirect('polls:index')
        else:
            error(request, 'Invalid Form')
    else:
        # create a user form and display it the signup page
        form = UserRegisterForm()
    return render(request, 'registration/signup.html', {'form': form})