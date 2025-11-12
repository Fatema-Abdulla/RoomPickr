from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

from .forms import ProfileForm, UserForm
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView
from .models import Profile, Space, Image, Feedback, Booking, Question, Answer


# Create your views here.
@login_required
def home(request):
    return render (request, 'home.html')

@login_required
def about(request):
    return render (request, 'about.html')

@login_required
def rooms_index(request):
    return render (request, 'rooms/index.html')

def signup(request):
    error_message = ""
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('index')
        else:
            error_message = "Invalid Sign Up, Try again later..."
    form = UserCreationForm()
    context = {'form': form, 'error_message': error_message}
    return render(request, 'registration/signup.html', context)

@login_required
def profile(request):
    profiles = Profile.objects.filter(user=request.user)
    return render(request, "users/profile.html", {"profiles": profiles})

@login_required
# reference: https://pythonguides.com/create-a-user-profile-using-django/
def update_profile(request, profile_id):
    profile = Profile.objects.get(id=profile_id)
    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=request.user)
        profile_form = ProfileForm(request.POST, instance=profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return redirect('/accounts/profile/')
    else:
        user_form = UserForm(instance=request.user)
        profile_form = ProfileForm(instance=profile)

    return render(request, 'users/update_profile.html', {'user_form': user_form, 'profile_form': profile_form})



class SpaceList(LoginRequiredMixin, ListView):
    model = Space

class SpaceDetail(LoginRequiredMixin, DetailView):
    model = Space

class SpaceCreate(LoginRequiredMixin, CreateView):
    model = Space
    fields = ['name', 'address', 'capacity', 'type', 'price_per_hour']

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class SpaceUpdate(LoginRequiredMixin, UpdateView):
    model = Space
    fields = "__all__"

class SpaceDelete(LoginRequiredMixin, DeleteView):
    model = Space
    success_url = "/stores/"


def add_feedback(request):
    if request.method == 'POST':
        form = Feedback(request.POST)
        if form.is_valid():
            new_feedBack = form.save(commit=False)
            new_feedBack#.space_id = space_id
            new_feedBack.save()
            return redirect()

##########################################
# def add_feedback(request):
#     form = Feedback(request.POST)
#     if form.is_valid():
#         new_feedBack = form.save(commit=False)
#         new_feedBack.#space_id = space_id
    #     new_feedBack.save()
    # return redirect()

