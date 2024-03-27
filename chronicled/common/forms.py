from django import forms

from chronicled.common.models import Log


class LogForm(forms.ModelForm):

    class Meta:
        model = Log
        fields = ['rating', 'review_text', 'completed', 'first_time']
        widgets = {
            'rating': forms.RadioSelect(),
            'progress': forms.RadioSelect(),
        }