from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .models import Recipe, User


def index(request):
    recipes = Recipe.objects.order_by('-pub_date')[:10]
    return render(
        request,
        'recipes/index.html',
        {
            'user': request.user,
            'recipes': recipes
        }
    )


def profile(request, username):
    profile = get_object_or_404(User, username=username)
    profile_recipes = profile.recipes.all()
    return render(
        request,
        'recipes/profile.html',
        {
            'profile': profile,
            'profile_recipes': profile_recipes
        },
    )


def recipe_view(request, recipe_id):
    recipe = get_object_or_404(Recipe, pk=recipe_id)
    return render(request, 'singlePageNotAuth.html', {
        'recipe': recipe
    })
