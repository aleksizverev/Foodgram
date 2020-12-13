from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('my_subscriptions/', views.user_subscriptions, name='user_subs'),
    path('recipes/new/', views.new_recipe, name='new_recipe'),
    path('ingredients/', views.ingredients, name='ingredients'),
    path('<username>/', views.profile, name='profile'),
    path('recipes/<int:recipe_id>/', views.recipe_view, name='recipe_view'),
    path('add_subscription', views.add_subscription, name='subscriptions'),
    path('remove_subscription/<int:author_id>', views.remove_subscription, name='subscriptions')
]
