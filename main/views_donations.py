from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import DonationForm
from .models import Donation
from django.contrib import messages
from django.utils import timezone
from django.core.paginator import Paginator

@login_required
def donate(request):
    if request.method == 'POST':
        form = DonationForm(request.POST, request.FILES)
        if form.is_valid():
            donation = form.save(commit=False)
            donation.member = request.user
            donation.fund_type = 'Donations'
            donation.method = 'GCash'
            donation.status = 'Pending'
            donation.verified = False
            donation.save()

            messages.success(request, "Your GCash donation was submitted. Please wait for admin verification.")
            return redirect('history')
    else:
        form = DonationForm()

    return render(request, 'donations/donate.html', {'form': form})

@login_required
def history(request):
    donations_list = Donation.objects.filter(member=request.user).order_by('-created_at')

    paginator = Paginator(donations_list, 3)
    page_number = request.GET.get('page')
    donations = paginator.get_page(page_number)

    return render(request, 'donations/history.html', {'donations': donations})

# Optional: view for admin to verify via front-end (but admin can use /admin)
from django.contrib.admin.views.decorators import staff_member_required

@staff_member_required
def verify_donation(request, pk):
    donation = get_object_or_404(Donation, pk=pk)
    now = timezone.now()
    if not (6 <= now.hour < 22):
        messages.error(request, "Verification allowed only between 06:00 and 22:00.")
        return redirect('admin:index')  # or back to a custom dashboard
    donation.verified = True
    donation.verified_by = request.user
    donation.verified_at = now
    donation.save()
    messages.success(request, "Donation verified.")
    return redirect('admin:donations_donation_changelist')
