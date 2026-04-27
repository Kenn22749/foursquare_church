from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import user_passes_test
from django.contrib import messages
from .models import Announcement
from .models import Event
from .models import Ministry
from django.utils import timezone
from .models import MemberProfile
from django.contrib.auth.models import User
from django.db.models import Sum


def admin_only(user):
    return user.is_superuser or user.is_staff

# -----------------------
#   MEMBERPROFILE CRUD
# -----------------------

@user_passes_test(admin_only)
def admin_memberprofile_list(request):
    members = MemberProfile.objects.select_related('user').order_by('user__username')
    return render(request, 'admin_ui/memberprofile/list.html', {
        'members': members
    })


@user_passes_test(admin_only)
def admin_memberprofile_edit(request, pk):
    profile = get_object_or_404(MemberProfile, pk=pk)

    if request.method == 'POST':
        profile.first_name = request.POST.get('first_name')
        profile.middle_name = request.POST.get('middle_name')
        profile.last_name = request.POST.get('last_name')
        profile.suffix = request.POST.get('suffix')
        profile.email_address = request.POST.get('email_address')
        profile.relationship_status = request.POST.get('relationship_status')
        profile.contact_number = request.POST.get('contact_number')
        profile.birth_date = request.POST.get('birth_date') or None
        profile.address = request.POST.get('address')

        if 'photo' in request.FILES:
            profile.photo = request.FILES['photo']

        profile.save()

        messages.success(request, "Member profile updated successfully.")
        return redirect('admin-memberprofile-list')

    return render(request, 'admin_ui/memberprofile/edit.html', {
        'profile': profile
    })


@user_passes_test(admin_only)
def admin_memberprofile_delete(request, pk):
    profile = MemberProfile.objects.filter(pk=pk).first()
    if profile:
        profile.delete()
        messages.success(request, "Member profile deleted successfully.")
    else:
        messages.info(request, "Member profile does not exist.")
    return redirect('admin-memberprofile-list')

@user_passes_test(admin_only)
def admin_memberprofile_approve(request, pk):
    profile = get_object_or_404(MemberProfile, pk=pk)

    profile.user.is_active = True
    profile.user.save()

    messages.success(request, "Member account approved successfully.")
    return redirect('admin-memberprofile-list')


# -----------------------
#   MINISTRIES CRUD
# -----------------------

@user_passes_test(admin_only)
def admin_ministry_list(request):
    ministries = Ministry.objects.order_by('name')
    return render(request, 'admin_ui/ministries/list.html', {
        'ministries': ministries
    })


@user_passes_test(admin_only)
def admin_ministry_add(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')
        coordinator = request.POST.get('coordinator')
        is_active = bool(request.POST.get('is_active'))

        Ministry.objects.create(
            name=name,
            description=description,
            coordinator=coordinator,
            is_active=is_active
        )

        messages.success(request, "Ministry created successfully.")
        return redirect('admin-ministry-list')

    return render(request, 'admin_ui/ministries/add.html')


@user_passes_test(admin_only)
def admin_ministry_edit(request, pk):
    ministry = get_object_or_404(Ministry, pk=pk)

    if request.method == 'POST':
        ministry.name = request.POST.get('name')
        ministry.description = request.POST.get('description')
        ministry.coordinator = request.POST.get('coordinator')
        ministry.is_active = bool(request.POST.get('is_active'))
        ministry.save()

        messages.success(request, "Ministry updated successfully.")
        return redirect('admin-ministry-list')

    return render(request, 'admin_ui/ministries/edit.html', {
        'ministry': ministry
    })


@user_passes_test(admin_only)
def admin_ministry_delete(request, pk):
    ministry = get_object_or_404(Ministry, pk=pk)

    ministry.delete()
    messages.success(request, "Ministry deleted successfully.")
    return redirect('admin-ministry-list')


@user_passes_test(admin_only)
def admin_event_list(request):
    events = Event.objects.order_by('-date', '-time')
    return render(request, 'admin_ui/events/list.html', {'events': events})

@user_passes_test(admin_only)
def admin_event_add(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        date = request.POST.get('date')
        time = request.POST.get('time')
        location = request.POST.get('location')
        capacity = request.POST.get('capacity')
        is_active = bool(request.POST.get('is_active'))

        Event.objects.create(
            title=title,
            description=description,
            date=date,
            time=time if time else None,
            location=location,
            capacity=capacity if capacity else None,
            is_active=is_active,
            created_by=request.user
        )
        messages.success(request, 'Event created successfully!')
        return redirect('admin-event-list')

    return render(request, 'admin_ui/events/add.html')

@user_passes_test(admin_only)
def admin_event_edit(request, pk):
    event = get_object_or_404(Event, pk=pk)
    if request.method == 'POST':
        event.title = request.POST.get('title')
        event.description = request.POST.get('description')
        event.date = request.POST.get('date')
        event.time = request.POST.get('time') if request.POST.get('time') else None
        event.location = request.POST.get('location')
        event.capacity = request.POST.get('capacity') if request.POST.get('capacity') else None
        event.is_active = bool(request.POST.get('is_active'))
        event.save()
        messages.success(request, 'Event updated successfully!')
        return redirect('admin-event-list')

    return render(request, 'admin_ui/events/edit.html', {'event': event})

@user_passes_test(admin_only)
def admin_event_delete(request, pk):
    event = get_object_or_404(Event, pk=pk)
    event.delete()
    messages.success(request, 'Event deleted successfully!')
    return redirect('admin-event-list')




@user_passes_test(admin_only)
def admin_announcement_list(request):
    announcements = Announcement.objects.order_by('-publish_date')
    return render(request, 'admin_ui/announcements/list.html', {
        'announcements': announcements
    })


@user_passes_test(admin_only)
def admin_announcement_add(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        is_active = bool(request.POST.get('is_active'))

        Announcement.objects.create(
            title=title,
            content=content,
            created_by=request.user,
            is_active=is_active
        )

        messages.success(request, 'Announcement created successfully!')
        return redirect('admin-announcement-list')

    return render(request, 'admin_ui/announcements/add.html')


@user_passes_test(admin_only)
def admin_announcement_edit(request, pk):
    announcement = get_object_or_404(Announcement, pk=pk)

    if request.method == 'POST':
        announcement.title = request.POST.get('title')
        announcement.content = request.POST.get('content')
        announcement.is_active = bool(request.POST.get('is_active'))
        announcement.save()

        messages.success(request, 'Announcement updated!')
        return redirect('admin-announcement-list')

    return render(request, 'admin_ui/announcements/edit.html', {
        'announcement': announcement
    })


@user_passes_test(admin_only)
def admin_announcement_delete(request, pk):
    announcement = get_object_or_404(Announcement, pk=pk)
    announcement.delete()
    messages.success(request, 'Announcement deleted.')
    return redirect('admin-announcement-list')


@user_passes_test(lambda u: u.is_superuser or u.is_staff)
def admin_dashboard(request):
    return render(request, 'admin_ui/dashboard.html')


# -----------------------
#   FUND TRACKING
# -----------------------

from .models import Donation

@user_passes_test(admin_only)
def admin_fundtracking_list(request):
    fund_type = request.GET.get('type', 'All')

    donations = Donation.objects.select_related('member').order_by('-created_at')

    if fund_type == 'Donation':
        donations = donations.filter(fund_type='Donation')

    elif fund_type == 'Offering':
        donations = donations.filter(fund_type='Offering')

    total_amount = donations.aggregate(
        total=Sum('amount')
    )['total'] or 0

    return render(request, 'admin_ui/fund_tracking/list.html', {
        'donations': donations,
        'selected_type': fund_type,
        'total_amount': total_amount,
    })


@user_passes_test(admin_only)
def admin_fundtracking_verify(request, pk):
    donation = get_object_or_404(Donation, pk=pk)

    donation.status = 'Verified'
    donation.verified = True
    donation.verified_by = request.user
    donation.verified_at = timezone.now()
    donation.save()

    messages.success(request, "Transaction verified successfully.")
    return redirect('admin-fundtracking-list')


@user_passes_test(admin_only)
def admin_fundtracking_reject(request, pk):
    donation = get_object_or_404(Donation, pk=pk)

    donation.status = 'Rejected'
    donation.verified = False
    donation.verified_by = request.user
    donation.verified_at = timezone.now()
    donation.save()

    messages.success(request, "Transaction rejected.")
    return redirect('admin-fundtracking-list')

@user_passes_test(admin_only)
def admin_fundtracking_reset(request, pk):
    donation = get_object_or_404(Donation, pk=pk)

    donation.status = "Pending"
    donation.verified = False
    donation.verified_by = None
    donation.verified_at = None
    donation.save()

    messages.success(request, "Donation status reset to Pending.")
    return redirect('admin-fundtracking-list')