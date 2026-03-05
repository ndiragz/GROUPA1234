from django.contrib.auth.models import User
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

class Payment(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    phone = models.IntegerField(max_length=15)
    amount = models.IntegerField()
    checkout_request_id = models.CharField(max_length=100,blank=True)
    status = models.CharField(default='pending',max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.phone


