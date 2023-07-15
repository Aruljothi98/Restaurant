from django.db import models
import datetime
from django.contrib.auth.models import User
import os

# Create your models here.
def getfilename(request,filename):
    now_time=datetime.datetime.now().strftime("%Y%M%D%H:%M:%S")
    now_filename="%s %s"%(now_time,filename)
    return os.path.join('uploads/',now_filename)   
 
class menu(models.Model):
    name=models.CharField(max_length=150,null=False,blank=False)
    image=models.ImageField(upload_to=getfilename,null=True,blank=True)
    status=models.BooleanField(default=False,help_text="0-show,1-hidden")
    created_at=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    
class list(models.Model):
    Menu=models.ForeignKey(menu,on_delete=models.CASCADE)
    name=models.CharField(max_length=150,null=False,blank=False)
    list_image=models.ImageField(upload_to=getfilename,null=True,blank=True)
    price=models.FloatField(null=False,blank=False)
    quantity=models.IntegerField(null=False,blank=False)
    status=models.BooleanField(default=False,help_text="0-show0,1-hidden")
    trending=models.BooleanField(default=False,help_text="0-default,1-trending")
    created_at=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Cart(models.Model):
    User=models.ForeignKey(User,on_delete=models.CASCADE)
    list=models.ForeignKey(list,on_delete=models.CASCADE)
    list_qty=models.IntegerField(null=False,blank=False)
    created_at=models.DateTimeField(auto_now_add=True)

    @property
    def total_cost(self):
        return self.list_qty*self.list.price


class Favourite(models.Model):
    User=models.ForeignKey(User,on_delete=models.CASCADE)
    list=models.ForeignKey(list,on_delete=models.CASCADE)
    created_at=models.DateTimeField(auto_now_add=True)


    
    

    






