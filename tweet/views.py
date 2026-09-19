from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.contrib import messages
from .models import Tweet
from .forms import TweetForm, UserRegistrationForm


def index(request):
    return redirect('tweet_list')


def tweet_list(request):
    tweets = Tweet.objects.all().order_by('-created_at')
    form = TweetForm() if request.user.is_authenticated else None
    return render(request, 'tweet_list.html', {
        'tweets': tweets,
        'form': form,
    })


@login_required
def tweet_create(request):
    if request.method == 'POST':
        form = TweetForm(request.POST, request.FILES)
        if form.is_valid():
            tweet = form.save(commit=False)
            tweet.user = request.user
            tweet.save()
            messages.success(request, 'Your tweet has been posted!')
            return redirect('tweet_list')
        else:
            messages.error(request, 'Failed to post tweet. Please check the form errors.')
    else:
        form = TweetForm()

    return render(request, 'tweet_form.html', {'form': form, 'is_create': True})


@login_required
def tweet_edit(request, tweet_id):
    tweet = get_object_or_404(Tweet, pk=tweet_id, user=request.user)
    if request.method == 'POST':
        form = TweetForm(request.POST, request.FILES, instance=tweet)
        if form.is_valid():
            form.save()
            messages.success(request, 'Tweet updated successfully!')
            return redirect('tweet_list')
        else:
            messages.error(request, 'Failed to update tweet. Please check the inputs.')
    else:
        form = TweetForm(instance=tweet)
    return render(request, 'tweet_form.html', {'form': form, 'tweet': tweet, 'is_create': False})


@login_required
def tweet_delete(request, tweet_id):
    tweet = get_object_or_404(Tweet, pk=tweet_id, user=request.user)
    if request.method == 'POST':
        tweet.delete()
        messages.success(request, 'Tweet deleted successfully.')
        return redirect('tweet_list')
    return render(request, 'tweet_confirm_delete.html', {'tweet': tweet})


def register(request):
    if request.user.is_authenticated:
        return redirect('tweet_list')

    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f'Welcome to Tweeter, @{user.username}!')
            return redirect('tweet_list')
        else:
            messages.error(request, 'Registration failed. Please correct the errors below.')
    else:
        form = UserRegistrationForm()

    return render(request, 'register.html', {'form': form})
