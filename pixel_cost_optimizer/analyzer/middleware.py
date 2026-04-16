"""
Middleware for handling authentication and security
"""
from django.shortcuts import redirect
from django.urls import reverse
from django.contrib import messages
from django.http import JsonResponse


class AuthenticationMiddleware:
    """
    Middleware to handle authentication requirements for protected views
    """
    
    def __init__(self, get_response):
        self.get_response = get_response
        # Paths that require authentication
        self.protected_paths = [
            '/',
            '/pricing/',
            '/history/',
            '/admin-dashboard/',
            '/business-dashboard/',
            '/role-check/',
        ]
        
        # Paths that should be accessible without authentication
        self.public_paths = [
            '/login/',
            '/register/',
            '/logout/',
            '/admin/',  # Django admin has its own auth
        ]

    def __call__(self, request):
        # Process the request before the view
        response = self.process_request(request)
        if response:
            return response
            
        # Get the response from the view
        response = self.get_response(request)
        
        return response

    def process_request(self, request):
        """
        Check if the user should be redirected to login
        """
        path = request.path_info
        
        # Skip for public paths or if user is already authenticated
        if any(path.startswith(public_path) for public_path in self.public_paths):
            return None
            
        if request.user.is_authenticated:
            return None
            
        # Check if this is a protected path
        if any(path.startswith(protected_path) for protected_path in self.protected_paths):
            # For AJAX requests
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({
                    'error': 'Authentication required',
                    'redirect': reverse('user_login')
                }, status=401)
            
            # For regular requests, redirect to login with next parameter
            messages.error(
                request, 
                "🔒 Please log in to access this page. Create an account if you don't have one!"
            )
            login_url = reverse('user_login')
            next_url = request.get_full_path()
            return redirect(f"{login_url}?next={next_url}")
        
        return None
