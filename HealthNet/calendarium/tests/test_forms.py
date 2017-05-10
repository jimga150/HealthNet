"""Tests for the forms of the ``calendarium`` app."""
import json

from django.forms.models import model_to_dict
from django.test import TestCase
from django.utils.timezone import timedelta

from mixer.backend.django import mixer

from ..constants import FREQUENCIES, OCCURRENCE_DECISIONS
from ..forms import OccurrenceForm
from ..models import Event, Occurrence
from ..utils import now


class OccurrenceFormTestCase(TestCase):
    """Test for the ``OccurrenceForm`` form class."""
    longMessage = True

    def setUp(self):
        # single, not recurring event
        self.event = mixer.blend('calendarium.Event', rule=None,
                                 end_recurring_period=None)
        self.event_occurrence = next(self.event.get_occurrences(
            self.event.start))


    def test_form(self):
        """Test if ``OccurrenceForm`` is valid and saves correctly."""
        # Test for not recurring event
        data = model_to_dict(self.event_occurrence)
        initial = data.copy()
        data.update({
            'decision': OCCURRENCE_DECISIONS['all'],
            'created_by': None,
            'category': None,
            'title': 'changed'})
        form = OccurrenceForm(data=data, initial=initial)
        self.assertTrue(form.is_valid(), msg=(
            'The OccurrenceForm should be valid'))
        form.save()
        event = Event.objects.get(pk=self.event.pk)
        self.assertEqual(event.title, 'changed', msg=(
            'When save is called, the event\'s title should be "changed".'))


