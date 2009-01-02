from django.contrib import admin

from ink.models import Entry

class EntryAdmin(admin.ModelAdmin):
    date_hierarchy = 'pub_date'
    prepopulated_fields = {'slug': ('title',)}
    search_fields = ('title', 'summary', 'body')
    list_display = ('title', 'pub_date', 'author', 'tags')
    list_filter = ('status',)

    fieldsets = (
        ('Content',  {'fields': ('title', 'summary', 'body'),
                      'classes': ('monospace',)}),
        ('Metadata', {'fields': ('slug', 'pub_date', 'author', 'tags')}),
        ('Options',  {'fields': ('status', 'commentable')}),
    )

admin.site.register(Entry, EntryAdmin)
