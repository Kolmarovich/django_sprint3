from django.shortcuts import get_object_or_404, render
from django.utils import timezone

from blog.models import Category, Post


def get_posts(category_slug=None):
    posts = Post.objects.filter(
        is_published=True,
        category__is_published=True,
        pub_date__date__lte=timezone.now()
    )
    if category_slug:
        posts = posts.filter(category__slug=category_slug)
    return posts


def index(request):
    template = 'blog/index.html'
    post_list = get_posts()[:5]
    context = {'post_list': post_list}
    return render(request, template, context)


def post_detail(request, id):
    template = 'blog/detail.html'
    post = get_object_or_404(get_posts(), pk=id)
    context = {'post': post}
    return render(request, template, context)


def category_posts(request, category_slug):
    template = 'blog/category.html'
    category = get_object_or_404(Category.objects.values('title',
                                                         'description').filter(
        slug=category_slug,
        is_published=True
    ))

    post_list = get_posts(category_slug=category_slug)

    context = {
        'category': category,
        'post_list': post_list
    }
    return render(request, template, context)
