import logging
import time
from datetime import datetime, timezone
from collections import defaultdict
from django.http import HttpResponseForbidden, JsonResponse
from django.utils.deprecation import MiddlewareMixin
from django.contrib.auth.models import AnonymousUser

# Configure logging for request logging
logging.basicConfig(
    filename='requests.log',
    level=logging.INFO,
    format='%(message)s',
    filemode='a'
)

class RequestLoggingMiddleware(MiddlewareMixin):
    """
    Middleware that logs each user's requests to a file, including the timestamp, user and the request path.
    """
    
    def __init__(self, get_response=None):
        self.get_response = get_response
        super().__init__(get_response)
    
    def __call__(self, request):
        # Get the user (handle anonymous users)
        user = request.user if not isinstance(request.user, AnonymousUser) else "Anonymous"
        
        # Log the request information
        log_message = f"{datetime.now()} - User: {user} - Path: {request.path}"
        logging.info(log_message)
        
        # Continue processing the request
        response = self.get_response(request)
        return response


class RestrictAccessByTimeMiddleware(MiddlewareMixin):
    """
    Middleware that restricts access to the messaging app during certain hours of the day.
    Denies access if user accesses chat outside 6AM and 9PM.
    """
    
    def __init__(self, get_response=None):
        self.get_response = get_response
        super().__init__(get_response)
    
    def __call__(self, request):
        # Get current hour (24-hour format)
        current_hour = datetime.now().hour
        
        # Check if current time is outside allowed hours (6AM to 9PM)
        if current_hour < 6 or current_hour >= 21:  # 21 = 9PM in 24-hour format
            return HttpResponseForbidden(
                "Access to the messaging app is restricted outside of 6AM - 9PM. Please try again during allowed hours."
            )
        
        # Continue processing the request if within allowed hours
        response = self.get_response(request)
        return response


class OffensiveLanguageMiddleware(MiddlewareMixin):
    """
    Middleware that limits the number of chat messages a user can send within a certain time window,
    based on their IP address. Implements rate limiting for POST requests (messages).
    """
    
    def __init__(self, get_response=None):
        self.get_response = get_response
        super().__init__(get_response)
        # Dictionary to store message counts per IP address
        # Structure: {ip_address: [(timestamp1, count1), (timestamp2, count2), ...]}
        self.ip_message_counts = defaultdict(list)
        self.max_messages = 5  # Maximum messages per time window
        self.time_window = 60  # Time window in seconds (1 minute)
    
    def __call__(self, request):
        # Only check POST requests (assuming these are message submissions)
        if request.method == 'POST' and '/chats/' in request.path:
            client_ip = self.get_client_ip(request)
            current_time = time.time()
            
            # Clean old entries for this IP
            self.cleanup_old_entries(client_ip, current_time)
            
            # Count current messages in the time window
            message_count = len(self.ip_message_counts[client_ip])
            
            # Check if user has exceeded the limit
            if message_count >= self.max_messages:
                return JsonResponse(
                    {
                        'error': 'Rate limit exceeded. You can only send 5 messages per minute. Please try again later.'
                    },
                    status=429  # Too Many Requests
                )
            
            # Add current request to the count
            self.ip_message_counts[client_ip].append(current_time)
        
        # Continue processing the request
        response = self.get_response(request)
        return response
    
    def get_client_ip(self, request):
        """Extract the client's IP address from the request."""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip
    
    def cleanup_old_entries(self, ip_address, current_time):
        """Remove entries older than the time window."""
        cutoff_time = current_time - self.time_window
        self.ip_message_counts[ip_address] = [
            timestamp for timestamp in self.ip_message_counts[ip_address]
            if timestamp > cutoff_time
        ]


class RolePermissionMiddleware(MiddlewareMixin):
    """
    Middleware that checks the user's role before allowing access to specific actions.
    Only allows admin and moderator roles to access certain endpoints.
    """
    
    def __init__(self, get_response=None):
        self.get_response = get_response
        super().__init__(get_response)
        # Define which roles are allowed access
        self.allowed_roles = ['admin', 'moderator']
        # Define protected paths that require special permissions
        self.protected_paths = [
            '/admin/',
            '/chats/conversations/',  # Assuming conversation management requires special permissions
        ]
    
    def __call__(self, request):
        # Check if the request path requires special permissions
        requires_special_permission = any(
            protected_path in request.path for protected_path in self.protected_paths
        )
        
        if requires_special_permission:
            # Check if user is authenticated
            if isinstance(request.user, AnonymousUser):
                return JsonResponse(
                    {'error': 'Authentication required'},
                    status=401
                )
            
            # Check if user has the required role
            user_role = getattr(request.user, 'role', None)
            if user_role not in self.allowed_roles:
                return JsonResponse(
                    {
                        'error': f'Access denied. This action requires admin or moderator privileges. Your role: {user_role}'
                    },
                    status=403
                )
        
        # Continue processing the request
        response = self.get_response(request)
        return response