from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from .models import Profile, Follow
from blog.models import Post
from .forms import LoginForm, ProfileForm
from django.contrib import messages
from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import logout


def home(request):
    print(request.user.is_authenticated)
    return render(request, 'users/home.html')


def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
        messages.success(request, 'Account created successfully')
    else:
        form = UserCreationForm()
    context={
        'form':form
        }
    return render(request, 'users/registration.html', context)

def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(username=cd['username'], password=cd['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect('profile_view', username=user.username)
                else:
                    return HttpResponse('Disabled account')
            else:
                return HttpResponse('Invalid login')
    else:
        form = LoginForm()
    return render(request, 'users/login.html', {'form': form})



@login_required
def profile_view(request, username):
    user = get_object_or_404(User, username=username)

    
    profile = getattr(user, 'profile', None) 

    context = {
        'user': user,
        'profile': profile,
    }

    return render(request, 'users/profile.html', context)

@login_required
def user_posts(request):
    posts = Post.objects.filter(author=request.user)  # Retrieve posts by the logged-in user
    return render(request, 'users/user_posts.html', {'posts': posts})


def edit_profile(request):
    profile, created = Profile.objects.get_or_create(user=request.user)  
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('profile_view', username=request.user.username)
    else:
        form = ProfileForm(instance=profile)
    return render(request, 'users/edit_profile.html', {'form': form})

def logout_view(request):
    logout(request)  
    return redirect('home')
   


@login_required
def follow_user(request, user_id):
    user_to_follow = get_object_or_404(User, id=user_id)
    if request.method == 'POST' and user_to_follow != request.user:
        Follow.objects.get_or_create(follower=request.user, following=user_to_follow)
    return redirect('profile_view', username=user_to_follow.username)

@login_required
def unfollow_user(request, user_id):
    user_to_unfollow = get_object_or_404(User, id=user_id)
    if request.method == 'POST' and user_to_unfollow != request.user:
        Follow.objects.filter(follower=request.user, following=user_to_unfollow).delete()
    return redirect('profile_view', username=user_to_unfollow.username)