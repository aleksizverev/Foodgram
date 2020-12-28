import json

from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import F, Sum
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import resolve
from django.views.decorators.http import require_http_methods

from foodgram.settings import PAGINATE_BY
from .forms import RecipeForm
from .models import Recipe, User, RecipeIngredient, Ingredient, Follow, \
    FavoriteRecipe, ShoppingList, Tag
from .utils import get_ingredients, create_shopping_list_response


def index(request):
    recipes = Recipe.objects.order_by('-pub_date')

    if 'filters' in request.GET:
        filters = request.GET.getlist('filters')
        recipes = Recipe.objects.filter(
            tags__slug__in=filters).distinct().order_by('-pub_date')

    tags = Tag.objects.all()
    paginator = Paginator(recipes, PAGINATE_BY)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)

    current_url = resolve(request.path).url_name

    return render(
        request,
        'recipes/index.html',
        {
            'user': request.user,
            'page': page,
            'current_url': current_url,
            'tags': tags
        }
    )


def profile(request, username):
    profile = get_object_or_404(User, username=username)
    profile_recipes = profile.recipes.order_by('-pub_date')

    if 'filters' in request.GET:
        filters = request.GET.getlist('filters')
        profile_recipes = profile_recipes.filter(
            tags__slug__in=filters).distinct().order_by('-pub_date')

    paginator = Paginator(profile_recipes, PAGINATE_BY)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)

    tags = Tag.objects.all()

    return render(
        request,
        'recipes/profile.html',
        {
            'profile': profile,
            'page': page,
            'tags': tags
        }
    )


def recipe_view(request, recipe_id):
    recipe = get_object_or_404(Recipe, pk=recipe_id)
    ingredients = recipe.recipeingredient_set.all()
    tags = recipe.tags.all()

    return render(request, 'recipes/single_recipe_view.html', {
        'user': request.user,
        'recipe': recipe,
        'ingredients': ingredients,
        'tags': tags
    })


def get_requested_ingredients(request):
    query = request.GET.get('query')
    filtered_ingredients = list(Ingredient.objects.filter(
        title__icontains=query).values('title', 'dimension'))
    return JsonResponse(filtered_ingredients, safe=False)


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
        ingredients = get_ingredients(request.POST)

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

    current_url = resolve(request.path).url_name

    return render(request, 'recipes/new_recipe.html', {
        'form': form, 'current_url': current_url})


@login_required
def recipe_edit(request, recipe_id):

    recipe = get_object_or_404(Recipe, pk=recipe_id)

    if request.user != recipe.author:
        return redirect('recipe_view', recipe_id=recipe_id)

    if request.method == 'POST':
        form = RecipeForm(
            request.POST, files=request.FILES or None, instance=recipe)
        ingredients = get_ingredients(request.POST)

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
    user_sub_list = Follow.subscriptions.get_subs_list(request.user)
    paginator = Paginator(user_sub_list, PAGINATE_BY)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)

    current_url = resolve(request.path).url_name

    return render(
        request,
        'recipes/user_subscriptions.html',
        {
            'page': page,
            'paginator': paginator,
            'current_url': current_url
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
    user_fav_recipes = FavoriteRecipe.fav_recipes.get_fav_recipes(
        request.user).order_by('-recipe__pub_date')

    if 'filters' in request.GET:
        filters = request.GET.getlist('filters')
        user_fav_recipes = user_fav_recipes.filter(
            recipe__tags__slug__in=filters).distinct().order_by(
            '-recipe__pub_date')

    paginator = Paginator(user_fav_recipes, PAGINATE_BY)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)

    current_url = resolve(request.path).url_name
    tags = Tag.objects.all()

    return render(
        request,
        'recipes/favorite_recipes.html',
        {
            'page': page,
            'paginator': paginator,
            'current_url': current_url,
            'tags': tags
        }
    )


@login_required
def shopping_list(request):
    purchases = ShoppingList.shop_list.get_shopping_list(request.user)
    current_url = resolve(request.path).url_name
    return render(
        request,
        'recipes/shopping_list.html',
        {
            'current_url': current_url,
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
    purchases = ShoppingList.shop_list.get_shopping_list(request.user)

    ingredients_list = purchases.annotate(
        title=F('recipe__recipeingredient__ingredient__title'),
        dimension=F('recipe__recipeingredient__ingredient__dimension')
    ).values(
        'title', 'dimension'
    ).annotate(
        total=Sum('recipe__recipeingredient__amount')
    ).order_by('title')

    response = create_shopping_list_response(ingredients_list)

    return response
