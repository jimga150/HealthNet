from django.db import models
from django.contrib.auth.models import User

"""
Message Manager that helps create Messages without too much code
"""


class MessageManager:
    def createMessage(self, sender, recipient, text, subject):
        message = self.createMessage(sender=sender, recipient=recipient, text=text, subject=subject)
        return message

"""
Message Model that creates a messsage object, using the sender, recipient, text, subject of the message
and stores it in the database
"""


class Message(models.Model):
    sender = models.ForeignKey(User, related_name='sender')
    recipient = models.ForeignKey(User, related_name='recipient')
    text = models.CharField(max_length=1000)
    subject = models.CharField(max_length=100)
    date = models.DateTimeField()
    viewed = models.BooleanField(default=False)

    objects = MessageManager()

    def __str__(self):
        return self.subject
