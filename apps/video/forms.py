from django import forms
from video.models import Video


class UploadFileForm(forms.Form):
    name = forms.CharField(max_length=100, label='Nome', widget=forms.TextInput(
        attrs={'class': "form-control"}
    ))
    title = forms.CharField(max_length=100, label='Titulo', widget=forms.TextInput(
        attrs={'class': "form-control"}
    ))
    description = forms.CharField(max_length=5000, label='Descrição', widget=forms.Textarea(
        attrs={
            'class': "form-control",
            'rows': 4
        }
    ))
    keywords = forms.CharField(max_length=500, label='Tags Youtube', widget=forms.TextInput(
        attrs={'class': "form-control"}
    ))
    type = forms.ChoiceField(choices=Video.TYPES, label='Tipo', widget=forms.Select(
        attrs={'class': "form-control"}
    ))
    file = forms.FileField(label='Arquivo', widget=forms.FileInput(
        attrs={'class': "form-control"}
    ))
