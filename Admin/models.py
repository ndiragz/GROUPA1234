from django.db import models

from django.utils import timezone

# Create your models here.
class Student(models.Model):
    image = models.ImageField(upload_to='students/',null=True,blank=True)
    name = models.CharField(max_length=20)
    course = models.CharField(max_length=50)
    age = models.IntegerField()
    email = models.EmailField()
    date = models.DateField(default=timezone.now)
    def __str__(self):
        return self.name




