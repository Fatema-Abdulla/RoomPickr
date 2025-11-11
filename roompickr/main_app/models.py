from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User


TYPES=(
    ('O', 'Office'),
    ('H', 'Hall'),
    ('M', 'Meeting Room'),
)


GENDERS=(
    ('F', 'Female'),
    ('M', 'Male')
)

# Create your models here.

class Profile(models.Model):
    name = models.CharField(max_length=100)
    email= models.EmailField(max_length=245)
    user= models.ForeignKey(User, on_delete=models.CASCADE)
    gender= models.CharField(max_length=1, choices=GENDERS, default=GENDERS[0][0])

    def __str__(self):
        return self.name

class Space(models.Model):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    capacity= models.IntegerField()
    type= models.CharField(max_length=1, choices=TYPES, default=TYPES[0][0])
    price_per_hour= models.IntegerField()
    user= models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class Image(models.Model):
    image= models.ImageField(upload_to='main_app/static/uploads/', default='')
    caption = models.TextField(max_length=150)
    space=models.ForeignKey(Space, on_delete=models.CASCADE)

    def __str__(self):
        return self.space.name


class Feedback(models.Model):
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    comment= models.TextField(max_length=234)
    space=models.ForeignKey(Space, on_delete=models.CASCADE)
    user= models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.space.name}, {self.user.username}'

class Booking(models.Model):
    start=models.DateTimeField(null=True)
    end=models.DateTimeField(null=True)
    status=models.CharField(max_length=10, default='pending') #under test
    total_price=models.IntegerField()
    space=models.ForeignKey(Space, on_delete=models.CASCADE)
    user= models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f'booking {self.space.name} for {self.user.username}'

class Question(models.Model):
    created_at=models.DateTimeField(auto_now_add=True)
    title=models.CharField(max_length=150)
    content= models.TextField(max_length=500)
    user= models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.title} from {self.user.username}'

class Answer(models.Model):
    created_at=models.DateTimeField(auto_now_add=True)
    answer= models.TextField(max_length=500)
    question= models.ForeignKey(Question, on_delete=models.CASCADE)
    user= models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f'answer of {self.question} from {self.user.username}'




