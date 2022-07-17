import imp
from django.db import models

# Create your models here.
from .managers import myManager

from django.db import models
from datetime import date
# Create your models here.
from django.contrib.auth.models import AbstractUser





class User(AbstractUser):
    name=models.CharField(max_length=100)
    email=models.EmailField(unique=True,max_length=150,null=False)
    password=models.CharField(max_length=250,unique=True,null=False)
    date_joined=models.DateField(default=date.isoformat(date.today()),editable=False)
    username=None
    
    objects=myManager()    
    USERNAME_FIELD='email'
    REQUIRED_FIELDS=[]



class Notes(models.Model):
   
    title=models.CharField(max_length=50,null=False)
    description=models.TextField(null=False)
    tag=models.CharField(default="general",max_length=30)
    date=models.DateField(default=date.isoformat(date.today()),editable=False)
    user=models.ForeignKey(User,on_delete=models.CASCADE)
   
    
    def __str__(self):
        return self.title