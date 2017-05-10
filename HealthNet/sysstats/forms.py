from django import forms
from datetimewidget.widgets import DateWidget


class DateFilterForm(forms.Form):
    """
    Very simple form responsible for specifying what dates to filter the system stats by.
    """
    start_date = forms.DateField(widget=DateWidget(usel10n=True, bootstrap_version=3))
    end_date = forms.DateField(widget=DateWidget(usel10n=True, bootstrap_version=3))

    class Meta:
        fields = ('start_date', 'end_date')
