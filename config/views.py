from django.views.generic import ListView

from blogs.views import CommonViewMixin
from config.models import Link


class LinkListView(CommonViewMixin, ListView):
    queryset = Link.objects.filter(status=Link.STATUS_NORMAL)

# def links(request):
#     return HttpResponse('links')