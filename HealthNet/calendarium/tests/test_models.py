"""Tests for the models of the ``calendarium`` app."""
from django.test import TestCase
from django.utils.timezone import timedelta
from django.template.defaultfilters import slugify

from mixer.backend.django import mixer

from ..models import Event, EventCategory, Occurrence, Rule
from ..utils import now


class EventModelManagerTestCase(TestCase):
    """Tests for the ``EventModelManager`` custom manager."""
    longMessage = True

    def setUp(self):
        # event that only occurs once
        self.event = mixer.blend('calendarium.Event', rule=None, start=now(),
                                 end=now() + timedelta(hours=1))
        # event that occurs for one week daily with one custom occurrence
        self.event_daily = mixer.blend('calendarium.Event')
        self.occurrence = mixer.blend(
            'calendarium.Occurrence', event=self.event, original_start=now(),
            original_end=now() + timedelta(days=1), title='foo_occurrence')

class EventTestCase(TestCase):
    """Tests for the ``Event`` model."""
    longMessage = True

    def setUp(self):
        self.not_found_event = mixer.blend(
            'calendarium.Event', start=now() - timedelta(hours=24),
            end=now() - timedelta(hours=24),
            creation_date=now() - timedelta(hours=24), rule=None)
        self.event = mixer.blend(
            'calendarium.Event', start=now(), end=now(),
             creation_date=now())
            # category=mixer.blend('calendarium.EventCategory'))
        self.event_wp = mixer.blend(
            'calendarium.Event', start=now(), end=now(),
            creation_date=now(),

        )
        self.occurrence = mixer.blend(
            'calendarium.Occurrence', original_start=now(),
            original_end=now() + timedelta(days=1), event=self.event,
            title='foo_occurrence')
        self.single_time_event = mixer.blend('calendarium.Event', rule=None)

    def test_get_title(self):
        """Test for ``__str__`` method."""
        title = "The Title"
        event = mixer.blend(
            'calendarium.Event', start=now(), end=now(),
             creation_date=now(),
            title=title)
        self.assertEqual(title, str(event), msg=(
            'Method ``__str__`` did not output event title.'))

    def test_get_absolute_url(self):
        """Test for ``get_absolute_url`` method."""
        event = mixer.blend(
            'calendarium.Event', start=now(), end=now(),
             creation_date=now())
        event.save()
        self.assertTrue(str(event.pk) in str(event.get_absolute_url()), msg=(
            'Method ``get_absolute_url`` did not contain event id.'))

    def test_create_occurrence(self):
        """Test for ``_create_occurrence`` method."""
        occurrence = self.event._create_occurrence(now())
        self.assertEqual(type(occurrence), Occurrence, msg=(
            'Method ``_create_occurrence`` did not output the right type.'))


class EventCategoryTestCase(TestCase):
    """Tests for the ``EventCategory`` model."""
    longMessage = True

    def test_instantiation(self):
        """Test for instantiation of the ``EventCategory`` model."""
        event_category = EventCategory()
        self.assertTrue(event_category)

    def test_get_name(self):
        """Test for ``__str__`` method."""
        name = "The Name"
        event_category = EventCategory(name=name)
        self.assertEqual(name, str(event_category), msg=(
            'Method ``__str__`` did not output event category name.'))

    def test_get_slug(self):
        """Test slug in ``save`` method."""
        name = "The Name"
        event_category = EventCategory(name=name)
        event_category.save()
        self.assertEqual(slugify(name), str(event_category.slug), msg=(
            'Method ``save`` did not set event category slug as expected.'))


class EventRelationTestCase(TestCase):
    """Tests for the ``EventRelation`` model."""
    longMessage = True

    def test_instantiation(self):
        """Test for instantiation of the ``EventRelation`` model."""
        event_relation = mixer.blend('calendarium.EventRelation')
        self.assertTrue(event_relation)


class OccurrenceTestCase(TestCase):
    """Tests for the ``Occurrence`` model."""
    longMessage = True

    def test_instantiation(self):
        """Test for instantiation of the ``Occurrence`` model."""
        occurrence = Occurrence()
        self.assertTrue(occurrence)

    def test_delete_period(self):
        """Test for the ``delete_period`` function."""
        occurrence = mixer.blend('calendarium.Occurrence')
        occurrence.delete_period('all')
        self.assertEqual(Occurrence.objects.all().count(), 0, msg=(
            'Should delete only the first occurrence.'))

        event = mixer.blend(
            'calendarium.Event', start=now() - timedelta(hours=0),
            end=now() - timedelta(hours=0))
        occurrence = mixer.blend(
            'calendarium.Occurrence', event=event,
            start=now() - timedelta(hours=0), end=now() - timedelta(hours=0))
        occurrence.delete_period('this one')
        self.assertEqual(Occurrence.objects.all().count(), 0, msg=(
            'Should delete only the first occurrence.'))

        event = mixer.blend(
            'calendarium.Event', start=now() - timedelta(hours=0),
            end=now() - timedelta(hours=0))
        event.save()
        occurrence = mixer.blend(
            'calendarium.Occurrence', event=event,
            start=now() - timedelta(hours=0), end=now() - timedelta(hours=0))
        occurrence.delete_period('following')
        self.assertEqual(Event.objects.all().count(), 0, msg=(
            'Should delete the event and the occurrence.'))

        occurrence_1 = mixer.blend(
            'calendarium.Occurrence', start=now(),
            end=now() + timedelta(days=1),
            original_start=now() + timedelta(hours=1))
        occurrence_2 = mixer.blend(
            'calendarium.Occurrence', start=now(),
            end=now() + timedelta(days=1),
            original_start=now() + timedelta(hours=1))
        occurrence_2.event = occurrence_1.event
        occurrence_2.save()
        occurrence_2.delete_period('this one')
        occurrence_3 = mixer.blend(
            'calendarium.Occurrence', start=now(),
            end=now() + timedelta(days=1),
            original_start=now() + timedelta(hours=1))
        occurrence_3.event = occurrence_1.event
        occurrence_3.save()
        occurrence_4 = mixer.blend(
            'calendarium.Occurrence', start=now(),
            end=now() + timedelta(days=1),
            original_start=now() + timedelta(hours=1))
        occurrence_4.event = occurrence_1.event
        occurrence_4.save()
        occurrence_3.delete_period('this one')
        occurrence_1.delete_period('following')
        self.assertEqual(Occurrence.objects.all().count(), 0, msg=(
            'Should delete all occurrences with this start date.'))


class RuleTestCase(TestCase):
    """Tests for the ``Rule`` model."""
    longMessage = True

    def test_instantiation(self):
        """Test for instantiation of the ``Rule`` model."""
        rule = Rule()
        self.assertTrue(rule)
