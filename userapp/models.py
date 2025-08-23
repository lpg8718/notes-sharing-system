from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class uploads(models.Model):
    id=models.AutoField(primary_key=True)
    username=models.CharField(max_length=100)
    email=models.CharField(max_length=100)
    title = models.CharField(max_length=100)
    category=models.CharField(max_length=100)
    visibility=models.CharField(max_length=100)
    file = models.FileField(upload_to='uploads/')
    file_size =models.CharField(max_length=100)
    upload_at= models.DateTimeField(auto_now_add=True)
    is_active=models.IntegerField()
    favorites = models.ManyToManyField(User, related_name='favorite_uploads', blank=True)
    download_count = models.IntegerField(default=0)
    view_counter = models.IntegerField(default=0)
    



class favorite(models.Model):
    id=models.AutoField(primary_key=True)
    notes_id=models.BigIntegerField()
    username=models.CharField(max_length=100)
    email=models.CharField(max_length=100)
    is_favorite=models.IntegerField(default=0)