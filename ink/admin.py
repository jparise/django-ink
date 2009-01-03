from django.contrib import admin

from ink.models import Entry, Article, Note

class EntryAdmin(admin.ModelAdmin):
    date_hierarchy = 'pub_date'
    prepopulated_fields = {'slug': ('title',)}
    list_display = ('title', 'pub_date', 'author', 'tags')
    list_filter = ('status',)
    exclude = ('author',)

    fieldsets = (
        ('Content',  {'fields': ('title', 'summary'),
                      'classes': ('monospace',)}),
        ('Metadata', {'fields': ('slug', 'pub_date', 'tags')}),
        ('Options',  {'fields': ('status', 'commentable')}),
    )

    def save_model(self, request, obj, form, change):
        if not change:
            obj.author = request.user
        obj.save()

class ArticleAdmin(EntryAdmin):
    search_fields = ('title', 'summary')

    fieldsets = (
        ('Content',  {'fields': ('title', 'summary', 'path'),
                      'classes': ('monospace',)}),
        ('Metadata', {'fields': ('slug', 'pub_date', 'tags')}),
        ('Options',  {'fields': ('status', 'commentable')}),
    )

class NoteAdmin(EntryAdmin):
    search_fields = ('title', 'summary', 'body')

    fieldsets = (
        ('Content',  {'fields': ('title', 'summary', 'body'),
                      'classes': ('monospace',)}),
        ('Metadata', {'fields': ('slug', 'pub_date', 'tags')}),
        ('Options',  {'fields': ('status', 'commentable')}),
    )

admin.site.register(Entry, EntryAdmin)
admin.site.register(Article, ArticleAdmin)
admin.site.register(Note, NoteAdmin)
