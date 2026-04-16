from django.urls import path
from . import views

urlpatterns = [
    # Landing page
    path('', views.landing_page, name='landing_page'),
    
    # Demo routes (no authentication required)
    path('demo/', views.demo_upload, name='demo_upload'),
    
    # Dashboard routes
    path('dashboard/', views.dashboard_router, name='dashboard_router'),
    path('dashboard/regular/', views.regular_user_dashboard, name='regular_user_dashboard'),
    path('dashboard/business/', views.business_owner_dashboard, name='business_owner_dashboard'),
    
    # Authentication routes
    path('login/', views.user_login, name='user_login'),
    path('register/', views.user_register, name='user_register'),
    path('logout/', views.user_logout, name='user_logout'),
    
    # Upload routes`
    path('upload/', views.upload_image, name='upload_image'),
    path('upload/regular/', views.regular_user_upload, name='regular_user_upload'),
    path('handle-regular-upload/', views.handle_regular_user_upload, name='handle_regular_user_upload'),
    path('debug-role/', views.debug_user_role, name='debug_user_role'),
    path('dashboard/business/upload/', views.business_owner_upload, name='business_owner_upload'),
    path('progress/<str:session_id>/', views.get_progress, name='get_progress'),
    
    # Business owner request
    path('business-request/', views.business_owner_request, name='business_owner_request'),
    
    # Messaging and request status routes
    path('request-status/', views.request_status_page, name='request_status_page'),
    path('admin/requests/', views.admin_requests_list, name='admin_requests_list'),
    path('admin/requests/<int:request_id>/', views.admin_request_detail, name='admin_request_detail'),
    
    # Pricing routes
    path('pricing/', views.pricing_dashboard, name='pricing_dashboard'),
    path('pricing/add/', views.add_pricing_rule, name='add_pricing_rule'),
    path('pricing/edit/<int:rule_id>/', views.edit_pricing_rule, name='edit_pricing_rule'),
    path('pricing/delete/<int:rule_id>/', views.delete_pricing_rule, name='delete_pricing_rule'),
    path('pricing/delete_all/', views.delete_all_pricing_rules, name='delete_all_pricing_rules'),
    path('pricing/toggle/<int:rule_id>/', views.toggle_pricing_rule, name='toggle_pricing_rule'),
    path('default-pricing-rules/', views.default_pricing_management, name='default_pricing_management'),
    
    # History and admin routes
    path('history/', views.document_history, name='document_history'),
    path('business/analysis-history/', views.business_user_analysis_history, name='business_user_analysis_history'),
    path('user/analysis-history/', views.regular_user_analysis_history, name='regular_user_analysis_history'),
    path('admin-dashboard/', views.super_admin_dashboard, name='super_admin_dashboard'),
    path('business-pricing-dashboard/', views.business_pricing_dashboard, name='business_pricing_dashboard'),
    path('role-check/', views.user_role_check, name='user_role_check'),
    path('clear-sessions/', views.clear_user_sessions, name='clear_user_sessions'),
    
    # Analytics and Reports routes
    path('analytics/', views.analytics_dashboard, name='analytics_dashboard'),
    path('reports/', views.detailed_reports, name='detailed_reports'),
    path('reports/export/', views.export_reports, name='export_reports'),
    
    # Progress tracking
    path('progress/', views.get_progress, name='get_progress'),
    
    # Print management routes
    path('print/', views.print_document, name='print_document'),
    path('print-history/', views.print_history, name='print_history'),
    path('print/update-status/', views.update_print_status, name='update_print_status'),
    path('print/document/<int:analysis_id>/', views.print_document_content, name='print_document_content'),
]

