from django import forms


class UploadFileForm(forms.Form):
    title = forms.CharField(max_length=100)
    description = forms.CharField(max_length=5000, widget=forms.Textarea)
    file = forms.FileField()
