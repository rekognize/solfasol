import secrets
import json
from urllib.parse import urlparse, parse_qs
from collections import defaultdict
from django.core.exceptions import ValidationError
from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils.functional import cached_property
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from slugify import slugify
from solfasol.issues.models import Issue, Page
from solfasol.tags.models import Tag
from solfasol.contributors.models import Contributor
from solfasol.publications.models import Publication


class Content(models.Model):
    title = models.CharField(_('title'), max_length=200, blank=True, null=True)
    slug = models.SlugField(max_length=100)
    subtitle = models.CharField(_('subtitle'), max_length=200, blank=True, null=True)

    data = models.JSONField(blank=True, null=True, editable=False)

    contributors = models.ManyToManyField(
        Contributor,
        verbose_name=_('contributor'),
        blank=True,
        related_name='content_set',
        through='ContentContributor',
    )

    lang = models.CharField(_('language'), max_length=7, choices=settings.LANGUAGES, default='tr')
    tags = models.ManyToManyField(Tag, verbose_name=_('tags'), blank=True)
    category = models.ForeignKey('category', verbose_name=_('category'), blank=True, null=True, on_delete=models.SET_NULL)
    series = models.ForeignKey('series', verbose_name=_('series'), blank=True, null=True, on_delete=models.SET_NULL)

    publication = models.ForeignKey(
        Publication, verbose_name=_('publication'),
        blank=True, null=True,
        on_delete=models.SET_NULL,
    )

    page = models.ForeignKey(
        Page, verbose_name=_('page'),
        help_text=_('Published on issue / page'),
        blank=True, null=True,
        on_delete=models.SET_NULL
    )

    image = models.ImageField(_('image'), upload_to='content/')

    summary = models.TextField(_('summary'), blank=True, null=True)

    video_url = models.URLField(_('video url'), blank=True, null=True)

    embed_media = models.TextField(_('media embed code'), blank=True, null=True)

    related_content = models.ManyToManyField('self', verbose_name=_('related content'), blank=True)

    added_by = models.ForeignKey(
        User, verbose_name=_('added by'),
        blank=True, null=True,
        on_delete=models.SET_NULL,
        related_name='added_content',
    )

    publish = models.BooleanField(_('publish'), default=False)
    publish_at = models.DateTimeField(
        _('publishing time'), default=now,
        help_text=_('Set a future date to publish later')
    )
    published_by = models.ForeignKey(
        User, verbose_name=_('published by'),
        blank=True, null=True,
        on_delete=models.SET_NULL,
        related_name='published_content',
    )

    featured = models.BooleanField(_('featured'), default=False)
    pinned = models.BooleanField(_('pinned'), default=False)

    date = models.DateTimeField(_('date'), default=now)

    added = models.DateTimeField(_('added'), default=now)
    modified = models.DateTimeField(_('modified'), auto_now=True)
    view_count = models.PositiveIntegerField(default=0, editable=False)

    def save(self, **kwargs):
        if not self.slug:
            if self.title:
                self.slug = slugify(self.title)[:100]
            else:
                self.slug = secrets.token_urlsafe()[:8]
        super().save(**kwargs)
        if self.pinned:
            Content.objects.filter(pinned=True).exclude(id=self.id).update(pinned=False)

    def __str__(self):
        return self.title or '-'

    def get_absolute_url(self):
        url = reverse('content_detail', kwargs={'slug': self.slug})
        if self.publication:
            url = f'//{self.publication.site.domain}{url}'
        return url

    def clean(self):
        if self.video_url:
            if not 'youtube.com/embed/' in self.video_url:
                if 'youtube.com/' or 'youtu.be/' in self.video_url:
                    vid = None
                    if 'youtube.com/' in self.video_url:
                        if 'watch?v=' in self.video_url:
                            parts = urlparse(self.video_url)
                            params = parse_qs(parts.query)
                            vid = params.get('v', [])[0]
                    elif 'youtu.be/' in self.video_url:
                        vid = self.video_url.split('/')[-1]
                    if vid:
                        self.video_url = f"https://youtube.com/embed/{vid}"
                    else:
                        raise ValidationError(_('Invalid Youtube video link!'))
                else:
                    raise ValidationError(_('Please submit a Youtube video link!'))

    @cached_property
    def rendered(self):
        rendered_doc = ''
        for block in self.data['blocks']:
            rendered_doc += render_to_string(f'content/blocks/{block["type"]}.html', block["data"])
        return rendered_doc

    @cached_property
    def data_js(self):
        return json.dumps(self.data)

    @cached_property
    def owners(self):
        return ContentContributor.objects.filter(
            content=self,
            contribution_type__primary=True,
        )

    @cached_property
    def contributors_dict(self):
        contributors = defaultdict(list)
        for contributor in  ContentContributor.objects.filter(content=self).order_by('-contribution_type__primary'):
            contributors[contributor.contribution_type].append(contributor)
        return dict(contributors)

    @cached_property
    def similar_content(self):
        return self.related_content.filter(publish=True)

    class Meta:
        verbose_name = _('content')
        verbose_name_plural = _('content')
        ordering = ('-pinned', '-added',)
        unique_together = (('slug', 'publication'),)


class ContentSection(models.Model):
    section_type = models.CharField(max_length=1, choices=(
        ('t', _('text')),
        ('s', _('spot')),
        ('i', _('image')),
    ), default='t')
    content = models.ForeignKey(Content, verbose_name=_('content'), on_delete=models.CASCADE)
    section_title = models.CharField(_('section title'), max_length=200, blank=True, null=True)
    body = models.TextField(_('section text'), blank=True, null=True)

    def get_section_no(self):
        return self.content.contentsection_set.filter(id__lte=self.id).count()

    def __str__(self):
        return '%s - %s' % (
            str(self.content),
            self.get_section_no(),
        )

    class Meta:
        ordering = ('id',)
        verbose_name = _('content section')
        verbose_name_plural = _('content sections')


class ContentSectionImage(models.Model):
    content_section = models.ForeignKey(ContentSection, verbose_name=_('section image'), on_delete=models.CASCADE)
    image = models.ImageField(_('image'), upload_to='content_images/')
    description = models.CharField(_('description'), blank=True, null=True, max_length=100)

    def __str__(self):
        return self.image.url

    class Meta:
        ordering = ('id',)
        verbose_name = _('section image')
        verbose_name_plural = _('section images')


class ContributionType(models.Model):
    description = models.CharField(_('description'), max_length=20)
    primary = models.BooleanField(_('primary'), default=False)

    def __str__(self):
        return self.description

    class Meta:
        ordering = ('id',)
        verbose_name = _('contribution type')
        verbose_name_plural = _('contribution types')


class ContentContributor(models.Model):
    content = models.ForeignKey(Content, verbose_name=_('content'), on_delete=models.CASCADE)
    contributor = models.ForeignKey(Contributor, verbose_name=_('contributor'), on_delete=models.CASCADE)
    contribution_type = models.ForeignKey(
        ContributionType,
        verbose_name=_('contribution type'),
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return self.contributor.name

    class Meta:
        verbose_name = _('content - contributor')
        verbose_name_plural = _('content - contributors')


class Category(models.Model):
    name = models.CharField(_('name'), max_length=100)
    slug = models.SlugField(unique=True)
    publication = models.ForeignKey(
        Publication, verbose_name=_('publication'),
        blank=True, null=True,
        on_delete=models.CASCADE,
    )
    order = models.PositiveSmallIntegerField(default=0)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('content_category_list', kwargs={'category': self.slug})

    @cached_property
    def content(self):
        return self.content_set.filter(publish=True)

    class Meta:
        verbose_name = _('category')
        verbose_name_plural = _('categories')
        ordering = ('order',)


class Series(models.Model):
    name = models.CharField(_('name'), max_length=100)
    slug = models.SlugField(unique=True)
    issues = models.ManyToManyField(
        Issue, verbose_name=_('issues'),
        blank=True,
    )
    tags = models.ManyToManyField(Tag, verbose_name=_('tags'), blank=True)
    contributors = models.ManyToManyField(
        Contributor,
        verbose_name=_('contributor'),
        blank=True,
        through='SeriesContributor',
    )

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('content_series_list', kwargs={'series': self.slug})

    @cached_property
    def contributors_dict(self):
        contributors = defaultdict(list)
        for contributor in  SeriesContributor.objects.filter(series=self).order_by('-contribution_type__primary'):
            contributors[contributor.contribution_type].append(contributor)
        return dict(contributors)

    @property
    def content(self):
        return self.content_set.filter(publish=True)

    class Meta:
        verbose_name = _('series')
        verbose_name_plural = _('series')


class SeriesContributor(models.Model):
    series = models.ForeignKey(Series, verbose_name=_('content'), on_delete=models.CASCADE)
    contributor = models.ForeignKey(Contributor, verbose_name=_('contributor'), on_delete=models.CASCADE)
    contribution_type = models.ForeignKey(
        ContributionType,
        verbose_name=_('contribution type'),
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return self.contributor.name

    class Meta:
        verbose_name = _('series contributor')
        verbose_name_plural = _('series contributors')


class ExtraFile(models.Model):
    file = models.FileField(upload_to='extra/')

    def __str__(self):
        return self.file.url

    class Meta:
        verbose_name = _('extra file')
        verbose_name_plural = _('extra files')
