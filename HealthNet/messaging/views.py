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

    messages = Message.objects.filter(recipient=request.user).order_by('date').reverse()

    return render(request, "messages_main.html", {'messages': messages})


@login_required
def createMessage(request):

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

    return render(request, 'messages_create.html', {'message_form': message_form})


class UpdateMessage(LoginRequiredMixin, UpdateView):

    model = Message

    template_name = 'messages_edit.html'

    form_class = MessageForm

    success_url = reverse_lazy('messages_home')


class DeleteMessage(LoginRequiredMixin, DeleteView):

    model = Message

    template_name = 'messages_delete.html'

    success_url = reverse_lazy('messages_home')
