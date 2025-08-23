
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views
from django.contrib.auth import views as auth_views
urlpatterns = [
    path('',views.userhome),
    path('my_notes/',views.my_notes),
    path('upload_notes/',views.upload_notes),
    path('favorites/',views.favorites),
    path('download_pdf/',views.download_pdf),
    path('trash/',views.trash),
    path('delete_pdf/',views.delete_pdf),
    path('restore_pdf/',views.restore_pdf),
    path('delete_trash_pdf/',views.delete_trash_pdf),
    path('view_pdf/',views.view_pdf),
    path('is_favorite/',views.is_favorite),
    path('favorite/',views.favorites),
    path('is_favorite1/',views.is_favorite1),
    path('logout1/',views.logout1),
    path('help/',views.help),
    path('profile/',views.profile),
    path('edit_profile/',views.edit_profile),
    path('change_password/',views.change_password),
    # path('login/', auth_views.LoginView.as_view(), name='login'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)