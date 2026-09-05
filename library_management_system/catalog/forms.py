from django import forms

from .models import Review


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ('puntuacion', 'comentario')
        widgets = {
            'puntuacion': forms.Select(choices=[(value, f'{value} / 5') for value in range(1, 6)]),
            'comentario': forms.Textarea(attrs={'rows': 4, 'maxlength': 1000}),
        }