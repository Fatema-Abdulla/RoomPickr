from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

from .forms import ProfileForm, UserForm, FeedbackForm, BookingForm
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


@login_required
def space_index(request):
    spaces = Space.objects.filter(user=request.user)
    return render(request,'spaces/index.html', {'spaces':spaces})

@login_required
def space_detail(request, space_id):
    space = Space.objects.get(id=space_id)
    feedback_form = FeedbackForm()
    return render(request, 'spaces/detail.html', {"space": space , 'feedback_form' : feedback_form})


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

@login_required
def add_feedback(request, space_id, user_id):
    form = FeedbackForm(request.POST)
    if form.is_valid():
        new_feedback = form.save(commit=False)
        new_feedback.space_id = space_id
        new_feedback.user_id = user_id
        new_feedback.save()
    return redirect('detail', space_id)

#edit/update #delete feedback
'''
@login_required
def add_review(request, game_id):
    form = ReviewForm(request.POST)
    if form.is_valid():
        new_feeding = form.save(commit=False)
        new_feeding.game_id = game_id
        new_feeding.save()
    return redirect("detail", game_id)
# reference: https://openclassrooms.com/en/courses/6967196-create-a-web-application-with-django/7349667-update-a-model-object-with-a-modelform
@login_required
def update_review(request, game_id, review_id):
    review = Review.objects.get(id=review_id)
    review_form = ReviewForm()
    if request.method == "POST":
        form = ReviewForm(request.POST, instance=review)
        if form.is_valid():
            new_feeding = form.save(commit=False)
            new_feeding.game_id = game_id
            new_feeding.save()
        return redirect("detail", game_id)
    else:
        form = ReviewForm(instance=review)
    return render(request, 'games/detail.html', {'review_form': review_form, 'game_id': game_id})
@login_required
def delete_review(request, game_id, review_id):
    review = Review.objects.get(id=review_id)
    if review:
        review.delete()
    return redirect("detail", game_id)
<form action="{% url 'delete_review' game.id review.id %}" method="post" class="gc-delete-review-form">
            {% csrf_token %}
            <input type="submit" value="Delete" class="btn btn-red" />
          </form>
'''



class star_booking(LoginRequiredMixin, CreateView):
    model = Booking
    fields = ['start', 'end', 'status', 'total_price']

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

# @login_required
# def star_booking(request, space_id, user_id):
#     form = BookingForm(request.POST)
#     if form.is_valid():
#         new_booking = form.save(commit=False)
#         new_booking.space_id = space_id
#         new_booking.user_id = user_id
#         new_booking.save()
#     return render('booking/', space_id)

