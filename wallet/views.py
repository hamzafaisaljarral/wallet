# -*- coding: utf-8 -*-
# Django 1.6


# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os
import json


from django.contrib import messages
from django.forms import formset_factory
from django.http import HttpResponse, HttpResponseRedirect, request, HttpResponseForbidden

from django.shortcuts import get_object_or_404, render, redirect, render_to_response
from django.template import RequestContext
from django.views.generic import FormView, TemplateView, ListView
from django.shortcuts import render
from django.http import JsonResponse

from cms.models.pagemodel import Page
from django.views.generic.edit import UpdateView
from .models import Profile, ProfilePluginModel
from .forms import ProfileBaseForm, ProfileAjaxForm
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.views import View
from django.urls import reverse
from django.urls import reverse_lazy



#
# This is used from the contact page, so, no AJAX is required. Its a normal
# POST submission.
#

class ProfileFormView(FormView):
    form_class = ProfileBaseForm
    template_name = 'contacts/contact_form.html'

    def get_initial(self):



        initial = super(ProfileFormView, self).get_initial()
        initial['referer'] = self.request.META.get('HTTP_REFERER', ''),
        return initial

    def get_success_url(self):
        page = get_object_or_404(
            Page,
            reverse_id='blog_form_submission',
            publisher_is_draft=False
        )
        return page.get_absolute_url()

    def form_valid(self, form):
        self.object = form.save()
        return super(ProfileFormView, self).form_valid(form)


#
# From: https://docs.djangoproject.com/en/1.6/topics/class-based-views/generic-editing/#ajax-example
#

class AjaxableResponseMixin(object):
    """
     Mixin to add AJAX support to a form.
     Must be used with an object-based FormView (e.g. CreateView)
    """

    def __init__(self):
        self.request = None
        self.object = Profile

    def render_to_json_response(self, context, **response_kwargs):
        data = json.dumps(context)
        response_kwargs['content_type'] = 'application/json'
        return HttpResponse(data, **response_kwargs)

    def form_invalid(self, form):
        response = super(AjaxableResponseMixin, self).form_invalid(form)
        if self.request.is_ajax():
            return self.render_to_json_response(form.errors)  # , status=400)
        else:
            return response

    def form_valid(self, form):
        # We make sure to call the parent's form_valid() method because
        # it might do some processing (in the case of CreateView, it will
        # call form.save() for example).
        response = super(AjaxableResponseMixin, self).form_valid(form)
        if self.request.is_ajax():
            data = {
                'pk': self.object.pk,
            }
            return self.render_to_json_response(data)
        else:
            return response


#
# This is used from the ContactPlugin, so could be anywhere on the site. It is
# submitted via AJAX and shouldn't take the user off the page.
#
class ProfileFormAjaxView(FormView):
    form_class = ProfileAjaxForm
    http_method_names = [u'post']  # Not interested in any GETs here...
    template_name = 'contacts/_contact_widget.html'
    form = ProfileAjaxForm(http_method_names)

    #
    # NOTE: Even though this will never be used, the FormView requires that
    # either the success_url property or the get_success_url() method is
    # defined. So, let use the sensible thing and set it to the page where
    # this plugin is coming from.
    #

    def get_success_url(self):
        page = get_object_or_404(
            Page,
            reverse_id='blog_form_submission',
            publisher_is_draft=False
        )
        return page.get_absolute_url()

    def form_valid(self, form):
        #AjaxableResponseMixin expects our contact object to be 'self.object'
        self.object = form.save(commit=True)
        return super(ProfileFormAjaxView, self).form_valid(form)


