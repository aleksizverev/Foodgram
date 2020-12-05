from django.urls import path

from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('recipe/<int:recipe_id>/', views.recipe_view, name='recipe_view'),
]
