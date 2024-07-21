from django import forms

__all__ = ['TelegramAccountForm']


class TelegramAccountForm(forms.Form):
    name = forms.CharField(max_length=100)
    phone_number = forms.CharField(max_length=15)
    api_id = forms.CharField(max_length=50)
    api_hash = forms.CharField(max_length=50)
    phone_code_hash = forms.CharField(max_length=100, required=False)
    phone_code = forms.CharField(max_length=10, required=False)
