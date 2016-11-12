from django.shortcuts import render
from django.views.generic import View
from django.shortcuts import render,render_to_response,redirect
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from .forms import LoginForm
# Create your views here.
def login_view(request):
    form=LoginForm(request.POST or None)
    next_url=request.GET.get('next')
    if form.is_valid():
        username=form.cleaned_data.get('username')
        password=form.cleaned_data.get('password')
        next_url=request.POST.get('next')
        user=authenticate(username=username, password=password)
        if user is not None:
            login(request,user)
            if next_url:
                return redirect(next_url)
            else:
                return redirect('dashboard')
    if bool(request.session.keys()):
        return redirect('dashboard')
    return render(request,'registration/login.html',{'form':form,'next':next_url })
