from django import forms
from .models import *
from django.forms import ModelForm


class ProfileForm(ModelForm):

    class Meta:
        model = Profiles
        fields = ('avatar',)
       

