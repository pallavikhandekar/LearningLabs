from django import forms


class UploadFileForm(forms.Form):
    title = forms.CharField()
    file = forms.FileField(label='Select a profile Image')

       
