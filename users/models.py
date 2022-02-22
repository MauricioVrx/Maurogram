"""Users models"""

import uuid

#Django
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.files.storage import default_storage


class User(AbstractUser):
    token =  models.UUIDField(primary_key=False, editable=False, null=True, blank=True)

class Visitor(models.Model):
    user = models.OneToOneField(User, null=False, related_name='visitor', on_delete=models.CASCADE)
    session_key = models.CharField(null=False, max_length=40)  

def upload_location(request, filename):
    filebase, extension = filename.split(".") 
    direc = 'users/pictures/'+str(request.user.username)+"."+str(extension)
    user = Profile.objects.filter(user_id=request.user.id).first()
    if user.picture !="":
        default_storage.delete(str(user.picture))
    return direc

class Profile(models.Model):
    """Profile model.
    
    Proxy model that extends the base data with other information.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    website = models.URLField(max_length=200, blank=True)
    biography = models.TextField(blank=True)
    phone_number = models.CharField(max_length=20, blank=True)

    picture = models.ImageField(
        upload_to=upload_location,
        blank=True, 
        null=True
    )

    created  = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        """Return username"""
        return self.user.username



class Follow(models.Model):
    """Follow model.""" 
    profile = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    user = models.IntegerField(blank=True)

    LOAN_STATUS = (
        ('f', 'following'),
        ('n', 'not following'),
        ('l', 'locked'),
        ('r', 'requested'),
        ('a', 'accepted'),
    )

    status = models.CharField(max_length=1, choices=LOAN_STATUS, blank=True, default='f')

    created  = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)    


