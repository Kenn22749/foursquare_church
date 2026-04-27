from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from .forms import UserRegisterForm, MemberProfileForm
from .models import MemberProfile, Event, Announcement


def home(request):
    announcements = Announcement.objects.filter(is_active=True).order_by('-publish_date')[:3]
    events = Event.objects.filter(is_active=True).order_by('date')[:3]
    return render(request, 'members/home.html', {
        'announcements': announcements,
        'events': events,
    })


def register(request):
    if request.method == 'POST':
        uform = UserRegisterForm(request.POST)
        pform = MemberProfileForm(request.POST, request.FILES)

        if uform.is_valid() and pform.is_valid():
            user = uform.save(commit=False)
            user.set_password(uform.cleaned_data['password'])
            user.is_active = False
            user.save()

            profile = pform.save(commit=False)
            profile.user = user

            # If user entered email, copy it to MemberProfile email_address
            profile.email_address = user.email or ""

            profile.save()

            messages.success(
                request,
                "Registration submitted. Please wait for admin approval before logging in."
            )
            return redirect('login')
    else:
        uform = UserRegisterForm()
        pform = MemberProfileForm()

    return render(request, 'members/register.html', {
        'uform': uform,
        'pform': pform
    })


def login_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        try:
            user_obj = User.objects.get(username=username)
        except User.DoesNotExist:
            user_obj = None

        if user_obj is not None and not user_obj.is_active:
            messages.error(request, "Your account is still pending admin approval.")
            return redirect('login')

        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)

            if user.is_superuser or user.is_staff or user.username.lower() == 'admin':
                return redirect('admin_dashboard')

            return redirect('dashboard')
        else:
            messages.error(request, "Invalid credentials.")

    return render(request, 'members/login.html')


@login_required
def dashboard(request):
    events_count = request.user.eventregistration_set.count() if hasattr(request.user, 'eventregistration_set') else 0
    donations_count = request.user.donation_set.count() if hasattr(request.user, 'donation_set') else 0
    ministries_count = request.user.volunteerassignment_set.count() if hasattr(request.user, 'volunteerassignment_set') else 0
    return render(request, 'members/dashboard.html', {
        'events_count': events_count,
        'donations_count': donations_count,
        'ministries_count': ministries_count,
    })


@login_required
def edit_profile(request):
    profile, _ = MemberProfile.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        form = MemberProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated.")
            return redirect('dashboard')
    else:
        form = MemberProfileForm(instance=profile)
    return render(request, 'members/edit_profile.html', {'form': form})


def logout_user(request):
    logout(request)
    return redirect('home')


# ✅ ADMIN DASHBOARD VIEW
@login_required
def admin_dashboard(request):
    # Optional: restrict access to only admin or staff users
    if not (request.user.is_staff or request.user.is_superuser or request.user.username.lower() == 'admin'):
        messages.error(request, "You are not authorized to access the admin dashboard.")
        return redirect('dashboard')

    # Example admin stats (you can expand this later)
    total_users = User.objects.count()
    total_events = Event.objects.count()
    total_announcements = Announcement.objects.count()

    return render(request, 'admin_ui/admin_dashboard.html', {
        'total_users': total_users,
        'total_events': total_events,
        'total_announcements': total_announcements,
    })
