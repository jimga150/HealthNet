import json

from django.forms.models import model_to_dict
from django.test import TestCase
from django.utils.timezone import timedelta
from mixer.backend.django import mixer
from ..constants import FREQUENCIES, OCCURRENCE_DECISIONS
from ..forms import OccurrenceForm
from ..utils import now
from django.template.defaultfilters import slugify
from ..models import Event, EventCategory, Occurrence, Rule
from django.template import Context, Template
from django.utils import timezone
from ..templatetags.calendarium_tags import get_upcoming_events, get_week_URL
from django_libs.tests.mixins import ViewRequestFactoryTestMixin
from .. import views

class OccurrenceFormTestCase(TestCase):
    """Test for the ``OccurrenceForm`` form class."""
    longMessage = True

    def setUp(self):
        # single
        self.event = mixer.blend('calendarium.Event', rule=None,
                                 end_recurring_period=None)
        self.event_occurrence = next(self.event.get_occurrences(
            self.event.start))


    def test_form(self):
        """Test if ``OccurrenceForm`` is valid and saves correctly."""
        # Test for event
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

class RenderUpcomingEventsTestCase(TestCase):
    """Tests for the ``render_upcoming_events`` tag."""
    longMessage = True

    def setUp(self):
        self.occurrence = mixer.blend(
            'calendarium.Occurrence',
            start=timezone.now() + timezone.timedelta(days=1),
            end=timezone.now() + timezone.timedelta(days=2),
            original_start=timezone.now() + timezone.timedelta(seconds=20),
            event__start=timezone.now() + timezone.timedelta(days=1),
            event__end=timezone.now() + timezone.timedelta(days=2),
            event__title='foo',
        )

    def test_render_tag(self):
        t = Template('{% load calendarium_tags %}{% render_upcoming_events %}')
        self.assertIn('foo', t.render(Context()))


class GetUpcomingEventsTestCase(TestCase):
    """Tests for the ``get_upcoming_events`` tag."""
    longMessage = True

    def setUp(self):
        self.occurrence = mixer.blend(
            'calendarium.Occurrence',
            start=timezone.now() + timezone.timedelta(days=1),
            end=timezone.now() + timezone.timedelta(days=2),
            original_start=timezone.now() + timezone.timedelta(seconds=20),
            event__start=timezone.now() + timezone.timedelta(days=1),
            event__end=timezone.now() + timezone.timedelta(days=2),
        )

    def test_tag(self):
        result = get_upcoming_events()
        self.assertEqual(len(result), 1)


class GetWeekURLTestCase(TestCase):
    """Tests for the ``get_week_URL`` tag."""
    longMessage = True

    def test_tag(self):
        result = get_week_URL(
            timezone.datetime.strptime('2016-02-07', '%Y-%m-%d'))
        self.assertEqual(result, u'/calendar/2016/week/5/')

class CalendariumRedirectViewTestCase(ViewRequestFactoryTestMixin, TestCase):
    """Tests for the ``CalendariumRedirectView`` view."""
    view_class = views.CalendariumRedirectView

    def test_view(self):
        resp = self.client.get(self.get_url())
        self.assertEqual(resp.status_code, 200)


class MonthViewTestCase(ViewRequestFactoryTestMixin, TestCase):
    """Tests for the ``MonthView`` view class."""
    view_class = views.MonthView

    def get_view_kwargs(self):
        return {'year': self.year, 'month': self.month}

    def setUp(self):
        self.year = now().year
        self.month = now().month

    def test_view(self):
        """Test for the ``MonthView`` view class."""
        # regular call
        resp = self.is_callable()
        self.assertEqual(
            resp.template_name[0], 'calendarium/calendar_month.html', msg=(
                'Returned the wrong template.'))
        self.is_postable(data={'next': True}, to_url_name='calendar_month')
        self.is_postable(data={'previous': True}, to_url_name='calendar_month')
        self.is_postable(data={'today': True}, to_url_name='calendar_month')

        # called with a invalid category pk
        self.is_callable(data={'category': 'abc'})

        # called with a non-existant category pk
        self.is_callable(data={'category': '999'})

        # called with a category pk
        category = mixer.blend('calendarium.EventCategory')
        self.is_callable(data={'category': category.pk})

        # called with wrong values
        self.is_not_callable(kwargs={'year': 2000, 'month': 15})


class WeekViewTestCase(ViewRequestFactoryTestMixin, TestCase):
    """Tests for the ``WeekView`` view class."""
    view_class = views.WeekView

    def get_view_kwargs(self):
        return {'year': self.year, 'week': self.week}

    def setUp(self):
        self.year = now().year
        # current week number
        self.week = now().date().isocalendar()[1]

    def test_view(self):
        """Tests for the ``WeekView`` view class."""
        resp = self.is_callable()
        self.assertEqual(
            resp.template_name[0], 'calendarium/calendar_week.html', msg=(
                'Returned the wrong template.'))
        self.is_postable(data={'next': True}, to_url_name='calendar_week')
        self.is_postable(data={'previous': True}, to_url_name='calendar_week')
        self.is_postable(data={'today': True}, to_url_name='calendar_week')

        resp = self.is_callable(ajax=True)
        self.assertEqual(
            resp.template_name[0], 'calendarium/partials/calendar_week.html',
            msg=('Returned the wrong template for AJAX request.'))
        self.is_not_callable(kwargs={'year': self.year, 'week': '60'})


class DayViewTestCase(ViewRequestFactoryTestMixin, TestCase):
    """Tests for the ``DayView`` view class."""
    view_class = views.DayView

    def get_view_kwargs(self):
        return {'year': self.year, 'month': self.month, 'day': self.day}

    def setUp(self):
        self.year = 2001
        self.month = 2
        self.day = 15

    def test_view(self):
        """Tests for the ``DayView`` view class."""
        resp = self.is_callable()
        self.assertEqual(
            resp.template_name[0], 'calendarium/calendar_day.html', msg=(
                'Returned the wrong template.'))
        self.is_postable(data={'next': True}, to_url_name='calendar_day')
        self.is_postable(data={'previous': True}, to_url_name='calendar_day')
        self.is_postable(data={'today': True}, to_url_name='calendar_day')
        self.is_not_callable(kwargs={'year': self.year, 'month': '14',
                                     'day': self.day})


class EventUpdateViewTestCase(ViewRequestFactoryTestMixin, TestCase):
    """Tests for the ``EventUpdateView`` view class."""
    view_class = views.EventUpdateView

    def get_view_kwargs(self):
        return {'pk': self.event.pk}

    def setUp(self):
        self.event = mixer.blend('calendarium.Event')
        self.user = mixer.blend('auth.User', is_superuser=True)

    def test_view(self):
        self.is_callable(user=self.user)


class EventCreateViewTestCase(ViewRequestFactoryTestMixin, TestCase):
    """Tests for the ``EventCreateView`` view class."""
    view_class = views.EventCreateView

    def setUp(self):
        self.user = mixer.blend('auth.User', is_superuser=True)

    def test_view(self):
        self.is_callable(user=self.user)
        self.is_callable(user=self.user, data={'delete': True})
        self.assertEqual(Event.objects.all().count(), 0)


class EventDetailViewTestCase(ViewRequestFactoryTestMixin, TestCase):
    """Tests for the ``EventDetailView`` view class."""
    view_class = views.EventDetailView

    def get_view_kwargs(self):
        return {'pk': self.event.pk}

    def setUp(self):
        self.event = mixer.blend('calendarium.Event')

    def test_view(self):
        self.is_callable()


class OccurrenceViewTestCaseMixin(object):
    """Mixin to avoid repeating code for the Occurrence views."""
    def get_view_kwargs(self):
        return {
            'pk': self.event.pk,
            'year': self.event.start.date().year,
            'month': self.event.start.date().month,
            'day': self.event.start.date().day,
        }

    def setUp(self):
        self.rule = mixer.blend('calendarium.Rule', name='daily')
        self.event = mixer.blend(
            'calendarium.Event', created_by=mixer.blend('auth.User'),
            start=now() - timedelta(days=1), end=now() + timedelta(days=5),
            rule=self.rule)


class OccurrenceDetailViewTestCase(
        OccurrenceViewTestCaseMixin, ViewRequestFactoryTestMixin, TestCase):
    """Tests for the ``OccurrenceDetailView`` view class."""
    view_class = views.OccurrenceDetailView


class OccurrenceUpdateViewTestCase(
        OccurrenceViewTestCaseMixin, ViewRequestFactoryTestMixin, TestCase):
    """Tests for the ``OccurrenceUpdateView`` view class."""
    view_class = views.OccurrenceUpdateView


class UpcomingEventsAjaxViewTestCase(ViewRequestFactoryTestMixin, TestCase):
    """Tests for the ``UpcomingEventsAjaxView`` view class."""
    view_class = views.UpcomingEventsAjaxView

    def test_view(self):
        self.is_callable()

    def test_view_with_count(self):
        self.is_callable(data={'count': 5})

    def test_view_with_category(self):
        cat = mixer.blend('calendarium.EventCategory')
        self.is_callable(data={'category': cat.slug})
