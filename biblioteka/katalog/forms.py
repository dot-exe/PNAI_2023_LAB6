import datetime
from django import forms

from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


class ProlongataForm(forms.Form):
    data_prolongaty = forms.DateField(
        help_text="Wprowadz date, nie dalej niz 4 tygodnie"
    )

    def clean_data_prolongaty(self):
        data = self.cleaned_data['data_prolongaty']

        if data < datetime.date.today():
            raise ValidationError(_('niepoprawna data - przeszlosc'))

        if data > datetime.date.today() + datetime.timedelta(weeks=4):
            raise ValidationError(_('niepoprawna data - dalej niz 4 tygodnie'))

        return data
