from django import forms
from .models import Game


class GameForm(forms.ModelForm):
    class Meta:
        model = Game
        fields = [
            "title",
            "description",
            "release_date",
            "developer",
            "publisher",
            "rating",
        ]
        widgets = {
            "title": forms.TextInput(attrs={"class": "form-input"}),
            "description": forms.Textarea(attrs={"class": "form-input", "rows": 5}),
            "release_date": forms.DateInput(attrs={"class": "form-input", "type": "date"}),
            "developer": forms.TextInput(attrs={"class": "form-input"}),
            "publisher": forms.TextInput(attrs={"class": "form-input"}),
            "rating": forms.NumberInput(attrs={"class": "form-input"}),
        }
