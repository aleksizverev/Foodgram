from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required
from .models import Recipe, User, RecipeIngredient, Ingredient
from .forms import RecipeForm
from .utils import get_ingredients


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
    ingredients = recipe.recipeingredient_set.all()
    return render(request, 'recipes/recipe.html', {
        'recipe': recipe,
        'ingredients': ingredients
    })


# @login_required
# def new_recipe(request):
#     if request.method == "POST":
#         form = RecipeForm(request.POST)
#         if form.is_valid():
#             _new_recipe = form.save(commit=False)
#             _new_recipe.author = request.user
#             _new_recipe.save()
#             return redirect("index")
#         return render(request, "recipes/new_recipe.html", {"form": form})
#
#     form = RecipeForm()
#     return render(request, 'recipes/new_recipe.html', {"form": form})

def ingredients(request):
    query = request.GET.get('query')
    filtered_ingredients = Ingredient.objects.filter(title__icontains=query).all()
    data = []

    for ingredient in filtered_ingredients:
        data.append({'title': ingredient.title, 'dimension': ingredient.dimension})

    return JsonResponse(data, safe=False)


@login_required
def new_recipe(request):
    new_recipe = True

    if request.method == 'POST':
        form = RecipeForm(request.POST, files=request.FILES or None)
        ingredients = get_ingredients(request)

        if not bool(ingredients):
            form.add_error(None, "Добавьте хотя бы один ингредиент")

        elif form.is_valid():
            recipe = form.save(commit=False)
            recipe.author = request.user
            recipe.save()

            objs = [RecipeIngredient(
                amount=amount, ingredient=Ingredient.objects.get(title=title),
                recipe=recipe) for title, amount in ingredients.items()]

            RecipeIngredient.objects.bulk_create(objs)
            form.save_m2m()
            return redirect('recipe_view', recipe_id=recipe.id)

    else:
        form = RecipeForm(files=request.FILES or None)

    return render(request, 'recipes/new_recipe.html', {
        'form': form, 'new_recipe': new_recipe})
