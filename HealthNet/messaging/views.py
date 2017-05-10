from django.contrib.auth.models import User
from django.shortcuts import render
from .models import Message
from .forms import MessageForm
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse_lazy
from django.views.generic.edit import UpdateView, DeleteView
from django.utils import timezone

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin


@login_required
def index(request):
    """
    displays the main page of the messaging system
    :param request: Self explanatory
    :return: render containing the html page and all the messages for the user
    """

    messages = Message.objects.filter(recipient=request.user).order_by('date').reverse()

    return render(request, "messages_main.html", {'messages': messages})


@login_required
def createMessage(request):
    """
    Creates a message that can be sent to other users
    :param request: Self explanatory
    :return: render containing the html page and the info needed for the message to be sent
    """
    if request.method == 'POST':
        message_form = MessageForm(request.POST)

        if message_form.is_valid():

            message = message_form.save(commit=False)

            message.date = timezone.now()

            message.sender = request.user

            message_form.save()

            return HttpResponseRedirect(reverse_lazy('messages_home'))
    else:
        message_form = MessageForm()
        message_form.fields['recipient'].queryset=User.objects.all().exclude(pk=request.user.id)

    return render(request, 'messages_create.html', {'message_form': message_form})



class UpdateMessage(LoginRequiredMixin, UpdateView):
    """
    Allows for messages to be edited
    """
    model = Message

    template_name = 'messages_edit.html'

    form_class = MessageForm

    success_url = reverse_lazy('messages_home')


class DeleteMessage(LoginRequiredMixin, DeleteView):
    """
    Allows for messages to be deleted
    """

    model = Message

    template_name = 'messages_delete.html'

    success_url = reverse_lazy('messages_home')
