from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, logout,login
from django.contrib.auth.models import User
from django.contrib import messages

# Create your views here.


def login_request(request):

    if request.user.is_authenticated:
        return redirect("products")

    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]

        user = authenticate(request=request, username=username, password=password)
        
        if user is not None:
            login(request=request,user=user)
            nextUrl = request.GET.get('next',None)
            print(nextUrl)
            if nextUrl is None:
                messages.success(request,"login başarılı")
                return redirect('products')
            else:
                return redirect(nextUrl)
        else:
            messages.error(request,"kullanıcı adı veya parola hatalı")
            return render(request,"account/login.html")

    elif request.method == "GET":
        return render(request, "account/login.html")


def register_request(request):
    if request.method == "POST":
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        repassword = request.POST['repassword']

        if password == repassword:
            if User.objects.filter(username = username).exists():
                return render(request, "account/register.html",{"error":"username kullanılıyor."})
            else:
                if User.objects.filter(email = email).exists():
                    return render(request, "account/register.html",{"error":"email kullanılıyor."})
                else:
                    user = User.objects.create_user(username==username,email=email,password=password)
                    user.save()
                    return redirect("login")
        else:
            return render(request, "account/register.html",{"error":"parola eşleşmiyor."})

    elif request.method == "GET":
        return render(request, "account/register.html")


def logout_request(request):
    logout(request)
    messages.success(request,"Uygulamadan çıkıldı.")
    return redirect("products")
