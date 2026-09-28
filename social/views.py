from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from .models import Profile, Post, Like, Comment, Follow


def register(request):

    if request.method == 'POST':

        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']

        if User.objects.filter(username=username).exists():

            messages.error(
                request,
                'Username already exists.'
            )

            return redirect('register')

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password
        )

        Profile.objects.create(
            user=user
        )

        login(request, user)

        return redirect(
            'profile',
            username=user.username
        )

    return render(
        request,
        'social/register.html'
    )


def user_login(request):

    if request.method == 'POST':

        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:

            login(request, user)

            return redirect('feed')

        messages.error(
            request,
            'Invalid username or password.'
        )

    return render(
        request,
        'social/login.html'
    )


def user_logout(request):

    logout(request)

    return redirect('login')


def profile(request, username):

    user = get_object_or_404(
        User,
        username=username
    )

    profile, created = Profile.objects.get_or_create(
        user=user
    )

    posts = Post.objects.filter(
        user=user
    ).order_by('-created_at')

    return render(
        request,
        'social/profile.html',
        {
            'profile_user': user,
            'profile': profile,
            'posts': posts
        }
    )


def feed(request):

    if not request.user.is_authenticated:
        return redirect('login')

    following_users = Follow.objects.filter(
        follower=request.user
    ).values_list(
        'following',
        flat=True
    )

    posts = Post.objects.filter(
        user__in=list(following_users) + [request.user.id]
    ).order_by('-created_at')

    return render(
        request,
        'social/feed.html',
        {
            'posts': posts
        }
    )


def create_post(request):

    if not request.user.is_authenticated:
        return redirect('login')

    if request.method == 'POST':

        content = request.POST['content']

        image = request.FILES.get('image')

        Post.objects.create(
            user=request.user,
            content=content,
            image=image
        )

        return redirect('feed')

    return render(
        request,
        'social/create_post.html'
    )


def edit_post(request, post_id):

    if not request.user.is_authenticated:
        return redirect('login')

    post = get_object_or_404(
        Post,
        id=post_id,
        user=request.user
    )

    if request.method == 'POST':

        post.content = request.POST['content']

        if request.FILES.get('image'):
            post.image = request.FILES.get('image')

        post.save()

        return redirect('feed')

    return render(
        request,
        'social/edit_post.html',
        {
            'post': post
        }
    )


def delete_post(request, post_id):

    if not request.user.is_authenticated:
        return redirect('login')

    post = get_object_or_404(
        Post,
        id=post_id,
        user=request.user
    )

    post.delete()

    return redirect('feed')

def like_post(request, post_id):

    if not request.user.is_authenticated:
        return redirect('login')

    post = get_object_or_404(
        Post,
        id=post_id
    )

    like = Like.objects.filter(
        user=request.user,
        post=post
    ).first()

    if like:
        like.delete()
    else:
        Like.objects.create(
            user=request.user,
            post=post
        )

    return redirect('feed')
def add_comment(request, post_id):

    if not request.user.is_authenticated:
        return redirect('login')

    post = get_object_or_404(
        Post,
        id=post_id
    )

    if request.method == 'POST':

        text = request.POST['text']

        if text.strip():

            Comment.objects.create(
                user=request.user,
                post=post,
                text=text
            )

    return redirect('feed')
def follow_user(request, username):

    if not request.user.is_authenticated:
        return redirect('login')

    target_user = get_object_or_404(
        User,
        username=username
    )

    if target_user != request.user:

        follow = Follow.objects.filter(
            follower=request.user,
            following=target_user
        ).first()

        if follow:
            follow.delete()

        else:
            Follow.objects.create(
                follower=request.user,
                following=target_user
            )

    return redirect(
        'profile',
        username=username
    )
def followers_list(request, username):

    user = get_object_or_404(
        User,
        username=username
    )

    followers = Follow.objects.filter(
        following=user
    )

    return render(
        request,
        'social/followers.html',
        {
            'profile_user': user,
            'followers': followers
        }
    )


def following_list(request, username):

    user = get_object_or_404(
        User,
        username=username
    )

    following = Follow.objects.filter(
        follower=user
    )

    return render(
        request,
        'social/following.html',
        {
            'profile_user': user,
            'following': following
        }
    )