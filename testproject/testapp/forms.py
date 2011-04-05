from django import forms

class SimpleForm(forms.Form):
    first_name = forms.CharField(max_length=80)
    second_name = forms.CharField(max_length=80)
