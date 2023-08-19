from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from django.contrib import messages
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .models import Profile, Post


# Create your views here.

@login_required(login_url='signin')  # Requieres login
def index(request):
    user_object = User.objects.get(username=request.user.username)
    user_profile = Profile.objects.get(user=user_object)
    # Send user profile into html
    posts = Post.objects.all()
    return render(request, 'index.html', {'user_profile': user_profile, 'posts': posts})


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

                # Log user in and redirect to settings page
                user_login = auth.authenticate(
                    username=username, password=password)
                auth.login(request, user_login)

                # Create a profile fot the new user
                user_model = User.objects.get(
                    username=username)  # Getting User model
                new_profile = Profile.objects.create(
                    user=user_model, id_user=user_model.id)
                new_profile.save()
                return redirect('settings')

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


@login_required(login_url='signin')  # Requieres login
def settings(request):
    user_profile = Profile.objects.get(user=request.user)

    if request.method == 'POST':

        if request.FILES.get('image') == None:
            image = user_profile.image
            bio = request.POST['bio']
            location = request.POST['location']

            user_profile.profileimg = image
            user_profile.bio = bio
            user_profile.location = location
            user_profile.save()
        if request.FILES.get('image') != None:
            image = request.FILES.get('image')
            bio = request.POST['bio']
            location = request.POST['location']

            user_profile.profileimg = image
            user_profile.bio = bio
            user_profile.location = location
            user_profile.save()

        return redirect('settings')

    return render(request, 'setting.html', {'user_profile': user_profile})


@login_required(login_url='signin')  # Requieres login
def upload(request):
    if request.method == 'POST':
        user = request.user.username
        image = request.FILES.get('image_upload')
        caption = request.POST['caption']

        new_post = Post.objects.create(user=user, image=image, caption=caption)
        new_post.save()

        return redirect('/')
    else:
        return redirect('/')
    return HttpResponse('<h1>Uploading Settings</h1>')
