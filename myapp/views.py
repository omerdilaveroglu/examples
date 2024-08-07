from django.http.response import Http404, HttpResponseNotFound, HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from .models import Product
from .froms import ProductForm
from django.contrib.auth.decorators import login_required
import random
import os


def index(request):
    products = Product.objects.filter(isActive=True).order_by("-price")

    context = {
        "products": products,
    }

    return render(request, 'myapp/index.html', context)

@login_required(login_url='/account/login')
def list(request):
    if 'search_name' in request.GET and request.GET.get('search_name'):
        q = request.GET['search_name']
        products = Product.objects.filter(name__contains=q).order_by("-price")
    else:
        products = Product.objects.all().order_by("-price")

    context = {
        "products": products,
    }

    return render(request, 'myapp/list.html', context)

@login_required(login_url='/account/login')
def create(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)

        if form.is_valid():
            form.save()
            return redirect("product_list")
    else:
        form = ProductForm()

    return render(request, "myapp/create.html", {
        "form": form
    })


def edit(request, id):
    product = get_object_or_404(Product, pk=id)

    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES, instance=product)

        if form.is_valid():
            form.save()
            return redirect("product_list")

    else:
        form = ProductForm(instance=product)

    return render(request, "myapp/edit.html", {
        "form": form
    })


def delete(request, id):
    product = get_object_or_404(Product, pk=id)

    if request.method == "POST":
        product.delete()
        return redirect("product_list")

    return render(request, "myapp/delete-confirm.html", {
        "product": product
    })


def details(request, slug):

    product = get_object_or_404(Product, slug=slug)

    context = {
        "product": product
    }
    return render(request, "myapp/details.html", context)


# def handle_uploaded_file(file):
#     number = random.randint(10000, 99999)
#     fileName, file_extension = os.path.splitext(file.name)
#     name = fileName+"_"+str(number)+file_extension

#     with open("temp/"+name, "wb+") as destination:
#         for chunk in file.chunks():
#             destination.write(chunk)


# def upload(request):

#     if request.method == "POST":
#         form = UploadForm(request.POST, request.FILES)

#         if form.is_valid():
#             model = UploadModel(image= request.FILES["image"])
#             model.save()
#             return render(request, 'success.html')
#     else:
#         form = UploadForm()

#     return render(request, "upload.html",{
#         "form": form
#     })
