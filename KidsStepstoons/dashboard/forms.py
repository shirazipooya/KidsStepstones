from typing import Any, Dict, Mapping, Optional, Type, Union
from django import forms
from django.core.files.base import File
from django.db.models.base import Model
from django.forms.utils import ErrorList
from account.models import User

class ProfileForm(forms.ModelForm):
    
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super(ProfileForm, self).__init__(*args, **kwargs)
        
        self.fields['username'].help_text = None
        
        if not user.is_superuser:
            self.fields['username'].disabled = True
            self.fields['email'].disabled = True
            self.fields['special_user'].disabled = True
            self.fields['is_author'].disabled = True

    
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'special_user', 'is_author', 'avatar']