from django.conf.urls.defaults import *

from ink.models import Entry
from ink.views import preview_object_detail

urlpatterns = patterns('',
    url(r'^(article|entry|note)/(?P<object_id>[0-9]+)/preview/$',
        preview_object_detail,
        dict(queryset=Entry.objects.all()),
        name='ink_entry_preview')
)
