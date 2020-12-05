from django.contrib import admin

from .models import Ingredient, Recipe, RecipeIngredient

class IngredientAdmin(admin.ModelAdmin):
    list_display = ('title', 'dimension')


class RecipeIngredientInline(admin.TabularInline):
    model = Recipe.ingredients.through
    extra = 1

class RecipeAdmin(admin.ModelAdmin):
    inlines = (RecipeIngredientInline,)


admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(Recipe, RecipeAdmin)
admin.site.register(RecipeIngredient)
