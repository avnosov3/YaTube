from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.cache import cache_page

from yatube.settings import POSTS_PER_PAGE
from .forms import PostForm, CommentForm
from .models import Group, Post, User, Follow


CACHE_TIME = 20


def paginator_get_page(request, post_list, num_list):
    return Paginator(post_list, num_list).get_page(request.GET.get('page'))


@cache_page(CACHE_TIME, key_prefix='index_page')
def index(request):
    return render(request, 'posts/index.html', {
        'page_obj': paginator_get_page(
            request, Post.objects.all(), POSTS_PER_PAGE),
    })


def group_posts(request, slug_name):
    group = get_object_or_404(Group, slug=slug_name)
    return render(request, 'posts/group_list.html', {
        'group': group,
        'page_obj': paginator_get_page(
            request, group.posts.all(), POSTS_PER_PAGE)
    })


def profile(request, username):
    author = get_object_or_404(User, username=username)
    following = (
        request.user.is_authenticated
        and request.user != author
        and author.follower.filter(
            user=request.user
        )
    )
    return render(request, 'posts/profile.html', {
        'author': author,
        'page_obj': paginator_get_page(
            request, author.posts.all(), POSTS_PER_PAGE),
        'following': following,
    })


def post_detail(request, post_id):
    return render(request, 'posts/post_detail.html', {
        'post': get_object_or_404(Post, id=post_id),
        'form': CommentForm(),
    })


@login_required
def post_create(request):
    form = PostForm(
        request.POST or None,
        files=request.FILES or None,
    )
    if not form.is_valid():
        return render(request, 'posts/create_post.html', {
            'form': form,
            'is_edit': False
        })
    post = form.save(False)
    post.author = request.user
    post.save()
    return redirect('posts:profile', request.user.username)


@login_required
def post_edit(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if post.author != request.user:
        return redirect('posts:index')
    form = PostForm(
        request.POST or None,
        files=request.FILES or None,
        instance=post,
    )
    if not form.is_valid():
        return render(request, 'posts/create_post.html', {
            'form': form,
            'is_edit': True
        })
    form.save()
    return redirect('posts:post_detail', post_id)


@login_required
def add_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    form = CommentForm(request.POST or None)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.author = request.user
        comment.post = post
        comment.save()
    return redirect('posts:post_detail', post_id=post_id)


@login_required
def follow_index(request):
    return render(request, 'posts/follow.html', {
        'page_obj': paginator_get_page(
            request, Post.objects.filter(author__following__user=request.user),
            POSTS_PER_PAGE)
    })


@login_required
def profile_follow(request, username):
    user = request.user
    author = get_object_or_404(User, username=username)
    follower = Follow.objects.filter(user=user, author=author)
    if user.username != username and not follower.exists():
        Follow.objects.create(user=user, author=author)
    return redirect('posts:profile', username=author)


@login_required
def profile_unfollow(request, username):
    get_object_or_404(
        Follow,
        user=request.user,
        author__username=username).delete()
    return redirect('posts:profile', username)
