from decimal import Decimal, InvalidOperation

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import user_passes_test
from django.contrib import messages
from django.contrib.auth.models import User
from django.utils import timezone
from django.db.models import Sum
from django.core.paginator import Paginator

from .models import Announcement, Event, Ministry, MemberProfile, Donation, EventRegistration, VolunteerAssignment


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
#   ACTIVITIES CRUD
# -----------------------

@user_passes_test(admin_only)
def admin_ministry_list(request):
    ministries = Ministry.objects.order_by('name')
    return render(request, 'admin_ui/ministries/list.html', {
        'ministries': ministries
    })

@user_passes_test(admin_only)
def admin_ministry_volunteers(request, pk):
    ministry = get_object_or_404(Ministry, pk=pk)
    volunteers = VolunteerAssignment.objects.filter(ministry=ministry).select_related("member").order_by("-assigned_at")

    return render(request, "admin_ui/ministries/volunteers.html", {
        "ministry": ministry,
        "volunteers": volunteers,
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

        messages.success(request, "Activity created successfully.")
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

        messages.success(request, "Activity updated successfully.")
        return redirect('admin-ministry-list')

    return render(request, 'admin_ui/ministries/edit.html', {
        'ministry': ministry
    })


@user_passes_test(admin_only)
def admin_ministry_delete(request, pk):
    ministry = get_object_or_404(Ministry, pk=pk)
    ministry.delete()

    messages.success(request, "Activity deleted successfully.")
    return redirect('admin-ministry-list')


# -----------------------
#   EVENTS CRUD
# -----------------------

@user_passes_test(admin_only)
def admin_event_list(request):
    events = Event.objects.order_by('-date', '-time')
    return render(request, 'admin_ui/events/list.html', {
        'events': events
    })

@user_passes_test(admin_only)
def admin_event_registrants(request, pk):
    event = get_object_or_404(Event, pk=pk)
    registrants = EventRegistration.objects.filter(event=event).select_related("member").order_by("-registered_at")

    return render(request, "admin_ui/events/registrants.html", {
        "event": event,
        "registrants": registrants,
    })


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

    return render(request, 'admin_ui/events/edit.html', {
        'event': event
    })


@user_passes_test(admin_only)
def admin_event_delete(request, pk):
    event = get_object_or_404(Event, pk=pk)
    event.delete()

    messages.success(request, 'Event deleted successfully!')
    return redirect('admin-event-list')


# -----------------------
#   ANNOUNCEMENTS CRUD
# -----------------------

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


# -----------------------
#   ADMIN DASHBOARD
# -----------------------

@user_passes_test(admin_only)
def admin_dashboard(request):
    return render(request, 'admin_ui/dashboard.html')


# -----------------------
#   FUND TRACKING
# -----------------------

@user_passes_test(admin_only)
def admin_fundtracking_list(request):
    selected_method = request.GET.get("method", "All")

    donations = Donation.objects.select_related("member").order_by("-created_at")

    if selected_method == "Cash":
        donations = donations.filter(method="Cash")
    elif selected_method == "GCash":
        donations = donations.filter(method="GCash")

    # ✅ ADD PAGINATION (15 per page)
    paginator = Paginator(donations, 15)
    page_number = request.GET.get("page")
    donations = paginator.get_page(page_number)

    verified_donations = Donation.objects.filter(status="Verified")

    total_amount = verified_donations.aggregate(total=Sum("amount"))["total"] or 0
    total_cash = verified_donations.filter(method="Cash").aggregate(total=Sum("amount"))["total"] or 0
    total_gcash = verified_donations.filter(method="GCash").aggregate(total=Sum("amount"))["total"] or 0

    return render(request, "admin_ui/fund_tracking/list.html", {
        "donations": donations,
        "total_amount": total_amount,
        "total_cash": total_cash,
        "total_gcash": total_gcash,
        "selected_method": selected_method,
    })


@user_passes_test(admin_only)
def admin_fundtracking_add(request):
    members = User.objects.filter(
        is_staff=False,
        is_superuser=False
    ).order_by("username")

    if request.method == "POST":
        member_id = request.POST.get("member")
        donor_name = request.POST.get("donor_name", "").strip()
        amount_input = request.POST.get("amount", "").strip()

        if not member_id and not donor_name:
            messages.error(
                request,
                "Please select a registered member or type an unregistered donor name."
            )
            return render(request, "admin_ui/fund_tracking/add.html", {
                "members": members
            })

        if not amount_input:
            messages.error(request, "Amount is required.")
            return render(request, "admin_ui/fund_tracking/add.html", {
                "members": members
            })

        try:
            amount = Decimal(amount_input)
        except InvalidOperation:
            messages.error(request, "Invalid amount.")
            return render(request, "admin_ui/fund_tracking/add.html", {
                "members": members
            })

        Donation.objects.create(
            member_id=member_id if member_id else None,
            donor_name=donor_name,
            fund_type="Donations",
            amount=amount,
            method="Cash",
            status="Verified",
            verified=True,
            verified_by=request.user,
            verified_at=timezone.now()
        )

        messages.success(request, "Cash transaction added successfully.")
        return redirect("admin-fundtracking-list")

    return render(request, "admin_ui/fund_tracking/add.html", {
        "members": members
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

@user_passes_test(admin_only)
def admin_fundtracking_delete(request, pk):
    donation = get_object_or_404(Donation, pk=pk)
    donation.delete()
    messages.success(request, "Transaction deleted successfully.")
    return redirect("admin-fundtracking-list")


@user_passes_test(admin_only)
def admin_fundtracking_edit(request, pk):
    donation = get_object_or_404(Donation, pk=pk)
    members = User.objects.filter(
        is_staff=False,
        is_superuser=False
    ).order_by("username")

    if request.method == "POST":
        donation.member_id = request.POST.get("member") or None
        donation.donor_name = request.POST.get("donor_name", "").strip()
        donation.amount = request.POST.get("amount")

        if not donation.status:
            donation.status = "Verified"

        if donation.method == "Cash":
            donation.status = "Verified"
            donation.verified = True
            donation.verified_by = request.user
            donation.verified_at = timezone.now()
        else:
            donation.status = donation.status or "Pending"

        donation.save()

        messages.success(request, "Transaction updated successfully.")
        return redirect("admin-fundtracking-list")

    return render(request, "admin_ui/fund_tracking/edit.html", {
        "donation": donation,
        "members": members
    })