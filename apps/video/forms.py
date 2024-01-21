from django import forms
from video.models import Video


class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True


class MultipleFileField(forms.FileField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("widget", MultipleFileInput(
            attrs={'class': "form-control"}
        ))
        super().__init__(*args, **kwargs)

    def clean(self, data, initial=None):
        single_file_clean = super().clean
        if isinstance(data, (list, tuple)):
            result = [single_file_clean(d, initial) for d in data]
        else:
            result = single_file_clean(data, initial)
        return result


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
    file = MultipleFileField()
