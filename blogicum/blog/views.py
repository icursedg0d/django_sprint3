from django.utils import timezone

from django.http import Http404
from django.shortcuts import render, get_object_or_404
from .models import Post, Category


def index(request):
    template = "blog/index.html"
    # Фильтрация публикаций согласно условиям
    context = (
        Post.objects.filter(
            is_published=True, category__is_published=True, pub_date__lte=timezone.now()
        )
        .order_by("-pub_date")[:5]
        .select_related("category")
    )
    return render(request, template, {"posts": context})


def post_detail(request, pk):
    template = "blog/detail.html"
    post = get_object_or_404(Post, pk=pk, is_published=True)
    return render(request, template, {"post": post})


def category_posts(request, category_slug):
    template = "blog/category.html"
    category = get_object_or_404(Category, slug=category_slug, is_published=True)
    posts = Post.objects.filter(
        category=category,
        is_published=True,
        category__is_published=True,
    ).order_by("-pub_date")
    return render(request, template, {"category": category})
