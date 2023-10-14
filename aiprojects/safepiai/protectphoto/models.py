from django.db import models
import os

# Create your models here.
#파일을 업로드하면, Image object로 인식된다.

class Photo(models.Model):
    image = models.ImageField(upload_to='uploads/')
