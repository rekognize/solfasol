from django.views.generic import ListView, DetailView, CreateView
from django.utils.translation import ugettext as _
from django.shortcuts import get_object_or_404
from django.shortcuts import render, redirect
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator
from django.utils.timezone import now
from solfasol.issues.models import Page
from solfasol.publications.models import Publication
from solfasol.publications.views import content_detail as publication_content_detail
from .models import Content, Category, Tag, Contributor, Series


class ContentListView(ListView):
    model = Content
    context_object_name = 'content_list'

    def get_queryset(self):
        qs = super().get_queryset().filter(
            publish=True,
            publish_at__lt=now(),
        )
        if self.kwargs.get('category'):
            qs = qs.filter(category__slug=self.kwargs.get('category'))
        elif self.kwargs.get('tag'):
            qs = qs.filter(tags__slug=self.kwargs.get('tag'))
        elif self.kwargs.get('series'):
            qs = qs.filter(series__slug=self.kwargs.get('series'))
        elif self.kwargs.get('popular'):
            qs = qs.order_by('-view_count')[:20]
        elif self.kwargs.get('series'):
            qs = qs.filter(series__slug=self.kwargs.get('series'))
        elif self.kwargs.get('contributor'):
            qs = qs.filter(contributors__slug=self.kwargs.get('contributor'))
        return qs.distinct()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.kwargs.get('category'):
            category = get_object_or_404(Category,slug=self.kwargs['category'])
            context.update({
                'list_type': _('category'),
                'category': category,
                'title': category.name,
            })
        elif self.kwargs.get('tag'):
            tag = get_object_or_404(Tag, slug=self.kwargs['tag'])
            context.update({
                'list_type': _('tag'),
                'tag': tag,
                'title': tag.name,
                'pages': Page.objects.filter(content__tags=tag),
            })
        elif self.kwargs.get('popular'):
            context.update({
                'list_type': _('popular'),
                'title': _('popular'),
            })
        elif self.kwargs.get('series'):
            series = get_object_or_404(Series, slug=self.kwargs['series'])
            context.update({
                'list_type': _('series'),
                'series': series,
                'title': series.name,
            })
        elif self.kwargs.get('contributor'):
            contributor = get_object_or_404(Contributor, slug=self.kwargs['contributor'])
            context.update({
                'list_type': _('contributor'),
                'contributor': contributor,
                'title': contributor.name,
                'pages': Page.objects.filter(content__contributors=contributor),
            })
        return context


@cache_page(5*60)  # 5 mins
def content_detail(request, slug):
    publication = Publication.objects.filter(
        site__domain=request.get_host()
    ).first()
    if publication:
        return publication_content_detail(request, publication, slug)

    content = get_object_or_404(Content, slug=slug)
    content.view_count += 1
    content.save()
    return render(request, 'content/content_detail.html', {
        'content': content,
    })
