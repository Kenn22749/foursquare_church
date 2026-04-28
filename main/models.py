from django.db import models
from django.contrib.auth.models import User

class MemberProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    
    first_name = models.CharField(max_length=100, blank=True)
    middle_name = models.CharField(max_length=100, blank=True)
    last_name = models.CharField(max_length=100, blank=True)
    suffix = models.CharField(max_length=20, blank=True)
    email_address = models.EmailField(blank=True) 

    RELATIONSHIP_CHOICES = [
        ('single', 'Single'),
        ('married', 'Married'),
        ('widowed', 'Widowed'),
        ('divorced', 'Divorced'),
        ('separated', 'Separated'),
        ('other', 'Other'),
    ]
    relationship_status = models.CharField(max_length=20, choices=RELATIONSHIP_CHOICES, blank=True)

    contact_number = models.CharField(max_length=20, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    address = models.TextField(blank=True)
    photo = models.ImageField(upload_to='profiles/', null=True, blank=True)

    def __str__(self):
        return self.user.username


class Announcement(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    publish_date = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.title

class Donation(models.Model):
    FUND_TYPE_CHOICES = [
    ('Donations', 'Donations'),
    ]

    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Verified', 'Verified'),
        ('Rejected', 'Rejected'),
    ]

    member = models.ForeignKey(User, on_delete=models.CASCADE)
    fund_type = models.CharField(max_length=50, choices=FUND_TYPE_CHOICES, default='Donations')
    amount = models.DecimalField(max_digits=10, decimal_places=2)

    method = models.CharField(max_length=10, default='GCash')
    receipt_image = models.ImageField(upload_to='donation_receipts/', null=True, blank=True)

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    verified = models.BooleanField(default=False)
    verified_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='verified_donations'
    )
    verified_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.member.username} - {self.fund_type} - ₱{self.amount}"
    
class Event(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    date = models.DateField()
    time = models.TimeField(null=True, blank=True)
    location = models.CharField(max_length=200, blank=True)
    capacity = models.PositiveIntegerField(null=True, blank=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.title} - {self.date}"

class EventRegistration(models.Model):
    STATUS_CHOICES = [('registered', 'Registered'), ('confirmed', 'Confirmed'), ('cancelled', 'Cancelled')]
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    member = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='registered')
    registered_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('event', 'member')

    def __str__(self):
        return f"{self.member.username} -> {self.event.title}"
        
class Ministry(models.Model):
    name = models.CharField(max_length=150)
    description = models.TextField(blank=True)
    coordinator = models.CharField(max_length=100, blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

class VolunteerAssignment(models.Model):
    STATUS = [('assigned','Assigned'), ('completed','Completed'), ('cancelled','Cancelled')]
    ministry = models.ForeignKey(Ministry, on_delete=models.CASCADE)
    member = models.ForeignKey(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=100, blank=True)
    schedule_start = models.DateTimeField(null=True, blank=True)
    schedule_end = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS, default='assigned')
    assigned_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('ministry','member')

    def __str__(self):
        return f"{self.member.username} - {self.ministry.name}"
