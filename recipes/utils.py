import csv

from django.shortcuts import HttpResponse


def get_ingredients(post_request_elements):
    ingredients = {}
    for key in post_request_elements:
        if key.startswith('nameIngredient'):
            value_ingredient = key[15:]

            ingredients[post_request_elements[key]] = post_request_elements[
                'valueIngredient_' + value_ingredient]

    return ingredients


def create_shopping_list_response(ingredients_list):
    response = HttpResponse(content_type='text/txt')

    response['Content-Disposition'] = 'attachment; filename="shop-list.txt"'

    writer = csv.writer(response)
    for ingredient in ingredients_list:
        title = ingredient['title']
        dimension = ingredient['dimension']
        total = ingredient['total']
        writer.writerow([f'{title} ({dimension}) - {total}'])

    return response
