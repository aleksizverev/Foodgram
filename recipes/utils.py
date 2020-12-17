def get_ingredients(request):
    ingredients = {}
    for key in request.POST:
        if key.startswith('nameIngredient'):
            value_ingredient = key[15:]

            ingredients[request.POST[key]] = request.POST[
                'valueIngredient_' + value_ingredient]

    return ingredients


def get_subs_list(request):
    user_author_list = request.user.follower.all()
    user_subscriptions = []
    for pair in user_author_list:
        user_subscriptions.append(pair.author)

    return user_subscriptions


def get_fav_list(request):
    user_recipe_list = request.user.favorite_recipes.all()
    user_favorites = []
    for pair in user_recipe_list:
        user_favorites.append(pair.recipe)

    return user_favorites
