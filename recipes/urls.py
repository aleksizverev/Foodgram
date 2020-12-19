from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('add_purchases/', views.add_to_purchases, name='add_purchases'),
    path('remove_purchases/<int:recipe_id>/', views.remove_from_purchases, name='remove_purchases'),
    path('shopping_list/', views.shopping_list, name='shopping_list'),
    path('my_subscriptions/', views.user_subscriptions, name='user_subs'),
    path('recipes/del_from_favorites/<int:recipe_id>/', views.del_recipe_from_fav, name='del_from_fav'),
    path('<username>/', views.profile, name='profile'),
    path('recipes/favorites/', views.fav_recipes, name='fav_recipes'),
    path('recipes/add_to_favorites/', views.add_recipe_to_fav, name='add_to_fav'),
    path('recipes/new/', views.new_recipe, name='new_recipe'),
    path('ingredients/', views.ingredients, name='ingredients'),
    path('recipes/<int:recipe_id>/', views.recipe_view, name='recipe_view'),
    path('add_subscription', views.add_subscription, name='subscriptions'),
    path('remove_subscription/<int:author_id>/', views.remove_subscription, name='subscriptions')
]
