from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.http.response import HttpResponse
from django.shortcuts import render, redirect
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from . import forms
from . import models

# Create your views here.
def home(request):
    return render(request,"home.html")

@login_required
def index(request):
    users = models.Profile.objects.all().order_by("-followers")
    context ={
        'users':users
    }
    return render(request,"UserAccount/index.html", context)
    
def registerPage(request):
    form = forms.CreateUserForm()
    
    if request.method == "POST":
        form = forms.CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "تم التسجيل بنجاح!")
            return redirect('login') #url name
        else:
            messages.error(request, "تأكد من صحة البيانات المدخلة!")
            return redirect('register') #url name

    context = {
        'form': form,
    }
    return render(request, 'UserAccount/userRegister.html', context)


def loginPage(request):
    form = forms.LoginForm()
    if request.method == "POST":
        form = forms.LoginForm(request.POST)
        if form.is_valid():
            username= request.POST['username']
            password= request.POST['password']
            
            user = authenticate(request, 
                                username=username, 
                                password=password)
            if user is not None:
                login(request, user) #django built in
                if user.user_profile.description:
                    return redirect('product_index')
                else:
                    return redirect('createProfile')
            else:
                messages.error(request, "كلمة المرور او اسم المستخدم غير صحيح!")
        else:
            messages.error(request, "تأكد من صحة البيانات المدخلة!")
    context = {
        'form': form,
    }

    
    return render(request,"UserAccount/userLogin.html", context)
@login_required
def logoutUser(request):
    logout(request)
    messages.success(request, "تم تسجيل الخروج بنجاح!")
    return redirect('login')

def userCreateProfile(request):
    realProfile = models.Profile.objects.get(username=request.user)
    form = forms.ProfileForm()
    if request.method == "POST":
        form = forms.ProfileForm(request.POST, request.FILES)
        if form.is_valid():
            if(realProfile == request.user.user_profile):
                # profile = models.Profile(
                #     image=request.FILES['image'],
                #     description=request.POST['description']
                # )
                # profile.save()
                if not request.FILES:
                    realProfile.description=request.POST['description'] 
                else:
                    realProfile.image = request.FILES['image']
                    realProfile.description=request.POST['description'] 
                realProfile.save()
                messages.success(request, "تم انشاء المتجر بنجاح!")
                return redirect(reverse('userProfile', kwargs={"id": realProfile.id}))
        else:
            messages.error(request, "تأكد من صحة البيانات المدخلة!")
    context = {
        'form': form,
    }
    return render(request,"UserAccount/userCreateProfile.html", context)
    
@login_required
def userProfile(request, id):
    profile = models.Profile.objects.get(id=id)
    followers = profile.followers.all().count()
    products = profile.username.seller.all()
    context = {
        'profile':profile,
        "followers":followers,
        'products':products
    }
    return render(request,"UserAccount/userProfile.html", context)
@login_required
def userFollow(request, id):
    Followed_user = models.Profile.objects.get(id=id)
    followers = Followed_user.followers.all() #Bring All Likes For This Blog
    if request.user in followers:
        Followed_user.followers.remove(request.user)
        return redirect(reverse('userProfile', kwargs={"id": id}))
    else:
        Followed_user.followers.add(request.user)
        return redirect(reverse('userProfile', kwargs={"id": id}))