from django import forms


class GoogleForm(forms.Form):
    question = forms.CharField()