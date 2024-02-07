from django.shortcuts import render, redirect
from .forms import UserRegisterForm
from django.contrib.auth import authenticate, login
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
