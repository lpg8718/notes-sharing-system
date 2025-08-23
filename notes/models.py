from django.db import models

class user(models.Model):
    id=models.AutoField(primary_key=True)
    username=models.CharField(max_length=100,unique=True)
    email=models.CharField(max_length=100,unique=True)
    mobile=models.CharField(max_length=13)
    gender=models.CharField(max_length=20)
    password=models.CharField(max_length=100)
    role=models.CharField(max_length=100)
    is_active=models.IntegerField()
    name=models.CharField(max_length=100, default='NULL')
    address=models.CharField(max_length=100, default='NULL')
    dob=models.CharField(max_length=20, default='NULL')
    img=models.FileField(upload_to='uploads/', default='default.png')
    



