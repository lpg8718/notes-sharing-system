from django.core.files.storage import FileSystemStorage
from django.http import FileResponse, Http404
from django.shortcuts import render,redirect
from django.contrib.auth import logout
from django.http import FileResponse
from django.contrib import messages
from django.conf import settings
media_url=settings.MEDIA_URL
from userapp import models
import mimetypes
import os

# Create your views here.
def userhome(request):
    username = request.session.get('username')
    visibility='Public'
    obj=models.uploads.objects.filter(is_active=1,visibility=visibility)
    print("username :",username)
    user = User.objects.get(username=username)
    return render(request,"userhome.html",{'username':username,'obj':obj,'user': user})




def my_notes(request):
    email=request.session.get('email')
    username = request.session.get('username')
    user = User.objects.get(username=username)
    obj=models.uploads.objects.filter(email=email,is_active=1)
    #Download counter
    total_downloads = sum(i.download_count for i in obj)
    print("total Downloads :",total_downloads)
    #favorite
    # total_favorite = sum(i.is_favorite for i in obj1)
    total_favorite = models.uploads.objects.filter(favorites=user,is_active=1).count()
    print("total favorites :",total_favorite)
    #View counter
    total_view = sum(i.view_counter for i in obj)
    print("total Views :",total_view)
    return render(request,"my_notes.html",{'obj':obj,'username':username,'media_url':media_url,'total_downloads':total_downloads,'total_view':total_view, 'favorite': total_favorite})



def view_pdf(request):
    id=request.GET.get('id')
    obj=models.uploads.objects.filter(id=id).first()
    file_path = os.path.join(settings.MEDIA_ROOT, obj.file.name)
    obj.view_counter += 1
    obj.save()
    
    print("file:",file_path)
      # Content-Type automatically detect करो
    content_type, encoding = mimetypes.guess_type(file_path)
    if content_type is None:
        content_type = 'application/octet-stream'  # fallback

    return FileResponse(open(file_path, 'rb'), content_type=content_type)




def upload_notes(request):
    if request.method=="POST":
        username=request.session.get('username')
        email=request.session.get('email')
        title=request.POST.get('title')
        category=request.POST.get('category')
        visibility=request.POST.get('visibility')
        file=request.FILES['file']
        is_active=1
        fs=FileSystemStorage()
        file_name=fs.save(file.name,file) 
        bytes = file.size
        if bytes < 1024 * 1024:
            size = round(bytes / 1024, 2)  # KB
            file_size=str(size)+" KB"
           
        else:
            size = round(bytes / (1024 * 1024), 2)  # MB
            file_size=str(size)+" MB"
            
        print("username :",username)
        print("email: ",email)
        print("title",title)
        print("category: ",category)
        print("visibility :",visibility)
        print("file :",file)
        print("file_size : ",file_size)
        print("name: ",file_name)
        
        obj=models.uploads(username=username,email=email,title=title,category=category,visibility=visibility,file=file_name,file_size=file_size,is_active=is_active)
        obj.save()
        messages.success(request,"✅ successful Upload ! ✅")
        return redirect("/userhome/upload_notes/")
    else:
        username = request.session.get('username')
        return render(request,"upload_notes.html",{'username':username})
        
# def favorites(request):
#     username = request.session.get('username')
#     obj=models.uploads.objects.filter(is_favorite=1,is_active=1)
    
#     return render(request,"favorites.html",{'username':username,'obj':obj})




def download_pdf(request):
    file_id = request.GET.get('name')  # ?id=1 जैसे URL से आएगा

    if not file_id:
        raise Http404("No ID provided")

    obj = models.uploads.objects.filter(id=file_id).first()
    obj.download_count += 1
    obj.save()
    if not obj:
        raise Http404("File not found in database")

    file_path = os.path.join(settings.MEDIA_ROOT, obj.file.name)

    if os.path.exists(file_path):
        return FileResponse(open(file_path, 'rb'), as_attachment=True, filename=os.path.basename(file_path))
    else:
        raise Http404("File not found on server")
    

def delete_pdf(request):
    id=request.GET.get('id')
    obj=models.uploads.objects.filter(id=id)
    is_active=0  # delete 
    models.uploads.objects.filter(id=id).update(is_active=is_active)
    return redirect("/userhome/my_notes/")

def delete_trash_pdf(request):
    id=request.GET.get('id')
    obj=models.uploads.objects.filter(id=id,is_active=0)
    obj.delete()
    return redirect("/userhome/trash/")

def restore_pdf(request):
    id=request.GET.get('id')
    obj=models.uploads.objects.filter(id=id)
    is_active=1  # Restore 
    models.uploads.objects.filter(id=id).update(is_active=is_active)
    return redirect("/userhome/trash/")


from django.shortcuts import render, redirect, get_object_or_404
from .models import uploads
from notes.models import user
from django.contrib.auth.models import User

def is_favorite(request):
    # Check if user is logged in via session
    username = request.session.get('username')
    
    if not username:
        return redirect('login')  # Redirect to login page if not logged in
    
    # Get the note to toggle favorite
    upload_id = request.GET.get('id')
    note = models.uploads.objects.get(id=upload_id)
    print("==================================================email", username)
    # Get user object from session username
    user1=User.objects.get(username=username)
    print("_======================================================user:",user1)
    # Toggle favorite status
    if user1 in note.favorites.all():
        print("_======================================================inside if:")
        note.favorites.remove(user1)  # Remove from favorites if already added
    else:
        print("_======================================================inside else:")
        note.favorites.add(user1)  # Add to favorites if not already added

    # Redirect to userhome or wherever you want
    return redirect('/userhome/')

def is_favorite1(request):
    # Check if user is logged in via session
    username = request.session.get('username')
    
    if not username:
        return redirect('login')  # Redirect to login page if not logged in
    
    # Get the note to toggle favorite
    upload_id = request.GET.get('id')
    note = models.uploads.objects.get(id=upload_id)
    print("==================================================email", username)
    # Get user object from session username
    user1=User.objects.get(username=username)
    print("_======================================================user:",user1)
    # Toggle favorite status
    if user1 in note.favorites.all():
        print("_======================================================inside if:")
        note.favorites.remove(user1)  # Remove from favorites if already added
    else:
        print("_======================================================inside else:")
        note.favorites.add(user1)  # Add to favorites if not already added

    # Redirect to userhome or wherever you want
    return redirect('/userhome/favorite/')





def favorites(request):
    
    print("========================================================================Favorites")
    username = request.session.get('username')

    if not username:
        return redirect('login')

    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        return redirect('login')

    # Get all notes this user has favorited
    favorite_notes = models.uploads.objects.filter(favorites=user,is_active=1)

    return render(request, 'favorites.html', {'obj': favorite_notes, 'username':username})
    
# =======================================================================




def trash(request):
    email = request.session.get('email')
    username = request.session.get('username')
    obj = models.uploads.objects.filter(email=email, is_active=0)
   
    return render(request, 'trash.html', {'obj': obj, 'username':username})


def profile(request):
    email=request.session.get('email')
    username=request.session.get('username')
    obj=user.objects.filter(email=email)
    return render(request,"profile.html",{'obj':obj,'username':username})


def edit_profile(request):
    email=request.session.get('email')
    username=request.session.get('username')
    if request.method=='POST':
       name=request.POST.get('name')
       mobile=request.POST.get('mobile')
       dob=request.POST.get('dob')
       address=request.POST.get('address')
       print("===============================================================if")
       print("name :",name,mobile,dob,address)
       user.objects.filter(email=email).update(name=name,mobile=mobile,dob=dob,address=address)

       return redirect("/userhome/profile/")
    else:
        print("-==========================================================================else")
        obj=user.objects.filter(email=email)

        return render(request,"edit_profile.html",{'obj':obj,'username':username})


def change_password(request):
    return render(request,"change_password.html")


def logout1(request):
    logout(request)
    return redirect('http://127.0.0.1:8000')




def help(request):
    
    username = request.session.get('username')
    visibility='Public'
    obj=models.uploads.objects.filter(is_active=1,visibility=visibility)
    print("username :",username)
    
    return render(request,'help.html',{'username':username,'obj':obj})
