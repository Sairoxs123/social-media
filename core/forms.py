from django import forms
from django.forms import ModelForm
from .models import Posts, Messages

class CreatePostForm(ModelForm):
    files = forms.FileField(widget=forms.TextInput(attrs={
        "name":"files",
        "type":"File",
        "class": "form-control",
        "multiple": "True",
    }), label="")
    class Meta:
        model = Posts
        fields = ('files', 'caption')

        widgets = {
            'caption': forms.Textarea(attrs={'class':'form-control', 'placeholder':'Enter Caption:', 'maxlength':1000})
        }

