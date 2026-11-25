from django import forms
from .models import Game


class GameForm(forms.ModelForm):
    
    rating = forms.DecimalField(
        min_value=0,
        max_value=10,
        max_digits=3,
        decimal_places=1,
        widget=forms.NumberInput(
            attrs={
                "class": "form-input",
                "min": "0",
                "max": "10",
                "step": "0.1",
            }
        )
    )

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
        }
