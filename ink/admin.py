from django.contrib import admin

from ink.models import Entry, Article, Note

class EntryAdmin(admin.ModelAdmin):
    date_hierarchy = 'pub_date'
    prepopulated_fields = {'slug': ('title',)}
    list_display = ('title', 'pub_date', 'author')
    list_filter = ('status',)
    exclude = ('author',)

    fieldsets = (
        ('Content',  {'fields': ('title', 'slug'),
                      'classes': ('monospace',)}),
        ('Metadata', {'fields': ('pub_date', 'status', 'commentable')}),
    )

    def save_model(self, request, obj, form, change):
        if not change:
            obj.author = request.user
        obj.save()

class ArticleAdmin(EntryAdmin):
    search_fields = ('title',)

    fieldsets = (
        ('Content',  {'fields': ('title', 'slug', 'path'),
                      'classes': ('monospace',)}),
        ('Metadata', {'fields': ('pub_date', 'status', 'commentable')}),
    )

class NoteAdmin(EntryAdmin):
    search_fields = ('title', 'text')

    fieldsets = (
        ('Content',  {'fields': ('title', 'slug', 'text'),
                      'classes': ('monospace',)}),
        ('Metadata', {'fields': ('pub_date', 'status', 'commentable')}),
    )

admin.site.register(Entry, EntryAdmin)
admin.site.register(Article, ArticleAdmin)
admin.site.register(Note, NoteAdmin)
