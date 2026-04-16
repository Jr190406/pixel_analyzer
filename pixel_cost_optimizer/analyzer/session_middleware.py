from django.contrib.auth import logout
from django.shortcuts import redirect
from django.contrib import messages
from .decorators import get_user_profile

class UserRoleSessionMiddleware:
    """
    Middleware to handle user role changes and session security
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Process the request
        response = self.process_request(request)
        if response:
            return response
            
        response = self.get_response(request)
        return response

    def process_request(self, request):
        """
        Check if user's role has changed or if session is invalid
        """
        # Check if user attribute exists and is authenticated
        if hasattr(request, 'user') and request.user.is_authenticated:
            try:
                # Get current user profile
                profile = get_user_profile(request.user)
                current_role = profile.role if profile else 'regular'
                
                # Check if role is stored in session
                session_role = request.session.get('user_role')
                
                if session_role is None:
                    # First time or session lost - store current role
                    request.session['user_role'] = current_role
                    request.session['user_id'] = request.user.id
                elif session_role != current_role:
                    # Role changed - invalidate session and force re-login
                    logout(request)
                    messages.warning(
                        request, 
                        'Your account role has been updated. Please log in again.'
                    )
                    return redirect('user_login')
                elif request.session.get('user_id') != request.user.id:
                    # Different user - invalidate session
                    logout(request)
                    messages.warning(
                        request, 
                        'Session conflict detected. Please log in again.'
                    )
                    return redirect('user_login')
                    
            except Exception as e:
                # If there's any error with profile access, force re-login
                logout(request)
                messages.error(
                    request, 
                    'Session error detected. Please log in again.'
                )
                return redirect('user_login')
        
        return None


class SingleSessionMiddleware:
    """
    Middleware to ensure only one active session per user
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.process_request(request)
        if response:
            return response
            
        response = self.get_response(request)
        return response

    def process_request(self, request):
        """
        Check for multiple sessions for the same user
        """
        # Check if user attribute exists and is authenticated
        if hasattr(request, 'user') and request.user.is_authenticated:
            # Store current session key in user profile or session
            current_session_key = request.session.session_key
            stored_session_key = request.session.get('active_session_key')
            
            if stored_session_key is None:
                # First login - store session key
                request.session['active_session_key'] = current_session_key
            elif stored_session_key != current_session_key:
                # Different session detected - this could indicate multiple logins
                # For now, we'll allow it but could implement single session enforcement
                request.session['active_session_key'] = current_session_key
        
        return None
