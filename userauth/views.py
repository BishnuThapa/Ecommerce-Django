from django.shortcuts import render, redirect
from .forms import UserRegisterForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
# Create your views here.


def register_view(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST or None)
        # print('User registered.')
        if form.is_valid():
            new_user = form.save()
            # to display message in admin panel
            username = form.cleaned_data.get("username")
            messages.success(
                request, f"Hey {username}, Your account created successfully!")

            # to authenticate after registration
            new_user = authenticate(
                username=form.cleaned_data['email'], password=form.cleaned_data['password1'])
            login(request, new_user)
            return redirect("core:index")
    else:
        form = UserRegisterForm()
        # print('User cannot be registered.')
    context = {
        'form': form

    }
    return render(request, 'userauth/sign-up.html', context)


def login_view(request):
    if request.user.is_authenticated:
        return redirect('core:index')

    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        try:
            user = User.objects.get(email=email)
        except:
            messages.warning(request, f'User with {email} doesn\'t exists.')
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, 'You are logged in.')
            return redirect('core:index')
        else:
            messages.warning(
                request, f'User Does not exist. Create an account.')
    return render(request, 'userauth/sign-in.html')


def logout_view(request):
    logout(request)
    return redirect('userauth:sign-in')
