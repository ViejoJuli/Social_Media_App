from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from django.contrib import messages
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .models import Profile


# Create your views here.

@login_required(login_url='signin')  # Requieres login
def index(request):
    return render(request, 'index.html')


def signup(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        password2 = request.POST['password2']
        email = request.POST['email']

        # Check if password matches
        if password == password2:
            # Check if email is not already in use
            if User.objects.filter(email=email).exists():
                messages.info(request, 'Email already in use')
                return redirect('signup')
            elif User.objects.filter(username=username).exists():
                messages.info(request, 'Username already in use')
                return redirect('signup')
            else:
                user = User.objects.create_user(
                    username=username, password=password, email=email)
                user.save()

                # Create a profile fot the new user
                user_model = User.objects.get(
                    username=username)  # Getting User model
                new_profile = Profile.objects.create(
                    user=user_model, id_user=user_model.id)
                new_profile.save()
                return redirect('signup')

        else:
            messages.info(request, 'Password mismatch')
            return redirect('signup')

    else:
        return render(request, 'signup.html')


def signin(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            return redirect('/')
        else:
            messages.info(request, 'Invalid username or password')
            return redirect('signin')

    else:
        return render(request, 'signin.html')


@login_required(login_url='signin')  # Requieres login
def logout(request):
    auth.logout(request)
    return redirect('signin')
