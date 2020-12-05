from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .models import Recipe


def index(request):
    return render(request, 'recipes/index.html', context={'username': request.user.username})


def recipe_view(request, recipe_id):
    recipe = get_object_or_404(Recipe, pk=recipe_id)
    return render(request, 'singlePageNotAuth.html', {
        'recipe': recipe
    })
