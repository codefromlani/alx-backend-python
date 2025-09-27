from django.http import HttpResponseForbidden
import logging
from datetime import datetime, time

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
