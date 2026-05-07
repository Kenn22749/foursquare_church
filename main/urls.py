from django.urls import path
from . import views_announce
from . import views_donations
from . import views_events
from . import views_members
from . import views_ministry
from . import views_admin

urlpatterns = [
    path('announcements/', views_announce.list_announcements, name='announcements-list'),

    path('donate/', views_donations.donate, name='donations-donate'),
    path('history/', views_donations.history, name='history'),
    path('verify/<int:pk>/', views_donations.verify_donation, name='verify'),

    path('events/', views_events.event_list, name='events-list'),
    path('events/<int:pk>/', views_events.event_detail, name='events-detail'),
    path('events/<int:pk>/register/', views_events.register_event, name='events-register'),
    path('events/my/', views_events.my_registrations, name='events-my'),

    path('', views_members.home, name='home'),
    path('register/', views_members.register, name='register'),
    path('login/', views_members.login_user, name='login'),
    path('logout/', views_members.logout_user, name='logout'),
    path('dashboard/', views_members.dashboard, name='dashboard'),
    path('profile/edit/', views_members.edit_profile, name='edit_profile'),

    
    path('admin_dashboard/', views_admin.admin_dashboard, name='admin_dashboard'),


    path('ministries/', views_ministry.list_ministries, name='ministries-list'),
    path('ministries/<int:pk>/join/', views_ministry.join_ministry, name='ministries-join'),
    path('ministries/my/', views_ministry.my_assignments, name='ministries-my'),


    # Custom Admin UI – Announcements
path('admin_ui/announcements/', views_admin.admin_announcement_list, name='admin-announcement-list'),
path('admin_ui/announcements/add/', views_admin.admin_announcement_add, name='admin-announcement-add'),
path('admin_ui/announcements/<int:pk>/edit/', views_admin.admin_announcement_edit, name='admin-announcement-edit'),
path('admin_ui/announcements/<int:pk>/delete/', views_admin.admin_announcement_delete, name='admin-announcement-delete'),

# Admin CRUD for Events
path('admin_ui/events/', views_admin.admin_event_list, name='admin-event-list'),
path('admin_ui/events/<int:pk>/registrants/', views_admin.admin_event_registrants, name='admin-event-registrants'),
path('admin_ui/events/add/', views_admin.admin_event_add, name='admin-event-add'),
path('admin_ui/events/<int:pk>/edit/', views_admin.admin_event_edit, name='admin-event-edit'),
path('admin_ui/events/<int:pk>/delete/', views_admin.admin_event_delete, name='admin-event-delete'),

# Admin CRUD for Ministries
path('admin_ui/ministries/', views_admin.admin_ministry_list, name='admin-ministry-list'),
path('admin_ui/ministries/<int:pk>/volunteers/', views_admin.admin_ministry_volunteers, name='admin-ministry-volunteers'),
path('admin_ui/ministries/add/', views_admin.admin_ministry_add, name='admin-ministry-add'),
path('admin_ui/ministries/<int:pk>/edit/', views_admin.admin_ministry_edit, name='admin-ministry-edit'),
path('admin_ui/ministries/<int:pk>/delete/', views_admin.admin_ministry_delete, name='admin-ministry-delete'),

# Admin CRUD for Member Profiles
path('admin_ui/members/', views_admin.admin_memberprofile_list, name='admin-memberprofile-list'),
path('admin_ui/members/<int:pk>/edit/', views_admin.admin_memberprofile_edit, name='admin-memberprofile-edit'),
path('admin_ui/members/<int:pk>/delete/', views_admin.admin_memberprofile_delete, name='admin-memberprofile-delete'),

path('admin_ui/fund-tracking/', views_admin.admin_fundtracking_list, name='admin-fundtracking-list'),
path('admin_ui/fund-tracking/<int:pk>/verify/', views_admin.admin_fundtracking_verify, name='admin-fundtracking-verify'),
path('admin_ui/fund-tracking/<int:pk>/reject/', views_admin.admin_fundtracking_reject, name='admin-fundtracking-reject'),
path('admin_ui/fund-tracking/reset/<int:pk>/', views_admin.admin_fundtracking_reset, name='admin-fundtracking-reset'),
path('admin_ui/fund-tracking/add/', views_admin.admin_fundtracking_add, name='admin-fundtracking-add'),
path('admin_ui/fund-tracking/<int:pk>/edit/', views_admin.admin_fundtracking_edit, name='admin-fundtracking-edit'),
path('admin_ui/fund-tracking/<int:pk>/delete/', views_admin.admin_fundtracking_delete, name='admin-fundtracking-delete'),


path(
    'admin_ui/members/<int:pk>/approve/', views_admin.admin_memberprofile_approve, name='admin-memberprofile-approve'),

]
