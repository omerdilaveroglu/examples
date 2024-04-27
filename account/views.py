from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login

# Create your views here.


def login_request(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]

        user = authenticate(
            request=request, username=username, password=password)
        
        if user is not None:
            login(request=request,user=user)
            return redirect("products")
        else:
            return render(request,"account/login.html",{
                "error": "kullanıcı adı veya parola hatalı"
            })

    elif request.method == "GET":
        return render(request, "account/login.html")


def register_request(request):
    if request.method == "POST":
        # login
        pass
    elif request.method == "GET":
        return render(request, "account/register.html")


def logout_request(request):
    return redirect("products")
