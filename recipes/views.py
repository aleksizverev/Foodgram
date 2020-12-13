import json

from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.http import require_http_methods

from .forms import RecipeForm
from .models import Recipe, User, RecipeIngredient, Ingredient, Follow
from .utils import get_ingredients, get_subs_list


def index(request):
    recipes = Recipe.objects.order_by('-pub_date')
    paginator = Paginator(recipes, 6)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)

    return render(
        request,
        'recipes/index.html',
        {
            'user': request.user,
            'page': page,
            'indx': True
        }
    )


def profile(request, username):
    profile = get_object_or_404(User, username=username)
    profile_recipes = profile.recipes.order_by('-pub_date')
    paginator = Paginator(profile_recipes, 6)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)

    return render(
        request,
        'recipes/profile.html',
        {
            'profile': profile,
            'page': page
        }
    )


def recipe_view(request, recipe_id):
    recipe = get_object_or_404(Recipe, pk=recipe_id)
    ingredients = recipe.recipeingredient_set.all()
    follow_status = None
    if request.user.username:
        follow_status = Follow.objects.filter(
            user=request.user, author=recipe.author).exists()

    return render(request, 'recipes/single_recipe_view.html', {
        'user': request.user,
        'recipe': recipe,
        'ingredients': ingredients,
        'follow_status': follow_status
    })


def ingredients(request):
    query = request.GET.get('query')
    filtered_ingredients = Ingredient.objects.filter(title__icontains=query).all()
    data = []

    for ingredient in filtered_ingredients:
        data.append({'title': ingredient.title, 'dimension': ingredient.dimension})

    return JsonResponse(data, safe=False)


@login_required
@require_http_methods(['POST'])
def add_subscription(request):
    author_id = json.loads(request.body).get('id')
    author = get_object_or_404(User, pk=author_id)

    if author == request.user:
        return JsonResponse({'success': False})

    Follow.objects.get_or_create(author=author, user=request.user)
    return JsonResponse({'success': True})


@login_required
@require_http_methods(['DELETE'])
def remove_subscription(request, author_id):
    recipe_author = get_object_or_404(User, pk=author_id)
    if recipe_author == request.user:
        return JsonResponse({'success': False})
    Follow.objects.filter(author=recipe_author, user=request.user).delete()
    return JsonResponse({'success': True})


@login_required
def new_recipe(request):
    new_recipe = True

    if request.method == 'POST':
        form = RecipeForm(request.POST, files=request.FILES or None)
        ingredients = get_ingredients(request)

        if not bool(ingredients):
            print("Добавьте хотя бы один ингредиент")
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


@login_required
def user_subscriptions(request):
    user_sub_list = get_subs_list(request)
    print(user_sub_list)
    paginator = Paginator(user_sub_list, 6)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)

    return render(request, 'recipes/user_subscriptions.html', {
        'page': page,
        'paginator': paginator,
        'subs': True
    })
