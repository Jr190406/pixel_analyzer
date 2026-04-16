from django.shortcuts import redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import REDIRECT_FIELD_NAME
from django.conf import settings
from django.urls import reverse
from django.http import JsonResponse
from functools import wraps

def get_user_profile(user):
    """Helper function to get or create user profile"""
    from .models import UserProfile
    profile, created = UserProfile.objects.get_or_create(user=user)
    return profile

def authentication_required(view_func):
    """Custom authentication decorator with better user experience"""
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            # For AJAX requests, return JSON response
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({
                    'error': 'Authentication required',
                    'redirect': reverse('user_login')
                }, status=401)
            
            # For direct URL access, show friendly access denied page
            messages.error(
                request, 
                "🔒 Please log in to access this page. If you don't have an account, you can register for free!"
            )
            # Redirect to login with next parameter
            login_url = reverse('user_login')
            next_url = request.get_full_path()
            return redirect(f"{login_url}?next={next_url}")
        return view_func(request, *args, **kwargs)
    return wrapper

def business_owner_required(view_func):
    """Decorator to require business owner or super admin role"""
    @wraps(view_func)
    @login_required
    def wrapper(request, *args, **kwargs):
        profile = get_user_profile(request.user)
        if not profile.can_manage_pricing():
            messages.error(request, "Access denied. Business owner privileges required.")
            return redirect('dashboard_router')
        return view_func(request, *args, **kwargs)
    return wrapper

def super_admin_required(view_func):
    """Decorator to require super admin role"""
    @wraps(view_func)
    @login_required
    def wrapper(request, *args, **kwargs):
        profile = get_user_profile(request.user)
        if not profile.can_view_all_users():
            messages.error(request, "Access denied. Super administrator privileges required.")
            return redirect('dashboard_router')
        return view_func(request, *args, **kwargs)
    return wrapper

def role_required(required_roles):
    """Decorator to require specific roles"""
    def decorator(view_func):
        @wraps(view_func)
        @login_required
        def wrapper(request, *args, **kwargs):
            profile = get_user_profile(request.user)
            if profile.role not in required_roles:
                messages.error(request, f"Access denied. Required role: {', '.join(required_roles)}")
                return redirect('dashboard_router')
            return view_func(request, *args, **kwargs)
        return wrapper
    return decorator
