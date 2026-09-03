from rest_framework.views import exception_handler


def custom_exception_handler(exc, context):
    """
    Custom exception handler to ensure standard JSON structure:
    {
        "error": {
            "type": "ValidationError",
            "status_code": 400,
            "details": { ... }
        }
    }
    """
    response = exception_handler(exc, context)

    if response is not None:
        custom_data = {
            "error": {
                "type": exc.__class__.__name__,
                "status_code": response.status_code,
                "details": response.data
            }
        }
        response.data = custom_data

    return response
