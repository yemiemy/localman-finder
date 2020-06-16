from django import forms
from .models import Feedback

class FeedBackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ['fname', 'lname', 'image', 'message']