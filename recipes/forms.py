from django import forms
from django.core.exceptions import ValidationError

from .models import Recipe, Ingredient


class RecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = ('title', 'cooking_time', 'description', 'image', 'tags')

    def clean_cooking_time(self):
        data = self.cleaned_data['cooking_time']
        if int(data) == 0:
            raise ValidationError('Время приготоления должно быть больше 0')

        return data

    def clean(self):
        ids_of_recipes = []
        for items in self.data.keys():
            if 'nameIngredient' in items:
                title, recipe_id = items.split('_')
                ids_of_recipes.append(recipe_id)

        for recipe_id in ids_of_recipes:
            title = self.data.get(f'nameIngredient_{recipe_id}')
            value = self.data.get(f'valueIngredient_{recipe_id}')

            if int(value) <= 0:
                raise ValidationError('Ингредиентов должно быть больше 0')

            is_exists = Ingredient.objects.filter(
                title=title).exists()

            if not is_exists:
                raise ValidationError('Выберите существующий ингредиент')
