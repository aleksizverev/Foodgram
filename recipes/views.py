import csv
import json

from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import F, Sum
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect, HttpResponse
from django.views.decorators.http import require_http_methods

from .forms import RecipeForm
from .models import Recipe, User, RecipeIngredient, Ingredient, Follow, \
    FavoriteRecipe, ShoppingList
from .utils import get_ingredients, get_subs_list, get_fav_list, get_shop_list


def index(request):
    recipes = Recipe.objects.order_by('-pub_date')
    paginator = Paginator(recipes, 6)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)

    fav_recipes = get_fav_list(request)
    purchases = get_shop_list(request)

    return render(
        request,
        'recipes/index.html',
        {
            'user': request.user,
            'page': page,
            'indx': True,
            'fav_recipes': fav_recipes,
            'purchases': purchases
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
    favorites_list = get_fav_list(request)
    purchases = get_shop_list(request)

    if request.user.username:
        follow_status = Follow.objects.filter(
            user=request.user, author=recipe.author).exists()

    return render(request, 'recipes/single_recipe_view.html', {
        'user': request.user,
        'recipe': recipe,
        'ingredients': ingredients,
        'follow_status': follow_status,
        'favorites_list': favorites_list,
        'purchases': purchases,
    })


def ingredients(request):
    query = request.GET.get('query')
    filtered_ingredients = Ingredient.objects.filter(
        title__icontains=query).all()
    data = []

    for ingredient in filtered_ingredients:
        data.append({
            'title': ingredient.title, 'dimension': ingredient.dimension
        })

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
        'form': form, 'new_recipe': True})


@login_required
def recipe_edit(request, recipe_id):

    recipe = get_object_or_404(Recipe, pk=recipe_id)

    if request.user != recipe.author:
        return redirect('recipe_view', recipe_id=recipe_id)

    if request.method == 'POST':
        form = RecipeForm(
            request.POST, files=request.FILES or None, instance=recipe)
        ingredients = get_ingredients(request)

        if not bool(ingredients):
            form.add_error(None, "Добавьте хотя бы один ингредиент")

        if form.is_valid():
            form.save()
            recipe.recipeingredient_set.all().delete()
            objs = [RecipeIngredient(
                amount=amount, ingredient=Ingredient.objects.get(title=title),
                recipe=recipe) for title, amount in ingredients.items()]

            RecipeIngredient.objects.bulk_create(objs)
            return redirect('recipe_view', recipe_id=recipe_id)
    else:
        form = RecipeForm(instance=recipe)

    return render(
        request, 'recipes/new_recipe.html',
        {'form': form, 'new_recipe': True, 'edit': True})


@login_required
def delete_recipe(request, recipe_id):
    recipe = get_object_or_404(Recipe, pk=recipe_id)
    if request.user == recipe.author:
        recipe.delete()
        return redirect('profile', request.user)
    return redirect('index')


@login_required
def user_subscriptions(request):
    user_sub_list = get_subs_list(request)
    paginator = Paginator(user_sub_list, 6)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)

    return render(
        request,
        'recipes/user_subscriptions.html',
        {
            'page': page,
            'paginator': paginator,
            'subs': True
        }
    )


@login_required
@require_http_methods(['POST'])
def add_recipe_to_fav(request):
    recipe_id = json.loads(request.body).get('id')
    recipe = get_object_or_404(Recipe, pk=recipe_id)

    FavoriteRecipe.objects.get_or_create(
        user=request.user,
        recipe=recipe
    )
    return JsonResponse({'success': True})


@login_required
@require_http_methods(['DELETE'])
def del_recipe_from_fav(request, recipe_id):
    recipe = get_object_or_404(Recipe, pk=recipe_id)
    FavoriteRecipe.objects.filter(recipe=recipe, user=request.user).delete()
    return JsonResponse({'success': True})


@login_required
def fav_recipes(request):
    user_fav_recipes = get_fav_list(request)
    paginator = Paginator(user_fav_recipes, 6)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)

    return render(
        request,
        'recipes/favorite.html',
        {
            'page': page,
            'paginator': paginator,
            'fav_page': True
        }
    )


@login_required
def shopping_list(request):
    purchases = get_shop_list(request)
    return render(
        request,
        'recipes/shopping_list.html',
        {
            'shopping': True,
            'purchases': purchases
         }
    )


@login_required
@require_http_methods(['POST'])
def add_to_purchases(request):
    recipe_id = json.loads(request.body).get('id')
    recipe = get_object_or_404(Recipe, pk=recipe_id)
    ShoppingList.objects.get_or_create(user=request.user, recipe=recipe)

    return JsonResponse({'success': True})


@login_required
@require_http_methods(['DELETE'])
def remove_from_purchases(request, recipe_id):
    recipe = get_object_or_404(Recipe, pk=recipe_id)
    ShoppingList.objects.filter(recipe=recipe, user=request.user).delete()

    return JsonResponse({'success': True})


@login_required
def download_shopping_list(request):
    purchases = get_shop_list(request)
    ingredients = {}

    # for recipe in purchases:
    #     ingredients.append(recipe.recipeingredient_set.all().annotate(
    #         title=F('ingredient__title'),
    #         dimension=F('ingredient__dimension')
    #     ).values('title', 'dimension').annotate(
    #         sums=Sum('amount')
    #     ).order_by('title'))

    for recipe in purchases:
        for recipe_ingr in recipe.recipeingredient_set.all():
            if recipe_ingr.ingredient.title not in ingredients.keys():
                ingredients[recipe_ingr.ingredient.title] = [
                    recipe_ingr.amount, recipe_ingr.ingredient.dimension]
            else:
                ingredients[recipe_ingr.ingredient.title][0] += recipe_ingr.amount

    print(ingredients)

    response = HttpResponse(content_type='text/txt')
    response['Content-Disposition'] = 'attachment; filename="shop-list.txt"'

    writer = csv.writer(response)

    for key, value in ingredients.items():
        writer.writerow([f'{key} ({value[1]}) - {value[0]}'])

    return response
