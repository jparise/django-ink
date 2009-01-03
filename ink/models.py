from datetime import datetime

from django.db import models
from django.contrib.auth.models import User

import tagging
import tagging.fields

from ink import markup, settings

# Status Constants
STATUS_PUBLIC, STATUS_DRAFT, STATUS_HIDDEN = 1, 2, 3
STATUSES = (
    (STATUS_PUBLIC, 'Public'),
    (STATUS_DRAFT,  'Draft'),
    (STATUS_HIDDEN, 'Hidden'),
)

class PublicEntryManager(models.Manager):
    def get_query_set(self):
        return super(PublicEntryManager, self).get_query_set().filter(status__exact=STATUS_PUBLIC)

class Entry(models.Model):
    # Metadata
    author = models.ForeignKey(User)
    pub_date = models.DateTimeField(u'Publish Date', default=datetime.today)
    slug = models.SlugField(unique_for_date='pub_date')
    tags = tagging.fields.TagField()

    # Options
    status = models.SmallIntegerField(choices=STATUSES, default=STATUS_DRAFT)
    commentable = models.BooleanField(default=True)

    # Content
    title = models.CharField(max_length=160)
    summary = models.TextField(blank=True, null=True)

    # Rendered Content
    summary_html = models.TextField(blank=True, null=True, editable=False)
    body_html = models.TextField(blank=True, editable=False)

    # Managers
    objects = models.Manager()
    public = PublicEntryManager()

    class Meta:
        verbose_name_plural = 'Entries'
        ordering = ('-pub_date',)
        get_latest_by = 'pub_date'

    def __unicode__(self):
        return self.title

    def save(self):
        if self.summary:
            self.summary_html = markup.render(self.summary)
        super(Entry, self).save()

    @models.permalink
    def get_absolute_url(self):
        if settings.INK_FLAT_URLS:
            return ('ink_flat_entry_detail', (),
                        {'slug': self.slug})
        else:
            return ('ink_entry_detail', (),
                        {'year': self.pub_date.strftime('%Y'),
                         'month': self.pub_date.strftime('%b').lower(),
                         'day': self.pub_date.strftime('%d'),
                         'slug': self.slug})

class Article(Entry):
    path = models.FilePathField(path=settings.INK_ARTICLES_PATH, match="\.txt$")

    class Meta:
        verbose_name_plural = 'Articles'

    def save(self):
        content = open(self.path, 'r')
        self.body_html = markup.render(content.read())
        super(Article, self).save()

class Note(Entry):
    body = models.TextField()

    class Meta:
        verbose_name_plural = 'Notes'

    def save(self):
        self.body_html = markup.render(self.body)
        super(Note, self).save()

tagging.register(Entry, 'tag_set')
