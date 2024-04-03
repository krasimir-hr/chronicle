from django import forms

from chronicled.common.models import Log, Comment


class LogForm(forms.ModelForm):
    def __init__(self, platform_choices, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['platform_id'].widget = forms.Select(choices=platform_choices)

    class Meta:
        model = Log
        fields = ['rating', 'review_text', 'completed', 'first_time', 'platform_id']
        widgets = {
            'rating': forms.RadioSelect(),
            'progress': forms.RadioSelect(),
        }


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']
        widgets = {
            'text': forms.Textarea(attrs={'placeholder': 'Add comment...'})
        }