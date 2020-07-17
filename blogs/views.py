from django.http import HttpResponse
from django.shortcuts import render

from blogs.models import Tag, Post, Category


def post_list(request, category_id=None, tag_id=None):
    """使用Model从数据库中批量拿取数据，然后把标题和摘要展示到页面上"""
    tag = None
    category = None

    if tag_id:
        try:
            tag = Tag.objects.get(id=tag_id)
        except Tag.DoesNotExist:
            post_list = []
        else:
            post_list = tag.post_set.filter(status=Post.STATUS_NORMAL)
    else:
        post_list = Post.objects.filter(status=Post.STATUS_NORMAL)
        if category_id:
            try:
                category = Category.objects.get(id=category_id)
            except Category.DoesNotExist:
                category = None
            else:
                post_list = post_list.filter(category_id=category_id)

    context = {
        'category': category,
        'tag': tag,
        'post_list': post_list,
    }

    return render(request, 'blogs/list.html', context=context)


def post_detail(request, post_id):
    """只展示一条数据"""
    try:
        post = Post.objects.get(id=post_id)
    except Post.DoesNotExist:
        post = None

    return render(request, 'blogs/detail.html', context={'post': post})