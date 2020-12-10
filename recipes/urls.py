from django.urls import path

from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('new/', views.new_recipe, name='new_recipe'),
    path('ingredients/', views.ingredients, name='ingredients'),
    path('<username>/', views.profile, name='profile'),
    path('recipes/<int:recipe_id>/', views.recipe_view, name='recipe_view'),
]
