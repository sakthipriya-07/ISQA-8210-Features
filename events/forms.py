from django import forms
from .models import Customer, User


class SendEmailForm(forms.Form):

    subject = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'Subject'}))
    message = forms.CharField(widget=forms.Textarea)
    users = forms.ModelMultipleChoiceField(label="To", queryset=User.objects.all(),
                                           widget=forms.SelectMultiple())
