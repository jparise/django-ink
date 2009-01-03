from django.contrib import admin

from ink.models import Category, Entry, Article, Note

class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}

    fieldsets = (
        ('', {'fields': ('name', 'slug')}),
    )

class EntryAdmin(admin.ModelAdmin):
    date_hierarchy = 'pub_date'
    prepopulated_fields = {'slug': ('title',)}
    list_display = ('title', 'pub_date', 'author')
    list_filter = ('status', 'categories')
    exclude = ('author',)

    fieldsets = (
        ('Content',  {'fields': ('title', 'slug'),
                      'classes': ('monospace',)}),
        ('Metadata', {'fields': ('pub_date', 'status', 'categories',
                                 'commentable')}),
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
        ('Metadata', {'fields': ('pub_date', 'status', 'categories',
                                 'commentable')}),
    )

class NoteAdmin(EntryAdmin):
    search_fields = ('title', 'text')

    fieldsets = (
        ('Content',  {'fields': ('title', 'slug', 'text'),
                      'classes': ('monospace',)}),
        ('Metadata', {'fields': ('pub_date', 'status', 'categories',
                                 'commentable')}),
    )

admin.site.register(Category, CategoryAdmin)
admin.site.register(Entry, EntryAdmin)
admin.site.register(Article, ArticleAdmin)
admin.site.register(Note, NoteAdmin)
