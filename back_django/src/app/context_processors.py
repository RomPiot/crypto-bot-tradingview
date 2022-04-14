from django.conf import settings


def from_settings(request):
    return {
        "ENV_BANNER_NAME": getattr(settings, "ENV_BANNER_NAME", ""),
        "ENV_BANNER_BG_COLOR": getattr(settings, "ENV_BANNER_BG_COLOR", "red"),
        "ENV_BANNER_TEXT_COLOR": getattr(settings, "ENV_BANNER_TEXT_COLOR", "white"),
        "ENV_BANNER_SHOW": getattr(settings, "ENV_BANNER_SHOW"),
    }
