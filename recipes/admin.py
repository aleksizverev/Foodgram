from django.contrib import admin

from .models import Ingredient, Recipe, RecipeIngredient, ShoppingList, Follow, FavoriteRecipe


class IngredientAdmin(admin.ModelAdmin):
    list_display = ('title', 'dimension')
    list_filter = ('title',)


class RecipeIngredientInline(admin.TabularInline):
    model = Recipe.ingredients.through
    extra = 1


class RecipeAdmin(admin.ModelAdmin):
    inlines = (RecipeIngredientInline,)
    list_filter = ('title',)


class ShoppingListAdmin(admin.ModelAdmin):
    list_display = ('user', 'recipe')


class FollowAdmin(admin.ModelAdmin):
    list_display = ('author', 'user')


class FavoriteRecipeAdmin(admin.ModelAdmin):
    list_display = ('user', 'recipe')


admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(Recipe, RecipeAdmin)
admin.site.register(RecipeIngredient)
admin.site.register(ShoppingList, ShoppingListAdmin)
admin.site.register(Follow, FollowAdmin)
admin.site.register(FavoriteRecipe, FavoriteRecipeAdmin)

