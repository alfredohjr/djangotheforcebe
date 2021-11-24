from django.db import models

from django.contrib.auth.models import User
from django.db.models.fields.related import ForeignKey

# Create your models here.

class Permission(models.Model):

    choices = [
        ('GET','GET'),
        ('POST','POST'),
    ]

    method = models.CharField(max_length=10,choices=choices)
    url = models.CharField(max_length=150)

    def __str__(self) -> str:
        return self.method + ' ' + self.url


class UserPermission(models.Model):

    user = models.ForeignKey(User,on_delete=models.CASCADE)
    Permission = models.ForeignKey(Permission,on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.user.username + ' ' + self.Permission.__str__()


class Group(models.Model):
    
    name = models.CharField(max_length=30)

    def __str__(self) -> str:
        return self.name


class GroupPermission(models.Model):

    group = models.ForeignKey(Group,on_delete=models.CASCADE)
    permission = models.ManyToManyField(Permission)


class UserGroup(models.Model):

    user = models.ForeignKey(User,on_delete=models.CASCADE)
    group = models.ForeignKey(Group,on_delete=models.CASCADE)


class Log(models.Model):

    user = models.ForeignKey(User,on_delete=models.CASCADE)
    url = models.CharField(max_length=150)
    method = models.CharField(max_length=20,default='NA')
    text = models.TextField()
    startedAt = models.DateTimeField(blank=True, null=True)
    finishedAt = models.DateTimeField(blank=True, null=True)

    def __str__(self) -> str:
        return self.text