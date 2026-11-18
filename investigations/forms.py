from django import forms
from .models import Investigation, FixAttempt


class InvestigationForm(forms.ModelForm):

    class Meta:
        model = Investigation
        fields = ["title", "description", "priority", "status"]

class FixAttemptForm(forms.ModelForm):
    class Meta:
        model = FixAttempt
        fields = ["description", "solution", "result"]