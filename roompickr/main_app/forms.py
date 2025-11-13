from django.forms import ModelForm
from .models import Profile, Feedback, Image
from django.contrib.auth.models import User


class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ["username"]


class ProfileForm(ModelForm):
    class Meta:
        model = Profile
        fields = ["name", "email", "gender"]


class FeedbackForm(ModelForm):
    class Meta:
        model = Feedback
        fields = ["comment"]


class ImageForm(ModelForm):
    class Meta:
        model = Image
        fields = ["image_space", "caption"]
