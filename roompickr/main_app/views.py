from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import ProfileForm, UserForm, FeedbackForm, ImageForm, QuestionForm, AnswerForm
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView
from .models import Profile, Space, Image, Feedback, Booking, Question, Answer

from django.utils import timezone


from django_xhtml2pdf.utils import generate_pdf

from django.core.mail import EmailMessage
from django.template.loader import render_to_string

import qrcode
from io import BytesIO
import base64


# Create your views here.
@login_required
def home(request):
    return render(request, "home.html")


@login_required
def about(request):
    return render(request, "about.html")


@login_required
def contact_us(request):
    return render(request, "contact.html")

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
            return redirect("profile")
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
def update_profile(request, profile_id):
    profile = Profile.objects.get(id=profile_id)
    if request.method == "POST":
        user_form = UserForm(request.POST, instance=request.user)
        profile_form = ProfileForm(request.POST, request.FILES, instance=profile)

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
def space_all(request):
    spaces = Space.objects.all()
    return render(request, "spaces/all_space.html", {"spaces": spaces})


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
    fields = ["name", "address", "capacity", "type", "price_per_hour", "description", "thumbnail"]

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class SpaceUpdate(LoginRequiredMixin, UpdateView):
    model = Space
    fields = ["name", "address", "capacity", "type", "price_per_hour", "description", "thumbnail"]


class SpaceDelete(LoginRequiredMixin, DeleteView):
    model = Space
    success_url = "/spaces/"


@login_required
def add_feedback(request, space_id):
    form = FeedbackForm(request.POST)
    if form.is_valid():
        new_feedback = form.save(commit=False)
        new_feedback.space_id = space_id
        new_feedback.user = request.user
        new_feedback.save()
    return redirect('detail', space_id)

#edit/update
@login_required
def edit_feedback(request, space_id, feedback_id):
    review = Feedback.objects.get(id=feedback_id)
    form = FeedbackForm()
    if request.method == "POST":
        form= FeedbackForm(request.POST, instance=review)
    if form.is_valid():
        new_feedback = form.save(commit=False)
        new_feedback.space_id = space_id
        new_feedback.save()
    return redirect('detail', space_id)



def delete_feedback(request, space_id, feedback_id):
    feedback = Feedback.objects.get(id=feedback_id)
    if feedback:
        feedback.delete()
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
            image_update = form.save(commit=False)
            image_update.space_id = space_id
            image_update.save()
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
def your_questions(request):
    questions = Question.objects.filter(user=request.user)
    question_form = QuestionForm()
    return render(request, "community/your_question.html", {"questions": questions, "question_form": question_form})

@login_required
def questions(request):
    questions = Question.objects.all()
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
    answer_form = AnswerForm()
    return render(request, "community/detail_question.html", {"question": question, "question_id": question_id, "answer_form": answer_form})

class QuestionUpdate(LoginRequiredMixin, UpdateView):
    model = Question
    fields = ['title', 'content']

class QuestionDelete(LoginRequiredMixin, DeleteView):
    model = Question
    success_url = "/community/"

@login_required
def add_answer(request, user_id, question_id):
    form = AnswerForm(request.POST)
    if form.is_valid():
        new_answer = form.save(commit=False)
        new_answer.question_id = question_id
        new_answer.user_id = user_id
        new_answer.save()
    return redirect("question_detail", question_id)

@login_required
def update_answer(request, answer_id, question_id):
    answer = Answer.objects.get(id=answer_id)
    answer_form = AnswerForm()
    if request.method == "POST":
        form = AnswerForm(request.POST, instance=answer)
        if form.is_valid():
            answer_update = form.save(commit=False)
            answer_update.question_id = question_id
            answer_update.save()
        return redirect("question_detail", question_id)
    else:
        form = AnswerForm(instance=answer)

    return render(request, 'community/detail_question.html', {'answer_form': answer_form, 'question_id': question_id})

@login_required
def delete_answer(request, answer_id, question_id):
    answer = Answer.objects.get(id=answer_id)
    if answer:
        answer.delete()
    return redirect("question_detail", question_id)

class start_booking(LoginRequiredMixin, CreateView):
    model = Booking
    fields = ['start', 'end']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        space = Space.objects.get(id=self.kwargs["pk"])
        context["price_per_hour"] = space.price_per_hour
        return context

    def form_valid(self, form):
        form.instance.space_id = self.kwargs["pk"]
        form.instance.user = self.request.user
        booking = form.save(commit=False)

        # This part form AI
        validation_msg = booking.clean()
        if validation_msg:
            form.add_error(None, validation_msg)
            return self.form_invalid(form)
        # End part AI

        booking.total_price_calculate()
        booking.save()

        def send_welcome_email():
            qr_data = (
                f"Booking ID: {booking.id}\n"
                f"User Name: {self.request.user.profile.full_name}\n"
                f"Email: {self.request.user.profile.email}\n"
                f"Start: {booking.start}\n"
                f"End: {booking.end}\n"
                f"Total Price: {booking.total_price}"
            )

            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_L,
                box_size=10,
                border=4,
            )
            qr.add_data(qr_data)
            qr.make(fit=True)
            img = qr.make_image(fill_color="black", back_color="white")
            buffered = BytesIO()
            img.save(buffered, format="PNG")

            subject = 'Thank You for Your Booking'
            html_message = render_to_string('emails/booking_email.html', {
                'booking': booking,
                'user': self.request.user,
                'qr_code_image': 'cid:qr_code.png',
            })

            email = EmailMessage(
                subject=subject,
                body=html_message,
                to=[self.request.user.profile.email],
            )

            email.content_subtype = 'html'
            # part ai
            email.attach('qr_code.png', buffered.getvalue(), 'image/png')
            html_message = html_message.replace(
                '{{ qr_code_image }}', 'cid:qr_code.png'
            )
            # end part ai
            email.send()

        send_welcome_email()
        return super().form_valid(form)

class BookingDetail(LoginRequiredMixin, DetailView):
    model = Booking

class SearchResultsView(LoginRequiredMixin, ListView):
    model = Space

    def get_queryset(self):
        if self.request.GET.get('type'):
            selected_type = self.request.GET.get('type')
            object_list = Space.objects.filter(type=selected_type)
        else:
            object_list = Space.objects.all()

        return object_list

@login_required
def booking_history(request):
    booking = Booking.objects.filter(user=request.user)
    current_time = timezone.now()
    return render(request, "spaces/your_booking.html", {"booking": booking, 'current_time': current_time})

class DeleteBooking(LoginRequiredMixin, DeleteView):
    model = Booking
    success_url = "/spaces/"


@login_required
def invoice_booking(request, book_id):
    booking = Booking.objects.filter(id=book_id)

    resp = HttpResponse(content_type='application/pdf')
    resp['Content-Disposition'] = 'attachment; filename="Booking Invoice.pdf"'
    result = generate_pdf('main_app/invoice.html', file_object=resp, context={'booking': booking})
    return result
