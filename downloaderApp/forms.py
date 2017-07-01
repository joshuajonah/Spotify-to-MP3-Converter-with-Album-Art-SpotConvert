from django import forms

class submitURLForm(forms.Form):
    uri = forms.CharField(max_length = 256)

