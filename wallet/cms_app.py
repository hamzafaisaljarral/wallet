# -*- coding: utf-8 -*-

from cms.app_base import CMSApp
from cms.apphook_pool import apphook_pool


class JobFormApphook(CMSApp):
    name = u"Blogs"

    def get_urls(self, page=None, language=None, **kwargs):
        return ["myshop.urls.example"]


apphook_pool.register(BlogFormApphook)
