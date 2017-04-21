from django import forms
from .models import Message
from django.contrib.auth.models import User


class MessageForm(forms.ModelForm):

    class Meta:
        model = Message

        fields = {'recipient', 'subject', 'text'}

    recipient = forms.ModelChoiceField(queryset=User.objects.all(), required=True, empty_label="Select User",
                                       to_field_name="last_name")

    subject = forms.CharField(required=True, label="Subject")

    text = forms.CharField(required=True, label="Message")
