from django.db import models
from django.urls import reverse
from datetime import date, time
from django.contrib.auth.models import User

# Create your models here.

class Profile(models.Model):
    name = models.CharField(max_length=100)
    email= models.EmailField(max_length=245)
    user= models.ForeignKey(User, on_delete=models.CASCADE)
    #phone_number = models.

    def __str__(self):
        return self.name

class Space(models.Model):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    capacity= models.IntegerField()
    type= models.CharField(max_length=1)
    price_per_hour= models.IntegerField()
    user= models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class image(models.Model):
    image= models.ImageField(upload_to='main_app/static/uploads/', default='')
    caption = models.TextField(max_length=150)
    space=models.ForeignKey(Space, on_delete=models.CASCADE)

    def __str__(self):
        return self.space.name


class feedback(models.Model):
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    comment= models.TextField(max_length=234)
    space=models.ForeignKey(Space, on_delete=models.CASCADE)
    user= models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.space.name}, {self.user.username}'

class booking(models.Model):
    start=models.DateTimeField(null=True)
    end=models.DateTimeField(null=True)
    # status=models.CharField
    total_price=models.IntegerField()
    space=models.ForeignKey(Space, on_delete=models.CASCADE)
    user= models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f'booking {self.space.name} for {self.user.username}'

class question(models.Model):
    created_at=models.DateTimeField(auto_now_add=True)
    title=models.CharField(max_length=150)
    content= models.TextField(max_length=300)
    user= models.ForeignKey(User, on_delete=models.CASCADE)


