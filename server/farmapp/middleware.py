

import json
from .models import AdminActivityLog

class AdminActionLoggerMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        # Log admin actions
        if (
            request.user.is_authenticated
            and request.user.is_staff
            and request.method in ["POST", "PUT", "DELETE"]
        ):
            try:
                # Decode and parse request body if it contains JSON
                if request.body:
                    body_content = request.body.decode("utf-8")
                    body_data = json.loads(body_content) if body_content.strip() else {}
                else:
                    body_data = {}

                action = f"{request.method} {request.path}"
                
                # Log admin action (details can be logged or skipped)
                AdminActivityLog.objects.create(
                    adminId=request.user,
                    action=action
                )

            except (json.JSONDecodeError, UnicodeDecodeError) as e:
                # Log the error or ignore invalid JSON
                pass

        return response

