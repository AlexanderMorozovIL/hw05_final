from django.conf import settings
from django.core.paginator import Paginator


def split_page_to_page_pagination(request, posts):
    paginator = Paginator(posts, settings.POSTS_AMOUNT)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return page_obj
