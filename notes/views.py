from django.contrib import messages

from django.shortcuts import render, redirect
from notes import models

def home(request):
    return render(request,"home.html")

from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate
def login(request):
    if request.method=="POST":
        email=request.POST.get('email')
        password=request.POST.get('password')
        res=models.user.objects.filter(email=email,password=password)
        if res:
            if res[0].is_active:
                role=res[0].role
                img=res[0].img
                username=res[0].username
                print("image :=============================================",img)
                request.session['email']=email
                request.session['username']=res[0].username
                request.session['password']=password
                request.session['image']=img.name
                if not User.objects.filter(username=username).exists():
                    User.objects.create_user(username=username)
                    print(f"✅ New user created: {username}")

                
                if role=="user":
                    messages.success(request,"✅ successful Login ! ✅")
                    return redirect("/userhome/")
                else:
                    messages.success(request,"✅ successful Login ! ✅")
                    return redirect("/adminhome/")
            else:
                messages.success(request,"⚠️ User Not Active !⚠️ ")
                return redirect("/login/")

        else:
            messages.success(request,"Invelid Email or password!❌")
            return redirect("/login/")
    else:
        return render(request,"login.html")

def register(request):
    if request.method=="POST":
        username=request.POST.get('username')
        email=request.POST.get('email')
        mobile=request.POST.get('mobile')
        gender=request.POST.get('gender')
        password=request.POST.get('password')
        role='user'
        is_active=1
        res=models.user.objects.filter(email=email)
        if res:
            messages.success(request, '❌ Registration Failed Email already Exist ! ❌')
            return redirect('/register/')
        else:
            obj=models.user(username=username, email=email,mobile=mobile,gender=gender,password=password,role=role,is_active=is_active)
            obj.save()
            messages.success(request, '✅ Registration successful ! ✅')
            return redirect('/login/')
    else:
        return render(request, "register.html")