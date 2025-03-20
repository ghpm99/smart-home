from django import forms
from video.models import Video


class ApontamentoForm(forms.Form):
    name = forms.CharField(max_length=256, label="Nome", widget=forms.TextInput(attrs={"class": "form-control"}))
    observation = forms.CharField(
        max_length=256, label="Observação", required=False, widget=forms.TextInput(attrs={"class": "form-control"})
    )
