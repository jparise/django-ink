from django.conf.urls.defaults import *
from django.views.generic import date_based

from tagging.views import tagged_object_list

from ink.models import Entry
from ink.views import flat_object_detail

entry_info_dict = {
    'queryset': Entry.public.all(),
    'date_field': 'pub_date',
}

flat_entry_info_dict = {
    'queryset': Entry.public.all(),
}

tag_info_dict = {
    'queryset_or_model': Entry.public.all(),
    'allow_empty': False,
}

urlpatterns = patterns('',
    url(r'^$',
        date_based.archive_index,
        dict(entry_info_dict, num_latest=5),
        name='ink_entry_archive_index'),

    url(r'^(?P<year>\d{4})/$',
        date_based.archive_year,
        entry_info_dict,
        name='ink_entry_archive_year'),

    url(r'^(?P<year>\d{4})/(?P<month>\w{3})/$',
        date_based.archive_month,
        entry_info_dict,
        name='ink_entry_archive_month'),

    url(r'^(?P<year>\d{4})/(?P<month>\w{3})/(?P<day>\d{2})/$',
        date_based.archive_day,
        entry_info_dict,
        name='ink_entry_archive_day'),

    url(r'^(?P<year>\d{4})/(?P<month>\w{3})/(?P<day>\d{2})/(?P<slug>[-\w]+)/$',
        date_based.object_detail,
        dict(entry_info_dict, slug_field='slug'),
        name='ink_entry_detail'),

    url(r'^(?P<slug>[-\w]+)/$',
        flat_object_detail,
        dict(flat_entry_info_dict, slug_field='slug'),
        name='ink_flat_entry_detail'),

    url(r'^tags/(?P<tag>[^/]+)/$',
        tagged_object_list,
        dict(tag_info_dict, template_name='ink/tagged_entry_list.html'),
        name='ink_tag_detail'),
)
