from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

from .forms import ProfileForm, UserForm, FeedbackForm, ImageForm, QuestionForm
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView
from .models import Profile, Space, Image, Feedback, Booking, Question, Answer


# Create your views here.
@login_required
def home(request):
    return render(request, "home.html")


@login_required
def about(request):
    return render(request, "about.html")


# @login_required
# def rooms_index(request):
#     return render (request, 'rooms/index.html')


def signup(request):
    error_message = ""
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("index")
        else:
            error_message = "Invalid Sign Up, Try again later..."
    form = UserCreationForm()
    context = {"form": form, "error_message": error_message}
    return render(request, "registration/signup.html", context)


@login_required
def profile(request):
    profiles = Profile.objects.filter(user=request.user)
    return render(request, "users/profile.html", {"profiles": profiles})


@login_required
# reference: https://pythonguides.com/create-a-user-profile-using-django/
def update_profile(request, profile_id):
    profile = Profile.objects.get(id=profile_id)
    if request.method == "POST":
        user_form = UserForm(request.POST, instance=request.user)
        profile_form = ProfileForm(request.POST, instance=profile)

        if user_form.is_valid() and profile_form.is_valid():
            profile_form.save()
            user_form.save()
            return redirect("/accounts/profile/")
    else:
        user_form = UserForm(instance=request.user)
        profile_form = ProfileForm(instance=profile)

    return render(
        request,
        "users/update_profile.html",
        {"user_form": user_form, "profile_form": profile_form},
    )


@login_required
def space_index(request):
    spaces = Space.objects.filter(user=request.user)
    return render(request, "spaces/index.html", {"spaces": spaces})


@login_required
def space_detail(request, space_id):
    space = Space.objects.get(id=space_id)
    feedback_form = FeedbackForm()
    image_form = ImageForm()
    return render(
        request,
        "spaces/detail.html",
        {"space": space, "feedback_form": feedback_form, "image_form": image_form},
    )


class SpaceCreate(LoginRequiredMixin, CreateView):
    model = Space
    fields = ["name", "address", "capacity", "type", "price_per_hour"]

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class SpaceUpdate(LoginRequiredMixin, UpdateView):
    model = Space
    fields = "__all__"


class SpaceDelete(LoginRequiredMixin, DeleteView):
    model = Space
    success_url = "/stores/"


@login_required
def add_feedback(request, space_id, user_id):
    form = FeedbackForm(request.POST)
    if form.is_valid():
        new_feedback = form.save(commit=False)
        new_feedback.space_id = space_id
        new_feedback.user_id = user_id
        new_feedback.save()
    return redirect("detail", space_id)


@login_required
def add_image(request, space_id):
    form = ImageForm(request.POST, request.FILES)
    if form.is_valid():
        new_image = form.save(commit=False)
        new_image.space_id = space_id
        new_image.save()
    return redirect("detail", space_id)


@login_required
def update_image(request, space_id, image_id):
    image = Image.objects.get(id=image_id)
    image_form = ImageForm()
    if request.method == "POST":
        form = ImageForm(request.POST, request.FILES, instance=image)
        if form.is_valid():
            new_image = form.save(commit=False)
            new_image.space_id = space_id
            new_image.save()
        return redirect("detail", space_id)
    else:
        form = ImageForm(instance=image)

    return render(request, 'spaces/detail.html', {'image_form': image_form, 'space_id': space_id})

@login_required
def delete_image(request, space_id, image_id):
    image = Image.objects.get(id=image_id)
    if image:
        image.delete()
    return redirect("detail", space_id)

@login_required
def questions(request):
    questions = Question.objects.filter(user=request.user)
    question_form = QuestionForm()
    return render(request, "community/question.html", {"questions": questions, "question_form": question_form})

@login_required
def add_question(request, user_id):
    form = QuestionForm(request.POST)
    if form.is_valid():
        new_question = form.save(commit=False)
        new_question.user_id = user_id
        new_question.save()
    return redirect("questions")

@login_required
def question_detail(request, question_id):
    question = Question.objects.get(id=question_id)
    return render(request, "community/detail_question.html", {"question": question, "question_id": question_id})

@login_required
def update_question(request, question_id):
    question = Question.objects.get(id=question_id)
    if request.method == "POST":
        question_form = QuestionForm(request.POST, instance=question)
        if question_form.is_valid():
            question_form.save()
        return redirect("question_detail", question_id)
    else:
        question_form = QuestionForm(instance=question)

    return render(request, 'community/update_question.html', {'question_form': question_form, 'question_id': question_id})
