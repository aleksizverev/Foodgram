from django import forms

from .models import Recipe, RecipeIngredient


class RecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = ('title', 'cooking_time', 'ingredients', 'description', 'image')

    ingredients = forms.ModelMultipleChoiceField(
        queryset=RecipeIngredient.objects.all()
    )