from django.http import HttpResponseForbidden
import logging
from datetime import datetime, time, timedelta

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
        user = request.user if request.user.is_authenticated else "Anonymous"

        log_message = f"{datetime.now()} - User: {user} - Path: {request.path}"
        logger.info(log_message)

        response = self.get_response(request)
        return response
    
class RestrictAccessByTimeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        start_time = time(21, 0)   # 9PM
        end_time = time(6, 0)      # 6AM

        current_time = datetime.now().time()

        if current_time < start_time or current_time > end_time:
            return HttpResponseForbidden(
                "Access to the messaging app is restricted between 9PM and 6AM."
            )

        response = self.get_response(request)
        return response


class OffensiveLanguageMiddleware:
    """
    Limits the number of chat messages a user can send per minute based on IP.
    """

    ip_requests = {}

    def __init__(self, get_response):
        self.get_response = get_response

        self.max_messages = 5
        self.time_window = timedelta(minutes=1)

    def __call__(self, request):
        if request.method == "POST":
            ip = self.get_client_ip(request)
            now = datetime.now()

            if ip not in self.ip_requests:
                self.ip_requests[ip] = []

            self.ip_requests[ip] = [
                t for t in self.ip_requests[ip] if now - t < self.time_window
            ]

            if len(self.ip_requests[ip]) >= self.max_messages:
                return HttpResponseForbidden(
                    f"You have exceeded {self.max_messages} messages per minute."
                )

            self.ip_requests[ip].append(now)

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
    
class RolepermissionMiddleware:
    """
    Middleware to check if the user has admin or moderator role.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if not request.user.is_authenticated:
            return HttpResponseForbidden("You must be logged in to perform this action.")

        user_role = getattr(request.user, "role", None)

        if user_role not in ("admin", "moderator"):
            return HttpResponseForbidden("You do not have permission to perform this action.")

        response = self.get_response(request)
        return response
    