from django import forms
from .models import Message
from django.contrib.auth.models import User
from core.utils import UserChoiceField


class MessageForm(forms.ModelForm):
    """
    Form that displays and gets the information from the user for the message
    """

    class Meta:
        model = Message

        fields = ['recipient', 'subject', 'text']

    recipient = UserChoiceField(queryset=User.objects.all(), required=True, empty_label="Select Recipient")

    subject = forms.CharField(required=True, label="Subject")

    text = forms.CharField(required=True, label="Message")
