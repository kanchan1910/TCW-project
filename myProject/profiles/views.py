# views.py

import threading

from django.conf import settings
from django.contrib import messages
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from threading import Thread


class WelcomeEmailThread(threading.Thread):
    def __init__(self, recipient_list):
        self.recipient_list = recipient_list
        threading.Thread.__init__(self)

    def send_welcome_email(self):
        subject = 'Welcome to Portfolio Hub!'
        message = 'Thank you for signing up. Build and share your portfolio.'
        email_from = settings.EMAIL_HOST_USER
        send_mail(subject, message, email_from, self.recipient_list)

    def run(self):
        self.send_welcome_email()


# Create your views here.
def index(request):
    return render(request, 'index.html')

def profile(request):
    return render(request, 'profile.html')

def signup(request):
    email_id = request.GET.get('email')
    password = request.GET.get('password')
    confirm_password = request.GET.get('confirmPassword')

    if not (email_id and password and confirm_password):
        messages.add_message(request, messages.ERROR, 'Please provide all the details!!')
        return render(request, 'index.html')

    if password != confirm_password:
        messages.add_message(request, messages.ERROR, 'Both passwords should match!!')
        return render(request, 'index.html')

    is_user_exists = User.objects.filter(email=email_id).exists()

    if is_user_exists:
        messages.add_message(request, messages.ERROR, 'User with this email id already exists!!')
        return render(request, 'index.html')

    user = User()
    user.email = email_id
    user.username = email_id.split('@')[0]
    user.password = password
    user.save()

    # Send welcome email asynchronously
    WelcomeEmailThread([user.email]).start()
    print('Welcome mail triggered asynchronously to email id: {email_id}'.format(email_id=user.email))

    print(user.id)
    messages.add_message(request, messages.SUCCESS, 'Signup Successful!! You can now proceed to login!')
    return render(request, 'index.html')


def login(request):
    email_id = request.GET.get('email')
    password = request.GET.get('password')

    if not (email_id and password):
        return HttpResponse('Please provide all the details!!')

    user_qs = User.objects.filter(email=email_id, password=password)
    if not user_qs:
        messages.add_message(request, messages.ERROR, 'Wrong email or password provided!!')
        return render(request, 'index.html')

    user = user_qs[0]
    print(user.id)
    url_path = reverse('userprofile')
    return HttpResponseRedirect(url_path)
