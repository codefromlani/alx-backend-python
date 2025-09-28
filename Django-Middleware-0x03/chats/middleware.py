from django.http import HttpResponseForbidden
import logging
from datetime import datetime, time, timedelta

# Configure a logger that writes to requests.log
logger = logging.getLogger(__name__)
handler = logging.FileHandler("requests.log")
formatter = logging.Formatter("%(message)s")
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.INFO)


class RequestLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Get user (anonymous if not logged in)
        user = request.user if request.user.is_authenticated else "Anonymous"

        # Log the request
        log_message = f"{datetime.now()} - User: {user} - Path: {request.path}"
        logger.info(log_message)

        # Continue processing request
        response = self.get_response(request)
        return response
    
class RestrictAccessByTimeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Define allowed access hours (6AM to 9PM)
        start_time = time(21, 0)   # 9PM
        end_time = time(6, 0)      # 6AM

        current_time = datetime.now().time()

        # If current time is outside allowed range, deny access
        if current_time < start_time or current_time > end_time:
            return HttpResponseForbidden(
                "Access to the messaging app is restricted between 9PM and 6AM."
            )

        # Continue processing request
        response = self.get_response(request)
        return response


class OffensiveLanguageMiddleware:
    """
    Limits the number of chat messages a user can send per minute based on IP.
    """

    # Store request timestamps by IP
    ip_requests = {}

    def __init__(self, get_response):
        self.get_response = get_response
        # Maximum allowed messages per time window
        self.max_messages = 5
        self.time_window = timedelta(minutes=1)

    def __call__(self, request):
        # Only apply for POST requests (messages)
        if request.method == "POST":
            # Get client IP
            ip = self.get_client_ip(request)
            now = datetime.now()

            # Initialize list if first request
            if ip not in self.ip_requests:
                self.ip_requests[ip] = []

            # Filter timestamps that are still within the time window
            self.ip_requests[ip] = [
                t for t in self.ip_requests[ip] if now - t < self.time_window
            ]

            # Check if limit exceeded
            if len(self.ip_requests[ip]) >= self.max_messages:
                return HttpResponseForbidden(
                    f"You have exceeded {self.max_messages} messages per minute."
                )

            # Record this request
            self.ip_requests[ip].append(now)

        # Continue processing request
        response = self.get_response(request)
        return response

    def get_client_ip(self, request):
        """Get the client IP from request headers"""
        x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
        if x_forwarded_for:
            ip = x_forwarded_for.split(",")[0]
        else:
            ip = request.META.get("REMOTE_ADDR")
        return ip
    