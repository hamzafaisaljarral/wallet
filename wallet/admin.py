# -*- coding: utf-8 -*-

from django.contrib import admin
from django.utils.translation import ugettext_lazy as _, ungettext

from .models import Wallet



class Walletadmin(admin.ModelAdmin):
    list_display = ('freelanceprofile', 'jobpaidfor', 'paidby', 'pendingpayment', 'amount', 'is_accepted', 'is_rejected','end_date', )

    fieldsets = (
        (None, {
            'fields': (
                'freelanceprofile', 'jobpaidfor', 'paidby', 'pendingpayment', 'amount', 'is_accepted',
                'is_rejected','end_date',

            ),
        }),

        (_(u'Internal'), {
            'classes': ('collapse',),
            'fields': (
                'contact_date',
                'was_contacted',
                'notes',
            ),
        }),
        (_(u'Refering page'), {
            'fields': (
                'referer',
            ),
        }),
    )

    def set_was_contacted(self, request, queryset):
        affected = queryset.update(was_contacted=True)
        kind = self.model._meta.verbose_name.title() if affected == 1 else self.model._meta.verbose_name_plural.title()
        self.message_user(request,
                          ungettext(u"%(num)d %(kind)s was set as contacted", "%(num)d %(kind)s were set as contacted",
                                    affected) % {'num': affected, 'kind': kind})

    def unset_was_contacted(self, request, queryset):
        affected = queryset.update(was_contacted=False)
        kind = self.model._meta.verbose_name.title() if affected == 1 else self.model._meta.verbose_name_plural.title()
        self.message_user(request, ungettext(u"%(num)d %(kind)s was unset as contacted",
                                             "%(num)d %(kind)s were unset as contacted", affected) % {'num': affected,
                                                                                                      'kind': kind})


admin.site.register(Wallet,Walletadmin,)
