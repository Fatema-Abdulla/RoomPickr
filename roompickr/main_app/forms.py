from django.forms import ModelForm
from .models import Profile
from django.contrib.auth.models import User

class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ['username']

class ProfileForm(ModelForm):
    class Meta:
        model = Profile
        fields = ['name', 'email', 'gender']
