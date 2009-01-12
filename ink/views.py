from django.template import loader, RequestContext
from django.contrib.admin.views.decorators import staff_member_required
from django.core.exceptions import ObjectDoesNotExist
from django.core.xheaders import populate_xheaders
from django.http import Http404, HttpResponse
from django.views.generic.list_detail import object_detail

def flat_object_detail(request, queryset, object_id=None, slug=None,
        slug_field='slug', template_name=None, template_name_field=None,
        template_loader=loader, extra_context=None, context_processors=None,
        template_object_name='object', mimetype=None):
    """
    Generic detail view from just the slug name.

    Templates: ``<app_label>/<model_name>_detail.html``
    Context:
        object:
            the object to be detailed
    """
    if extra_context is None:
        extra_context = {}

    model = queryset.model

    lookup_kwargs = {}
    if object_id:
        lookup_kwargs['%s__exact' % model._meta.pk.name] = object_id
    elif slug and slug_field:
        lookup_kwargs['%s__exact' % slug_field] = slug
    else:
        raise AttributeError, "Generic detail view must be called with either an object_id or a slug/slugfield"

    try:
        obj = queryset.get(**lookup_kwargs)
    except ObjectDoesNotExist:
        raise Http404, "No %s found for" % model._meta.verbose_name

    if not template_name:
        template_name = "%s/%s_detail.html" % (model._meta.app_label, model._meta.object_name.lower())

    if template_name_field:
        template_name_list = [getattr(obj, template_name_field), template_name]
        t = template_loader.select_template(template_name_list)
    else:
        t = template_loader.get_template(template_name)

    c = RequestContext(request,
                       { template_object_name: obj },
                       context_processors)

    for key, value in extra_context.items():
        if callable(value):
            c[key] = value()
        else:
            c[key] = value
    response = HttpResponse(t.render(c), mimetype=mimetype)
    populate_xheaders(request, response, model, getattr(obj, obj._meta.pk.name))
    return response

@staff_member_required
def preview_object_detail(request, queryset, object_id, template_name=None,
        **kwargs):
    """
    Preview detail view from object_id.

    Templates: ``<app_label>/<model_name>_preview.html``
    Context:
        object:
            the object to be previewed
    """
    if not object_id:
        raise AttributeError, "Preview view must be called with an object_id"

    if not template_name:
        model = queryset.model
        template_name = "%s/%s_preview.html" % (model._meta.app_label, model._meta.object_name.lower())

    return object_detail(request, queryset, object_id=object_id,
            template_name=template_name, **kwargs)
