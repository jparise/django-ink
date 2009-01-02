from django.contrib import admin

from ink.models import Entry

class EntryAdmin(admin.ModelAdmin):
    date_hierarchy = 'pub_date'
    prepopulated_fields = {'slug': ('title',)}
    search_fields = ('title', 'summary', 'body')
    list_display = ('title', 'pub_date', 'author', 'tags')
    list_filter = ('status',)
    exclude = ('author',)

    fieldsets = (
        ('Content',  {'fields': ('title', 'summary', 'body'),
                      'classes': ('monospace',)}),
        ('Metadata', {'fields': ('slug', 'pub_date', 'tags')}),
        ('Options',  {'fields': ('status', 'commentable')}),
    )

    def save_model(self, request, obj, form, change):
        if not change:
            obj.author = request.user
        obj.save()

admin.site.register(Entry, EntryAdmin)
