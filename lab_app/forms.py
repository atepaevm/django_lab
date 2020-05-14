# forms.py
from django import forms
from .models import *


class UploadForm(forms.ModelForm):
    #user = LabUser.objects.get(pk=2)
    class Meta:
        model = LabReport
        fields = ['text', 'photo', 'lat', 'lng', 'status', 'comment']


class UserUploadForm(forms.ModelForm):
    class Meta:
        model = LabUser
        fields = ['name', 'email', 'hash', 'role']


class CommentForm(forms.ModelForm):
    class Meta:
        model = LabComment
        fields = ['user', 'report', 'text', 'time']