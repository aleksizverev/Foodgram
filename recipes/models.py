from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Ingredient(models.Model):
    title = models.CharField(max_length=128)
    dimension = models.CharField(max_length=32)

    def __str__(self):
        return '{title} ({dimension})'.format(title=self.title, dimension=self.dimension)


class Recipe(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='recipes')
    title = models.CharField(max_length=256)
    description = models.TextField(max_length=1024)
    image = models.ImageField(upload_to="recipes/", blank=False, null=True)
    cooking_time = models.IntegerField()
    ingredients = models.ManyToManyField(Ingredient, through='RecipeIngredient')
    pub_date = models.DateTimeField('date published', auto_now_add=True, null=True)

    def __str__(self):
        return self.title


class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    amount = models.IntegerField()


class Follow(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='following')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='follower')

    def __str__(self):
        return self.user.username
