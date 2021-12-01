from django.db import models
from django.utils import timezone
from django.core.exceptions import ValidationError

# Create your models here.

class Script(models.Model):

    name = models.CharField(max_length=50)
    description = models.TextField()
    script = models.TextField()
    group = models.ForeignKey('Group',on_delete=models.SET_NULL, blank=True, null=True)
    active = models.BooleanField(default=False)
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)
    deletedAt = models.DateTimeField(null=True, blank=True)    

    def __str__(self):
        return self.name


class Group(models.Model):

    name = models.CharField(max_length=30)
    active = models.BooleanField(default=False)
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)
    deletedAt = models.DateTimeField(null=True, blank=True)    

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if self.pk is None:
            pass
        else:
            obj = Group.objects.get(id=self.id)
            if obj.deletedAt and self.deletedAt:
                raise ValidationError('don\'t alter deleted item')
        
        return super().save(*args, **kwargs)

    def delete(self):

        script = Script.objects.filter(group__id=self.id,active=True)
        if script:
            crontab = Crontab.objects.filter(script__in=script,active=True)
            if crontab:
                raise ValidationError('don\'t delete group with crontab active')
            raise ValidationError('don\'t delete group with script active')

        self.deletedAt = timezone.now()
        self.save()
    
    def open(self):
        self.deletedAt = None
        self.save()
    
    def close(self):
        self.delete()



class Crontab(models.Model):

    name = models.CharField(max_length=50)
    script = models.ForeignKey(Script,on_delete=models.CASCADE)
    description = models.TextField()
    active = models.BooleanField(default=False)
    minute = models.CharField(max_length=20)
    hour = models.CharField(max_length=20)
    dayOfMonth = models.CharField(max_length=20)
    month = models.CharField(max_length=20)
    dayOfWeek = models.CharField(max_length=20)
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)
    deletedAt = models.DateTimeField(null=True, blank=True)    

    def __str__(self):
        return self.name


class ExecutionLog(models.Model):

    script = models.ForeignKey(Script, on_delete=models.CASCADE)
    crontab = models.ForeignKey(Crontab, on_delete=models.CASCADE,null=True,blank=True)
    startedAt = models.DateTimeField(null=True, blank=True)
    finishedAt = models.DateTimeField(null=True, blank=True)
    success = models.BooleanField(default=False)
    message = models.TextField(null=True, blank=True)
    createdAt = models.DateTimeField(auto_now_add=True)
    deletedAt = models.DateTimeField(null=True, blank=True)    


class ExecutionManual(models.Model):

    script = models.ForeignKey(Script,on_delete=models.CASCADE)
    user = models.IntegerField(default=0)
    run = models.BooleanField(default=True)
    startAt = models.DateTimeField(default=timezone.now)
    finishedAt = models.DateTimeField(blank=True, null=True)
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)
    deletedAt = models.DateTimeField(null=True, blank=True)    

