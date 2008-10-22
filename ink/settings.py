"""
Convenience module for accessing custom ink application settings.  This allows
us to enforce default settings when the main settings module does not contain
overriding definitions.
"""
from django.conf import settings

# Should we prefer flat (non-date-based) URLs?
INK_FLAT_URLS = getattr(settings, 'INK_FLAT_URLS', False)
