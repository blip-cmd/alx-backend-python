# Django Middleware - Project 0x03

This project demonstrates the implementation of custom Django middleware for a messaging application.

## Setup Instructions

1. **Navigate to the project directory:**
   ```bash
   cd Django-Middleware-0x03
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up the database:**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

4. **Create a superuser (optional):**
   ```bash
   python manage.py createsuperuser
   ```

5. **Run the development server:**
   ```bash
   python manage.py runserver
   ```

## Implemented Middleware

### 1. RequestLoggingMiddleware
- **File:** `chats/middleware.py`
- **Purpose:** Logs each user's requests to a file
- **Log Format:** `{timestamp} - User: {user} - Path: {request.path}`
- **Log File:** `requests.log`

### 2. RestrictAccessByTimeMiddleware
- **File:** `chats/middleware.py`
- **Purpose:** Restricts access to the messaging app during certain hours
- **Restriction:** Access denied outside 6AM - 9PM
- **Response:** HTTP 403 Forbidden

### 3. OffensiveLanguageMiddleware (Rate Limiting)
- **File:** `chats/middleware.py`
- **Purpose:** Limits the number of chat messages a user can send within a time window
- **Limit:** 5 messages per minute per IP address
- **Response:** HTTP 429 Too Many Requests when limit exceeded

### 4. RolePermissionMiddleware
- **File:** `chats/middleware.py`
- **Purpose:** Checks user roles before allowing access to specific actions
- **Allowed Roles:** admin, moderator
- **Protected Paths:** `/admin/`, `/chats/conversations/`
- **Response:** HTTP 403 Forbidden for unauthorized roles

## Testing the Middleware

### Manual Testing

1. **Start the server:**
   ```bash
   python manage.py runserver
   ```

2. **Test Request Logging:**
   - Make any request to the application
   - Check `requests.log` file for logged requests

3. **Test Time Restrictions:**
   - Access the application outside 6AM-9PM hours
   - Should receive a 403 Forbidden response

4. **Test Rate Limiting:**
   - Make more than 5 POST requests to `/chats/` within a minute
   - Should receive a 429 Too Many Requests response after the 5th request

5. **Test Role Permissions:**
   - Try to access `/admin/` without admin/moderator role
   - Should receive a 403 Forbidden response

### Automated Testing

Run the test script:
```bash
python test_middleware.py
```

## Middleware Configuration

The middleware is configured in `settings.py`:

```python
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    # Custom middleware
    'chats.middleware.RequestLoggingMiddleware',
    'chats.middleware.RestrictAccessByTimeMiddleware',
    'chats.middleware.OffensiveLanguageMiddleware',
    'chats.middleware.RolePermissionMiddleware',
]
```

## API Endpoints

The application provides REST API endpoints for:
- Conversations: `/chats/conversations/`
- Messages: `/chats/messages/`
- User management through Django admin: `/admin/`

## User Roles

The application supports the following user roles:
- `guest`: Regular user with basic permissions
- `host`: User with additional permissions
- `admin`: Full administrative access
- `moderator`: Moderation capabilities

## Files Structure

```
Django-Middleware-0x03/
├── chats/
│   ├── middleware.py          # Custom middleware implementations
│   ├── models.py             # User, Conversation, Message models
│   ├── views.py              # API views
│   ├── serializers.py        # DRF serializers
│   └── ...
├── manage.py
├── settings.py               # Django settings with middleware configuration
├── requests.log              # Request logging output
├── test_middleware.py        # Middleware testing script
└── README.md                 # This file
```

## Notes

- The middleware classes inherit from `MiddlewareMixin` for better compatibility
- Rate limiting is implemented using in-memory storage (consider Redis for production)
- Time restrictions are based on server time
- Request logging uses Python's built-in logging module
- All middleware includes proper error handling and informative error messages