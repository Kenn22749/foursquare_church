from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from .models import Ministry, VolunteerAssignment
from django.contrib.auth.decorators import login_required
from django.contrib import messages

def list_ministries(request):
    # Only show active ministries
    ministries_list = Ministry.objects.filter(is_active=True).order_by('id')

    # Paginate — e.g., 3 cards per page
    paginator = Paginator(ministries_list, 3)
    page_number = request.GET.get('page')
    ministries = paginator.get_page(page_number)

    return render(request, 'ministries/list.html', {'ministries': ministries})


@login_required
def join_ministry(request, pk):
    ministry = get_object_or_404(Ministry, pk=pk)
    if VolunteerAssignment.objects.filter(ministry=ministry, member=request.user).exists():
        messages.info(request, "You are already joined in this activity.")
    else:
        VolunteerAssignment.objects.create(ministry=ministry, member=request.user)
        messages.success(request, "You successfully joined this activity.")
    return redirect('ministries-list')


@login_required
def my_assignments(request):
    assignments = VolunteerAssignment.objects.filter(member=request.user)
    return render(request, 'ministries/my_assignments.html', {'assignments': assignments})
