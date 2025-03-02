from django import forms

class FundUploadForm(forms.Form):
    csv_file = forms.FileField()
