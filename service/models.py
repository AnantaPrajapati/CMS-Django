from django.db import models
from django.contrib.auth.models import User
from django.contrib.postgres.fields import ArrayField


# Create your models here.


class Notice(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null = True)
    title = models.CharField(max_length = 255)
    description = models.TextField()
    # image = ArrayField(models.ImageField(upload_to='notices'), default=list)
    # upload_to='images'
    
    def __str__(self):
        return self.title
    

class  NoticeImage(models.Model):
    notice = models.ForeignKey(Notice, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='notices', default="", null=True, blank=True)
