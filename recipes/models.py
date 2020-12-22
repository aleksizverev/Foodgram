from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Ingredient(models.Model):
    title = models.CharField(max_length=128)
    dimension = models.CharField(max_length=32)

    def __str__(self):
        return '{title} ({dimension})'.format(title=self.title, dimension=self.dimension)


class Tag(models.Model):
    title = models.CharField(max_length=255)
    color = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.title


class Recipe(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE,
                               related_name='recipes')
    title = models.CharField(max_length=256)
    description = models.TextField(max_length=1024)
    image = models.ImageField(upload_to="recipes/", blank=False, null=True)
    cooking_time = models.IntegerField()
    ingredients = models.ManyToManyField(Ingredient, through='RecipeIngredient')
    tags = models.ManyToManyField(Tag, related_name='recipes')
    pub_date = models.DateTimeField('date published', auto_now_add=True,
                                    null=True)

    def __str__(self):
        return self.title


class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    amount = models.IntegerField()


class Follow(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE,
                               related_name='following')
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             related_name='follower')

    def __str__(self):
        return self.user.username


class FavoriteRecipe(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='favorite_recipes'
    )

    recipe = models.ForeignKey(
        Recipe, on_delete=models.CASCADE, related_name='favorite_recipe',
        null=True
    )

    def __str__(self):
        return f'Избранные рецепты {self.user}'


class ShoppingList(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='shopping_list')

    recipe = models.ForeignKey(
        Recipe, related_name='shopping_list', null=True,
        on_delete=models.CASCADE)

    def __str__(self):
        return f'Список покупок {self.user}'
