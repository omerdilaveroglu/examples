from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, logout,login,update_session_auth_hash
from django.contrib import messages
from account.froms import LoginUserForm, NewUserForm
from django.contrib.auth.forms import PasswordChangeForm

# Create your views here.

def login_request(request):

    if request.user.is_authenticated:
        return redirect("products")

    if request.method == "POST":
        form = LoginUserForm(request,data = request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(request,username=username,password=password)
        
            if user is not None:
                login(request,user)
                return redirect("products")
            else:
                return render(request,"account/login.html",{'form':form})
        else:
            return render(request,"account/login.html",{'form':form})
    else:
        form = LoginUserForm()
        return render(request,"account/login.html",{'form':form})

def register_request(request):
    if request.method == "POST":
        form = NewUserForm(request.POST)

        if form.is_valid():
            form.save()

            username = form.cleaned_data["username"]
            password = form.cleaned_data["password1"]
            user = authenticate(username=username,password=password)
            login(request,user)
            return redirect("login")
        else:
            return render(request,"account/register.html",{"form":form})
    form = NewUserForm()
    return render(request,"account/register.html",{"form":form})

def logout_request(request):
    logout(request)
    messages.success(request,"Uygulamadan çıkıldı.")
    return redirect("products")


def change_password(request):
    if request.method =="POST":
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request,user)
            messages.success(request,"parola değiştirildi.")
            return redirect("change_password")
        else:
            return render(request,"account/change_password.html",{"form":form})
        
    form = PasswordChangeForm(request.user)
    return render(request,"account/change_password.html",{"form":form})