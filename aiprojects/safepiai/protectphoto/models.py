from django.db import models

# Create your models here.

from django.db import models
import os

# Create your models here.
#파일을 업로드하면, File object로 인식된다.
class Photo(models.Model):
    image = models.FileField(null=True, blank=True, upload_to='uploads/')

    class Meta:
        app_label = 'protectphoto'

    def save(self):
        super().save()