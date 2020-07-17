from django.http import HttpResponse
from django.shortcuts import render


def post_list(request, category_id=None, tag_id=None):
    # content = 'post_list category_id={category_id}, tag_id={tag_id}'.format(
    #     category_id=category_id,
    #     tag_id=tag_id,
    # )
    # return HttpResponse(content)
    return render(request, 'blogs/list.html', context={'name': 'post_list'})


def post_detail(request, post_id):
    # return HttpResponse('detail')
    return render(request, 'blogs/detail.html', context={'name': 'post_detail'})