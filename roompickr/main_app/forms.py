from django.forms import ModelForm
from .models import Profile, Feedback, Image, Question, Answer
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError



class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ["username"]


class ProfileForm(ModelForm):
    class Meta:
        model = Profile
        fields = ["full_name", "email", "avatar", "gender"]

    # reference: https://django-oscar.readthedocs.io/en/3.1/_modules/oscar/apps/customer/forms.html
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if Profile.objects.filter(email = email).exclude(id=self.instance.id).exists():
            raise ValidationError("This email already exists.")
        return email


class FeedbackForm(ModelForm):
    class Meta:
        model = Feedback
        fields = ["comment"]


class ImageForm(ModelForm):
    class Meta:
        model = Image
        fields = ["image_space", "caption"]

class QuestionForm(ModelForm):
    class Meta:
        model = Question
        fields = ["title", "content"]

class AnswerForm(ModelForm):
    class Meta:
        model = Answer
        fields = ["answer"]
