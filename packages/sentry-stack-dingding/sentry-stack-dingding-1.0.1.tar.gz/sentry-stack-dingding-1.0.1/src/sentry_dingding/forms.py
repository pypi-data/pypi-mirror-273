# coding: utf-8

from django import forms


class DingDingOptionsForm(forms.Form):
    access_token = forms.CharField(
        max_length=255,
        help_text='DingTalk robot access_token'
    )
    stack_deep = forms.IntegerField(
        initial=50,
        help_text='The number of stack trace lines to send'
    )
