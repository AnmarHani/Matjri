from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.http.response import HttpResponse
from django.shortcuts import render, redirect
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from UserAccount.models import Profile
from . import forms
from . import models
from django.core.paginator import Paginator, EmptyPage
from django.contrib.auth.decorators import login_required

    # for search:
    # def BlogSearch(request, title):
    # GetBlog = Blog.objects.all().filter(title__contains=title)

# Create your views here.
@login_required
def index(request):
    products = models.Product.objects.all().order_by('-likes')

    context = {
        'products': products
    }


#     def BlogList(request, page_num):
#   GetBlog = Blog.objects.all().order_by('-id')

#   p = Paginator(GetBlog, 10)
#   try:
#     page = p.page(page_num)
#   except EmptyPage:
#     page = p.page(1)
    return render(request,"Products/index.html", context)
@login_required
def productGetPage(request, id):
    product = models.Product.objects.get(id=id)
    likes = product.likes.all().count()
    product_seller_profile = product.seller.user_profile.id
    profile = Profile.objects.get(id=product_seller_profile)


    context = {
        'product':product,
        'likes':likes,
        'profile':profile
    }

    return render(request,"Products/productDetail.html", context)
    
@login_required
def productCreatePage(request):
    form = forms.ProductForm()
    product = models.Product()
    if request.method == "POST":
        form = forms.ProductForm(request.POST)
        if form.is_valid():
            if not request.FILES:
                product.seller = request.user
                product.title=request.POST['title'] 
                product.description=request.POST['description'] 
                product.stock=request.POST['stock'] 
                product.location=request.POST['location'] 
                product.price=request.POST['price'] 
                product.payment_type=request.POST['payment_type'] 
                product.delivery_type=request.POST['delivery_type'] 
            else:
                product.seller = request.user
                product.image = request.FILES['image']
                product.title=request.POST['title'] 
                product.description=request.POST['description'] 
                product.stock=request.POST['stock'] 
                product.location=request.POST['location'] 
                product.price=request.POST['price'] 
                product.payment_type=request.POST['payment_type'] 
                product.delivery_type=request.POST['delivery_type']  
            messages.success(request, "تم انشاء المنتج بنجاح!")
            product.save()
            return redirect('product_index')
        else:
            messages.error(request, "تأكد من صحة البيانات المدخلة!")

    context = {
        'form': form,
    }
    return render(request,"Products/createProduct.html", context)

@login_required
def productUpdatePage(request, id):
    product = models.Product.objects.get(id=id)
    form = forms.ProductForm()
    form['title'].initial = product.title
    form['description'].initial = product.description
    form['stock'].initial = product.stock
    form['location'].initial = product.location
    form['price'].initial = product.price
    form['payment_type'].initial = product.payment_type
    form['delivery_type'].initial = product.delivery_type
    if request.method == "POST":
        form = forms.ProductForm(request.POST)
        if form.is_valid():
            if request.user == product.seller:
                if not request.FILES:
                    product.title=request.POST['title'] 
                    product.description=request.POST['description'] 
                    product.stock=request.POST['stock'] 
                    product.location=request.POST['location'] 
                    product.price=request.POST['price'] 
                    product.payment_type=request.POST['payment_type'] 
                    product.delivery_type=request.POST['delivery_type'] 
                else:
                    product.image = request.FILES['image']
                    product.title=request.POST['title'] 
                    product.description=request.POST['description'] 
                    product.stock=request.POST['stock'] 
                    product.location=request.POST['location'] 
                    product.price=request.POST['price'] 
                    product.payment_type=request.POST['payment_type'] 
                    product.delivery_type=request.POST['delivery_type']  
                messages.success(request, "تم تعديل المنتج بنجاح!")
                product.save()
                return redirect(reverse('productGet', kwargs={"id": id}))
            else:
                messages.error(request, "انت لست البائع!")
        else:
            messages.error(request, "تأكد من صحة البيانات المدخلة!")

    context = {
        'form': form,
        'product':product
    }
    return render(request,"Products/updateProduct.html", context)
@login_required
def productDeletePage(request, id):
    product = models.Product.objects.get(id=id)
    if product.seller == request.user:
        product.delete()
    else:
        messages.error(request, "انت لست البائع!")
    return redirect('product_index')
@login_required
def productLikes(request, id):
    product = models.Product.objects.get(id=id)
    likes = product.likes.all()
    if request.user in likes:
        product.likes.remove(request.user)
        return redirect(reverse('productGet', kwargs={"id": id}))
    else:
        product.likes.add(request.user)
        return redirect(reverse('productGet', kwargs={"id": id}))

def notYet(request):
        
    return render(request,"Products/not_yet.html")

