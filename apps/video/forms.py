from django import forms


class UploadFileForm(forms.Form):
    title = forms.CharField(max_length=100, label='Titulo')
    description = forms.CharField(max_length=5000, widget=forms.Textarea, label='Descrição')
    file = forms.FileField(label='Arquivo')
