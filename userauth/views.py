from django.shortcuts import render
from .forms import UserRegisterForm
# Create your views here.
def register_view(request):
    if request.method=='POST':
        pass
    form= UserRegisterForm()
    context={
        'form':form

    }
    return render(request,'userauth/sign-up.html',context)