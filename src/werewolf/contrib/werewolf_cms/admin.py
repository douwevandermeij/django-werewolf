from cms import models as cms_models
from django.conf.urls import patterns, url
from django.contrib import admin
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect

from werewolf.admin import WerewolfBaseAdmin
from werewolf.contrib.werewolf_cms.models import Page


class PageAdmin(WerewolfBaseAdmin):
    list_display = ['page', 'pk', 'status']
    change_list_template = "werewolf_cms/change_list.html"

    def changelist_view(self, request, extra_context=None):
        """Renders the change view."""
        opts = self.model._meta
        context = {
            "sync_url": reverse("%s:%s_%s_synclist" % (self.admin_site.name, opts.app_label, opts.module_name)),
        }
        context.update(extra_context or {})
        return super(PageAdmin, self).changelist_view(request, context)

    def get_urls(self):
        """Returns the additional urls used by the Reversion admin."""
        urls = super(PageAdmin, self).get_urls()
        admin_site = self.admin_site
        opts = self.model._meta
        info = opts.app_label, opts.module_name,
        reversion_urls = patterns(
            "",
            url("^synchronize/$", admin_site.admin_view(self.synclist_view), name='%s_%s_synclist' % info),
        )
        return reversion_urls + urls

    def synclist_view(self, request, extra_context=None):
        """Displays a deleted model to allow recovery."""
        pages = dict([(p.page.pk, p) for p in Page.objects.all()])
        for page in cms_models.Page.objects.all():
            if page.pk in pages:
                pp = pages[page.pk]
                pages.pop(page.pk)
            else:
                pp = Page(page=page)
            pp.status = 'draft' if page.publisher_is_draft else 'published'
            pp.save()
        for p in pages.values():
            p.delete()
        opts = self.model._meta
        return HttpResponseRedirect(reverse("%s:%s_%s_changelist" % (self.admin_site.name, opts.app_label, opts.module_name)))

admin.site.register(Page, PageAdmin)
