# -*- coding: utf-8 -*-

from django import forms
from django.forms import ModelForm

from .models import Profile


class ProfileBaseForm(ModelForm):
    class Meta:
        abstract = True

    required_css_class = 'required'

    #
    # To help prevent people sending a typo’ed email address, then wondering
    # why we never got back to them, we'll require them to provide their email
    # twice.
    #
    verify_email = forms.EmailField(
        label=u'Verify email',
        help_text=u'Please retype your email address here.',
        max_length=255,
        required=True,
    )

    required_fields = []



class ProfileForm(ProfileBaseForm):

    images=forms.ImageField(help_text="Upload image: ", required=False)

    class Meta:
        model = Profile
        fields = [
            'name','images', 'description', 'referer',
        ]
        widgets = {
            'referer': forms.HiddenInput(),

        }


    required_fields = ['name', 'email', 'verify_email', ]



class ProfileAjaxForm(ProfileBaseForm):
    images=forms.ImageField(help_text="Upload image: ", required=False)
    class Meta:
        model = Profile
        fields = ['name','images', 'description','referer', ]
        widgets = { 'referer': forms.HiddenInput(),}





