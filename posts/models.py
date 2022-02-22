"""Posts models."""

#Django
from django.db import models
from users.models import User
import uuid


def upload_location(instance, filename):
    base = 'posts/photos/'
    username = instance.user.username
    extension = filename.split(".")[-1]
    return base + "%s/%s.%s" %(username,uuid.uuid4(),extension)


class Post(models.Model):
    """Post model."""

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    #profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    profile = models.ForeignKey('users.Profile', on_delete=models.CASCADE)

    title = models.CharField(max_length=255)
    photo = models.ImageField(upload_to=upload_location)

    created  = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        """Return title and username."""
        return  f'{self.title} by @{self.user.username}'
    

class Like(models.Model):
    """Follow model.""" 
    profile = models.ForeignKey(User,   on_delete=models.SET_NULL, null=True)
    post    = models.ForeignKey('Post', on_delete=models.SET_NULL, null=True)
    # post = models.IntegerField(blank=True)

    LOAN_STATUS = (
        ('l', 'like'),
        ('n', 'not like'),
    )

    status = models.CharField(max_length=1, choices=LOAN_STATUS, blank=True, default='n')

    created  = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)  


class Comment(models.Model):
    """Comments model """
    user = models.ForeignKey(User, on_delete=models.RESTRICT)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

    comment = models.CharField(max_length=250, blank=True)

    LOAN_STATUS = (
        ('a', 'active'),
        ('n', 'not active'),
        ('d', 'delete'),
        ('b', 'banned'),
    )

    status = models.CharField(max_length=1, choices=LOAN_STATUS, blank=True, default='a')

    created  = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)