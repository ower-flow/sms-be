from django.core.exceptions import ValidationError
import datetime

def no_future_date(value):
    if value > datetime.date.today():
        raise ValidationError("Date cannot be in the future.")
