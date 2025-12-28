from django.shortcuts import render
from .models import Announcement
from django.core.paginator import Paginator

def list_announcements(request):
    announcements_list = Announcement.objects.filter(is_active=True).order_by('-publish_date')
    paginator = Paginator(announcements_list, 3)
    page_number = request.GET.get('page')
    print("Pagination working — current page:", page_number)
    announcements = paginator.get_page(page_number)
    return render(request, 'announcements/list.html', {'announcements': announcements})
