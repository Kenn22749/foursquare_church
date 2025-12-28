from django.contrib import admin
from .models import (
    Ministry, VolunteerAssignment, Announcement,
    MemberProfile, Event, EventRegistration, Donation
)
from django.utils.html import format_html

class DonationAdmin(admin.ModelAdmin):
    list_display = ('member', 'amount', 'method', 'verified', 'created_at', 'receipt_preview')
    list_filter = ('method', 'verified')
    search_fields = ('member__username',)
    readonly_fields = ('receipt_preview',)

    def receipt_preview(self, obj):
        if obj.receipt_image:
            return format_html('<img src="{}" style="max-height:120px;"/>', obj.receipt_image.url)
        return '(No image)'
    receipt_preview.short_description = 'Receipt'


@admin.register(MemberProfile)
class MemberProfileAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'first_name', 'middle_name', 'last_name', 'suffix',
        'email_address',
        'relationship_status', 'contact_number',
    )
    search_fields = (
        'user__username',
        'first_name',
        'last_name',
        'email_address',
        'contact_number',
    )
    list_filter = ('relationship_status',)
    ordering = ('user',)


admin.site.register(Donation, DonationAdmin)
admin.site.register(Announcement)
admin.site.register(Event)
admin.site.register(EventRegistration)
admin.site.register(Ministry)
admin.site.register(VolunteerAssignment)
