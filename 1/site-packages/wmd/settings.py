
from django.conf import settings

WMD_SHOW_PREVIEW = getattr(settings, 'WMD_SHOW_PREVIEW', False)
WMD_ADMIN_SHOW_PREVIEW = getattr(settings, 'WMD_ADMIN_SHOW_PREVIEW', True)
