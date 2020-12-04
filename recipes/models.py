from django.db import models


class Ingredient(models.Model):
    title = models.CharField(max_length=128)
    dimension = models.CharField(max_length=32)

    def __str__(self):
        return '{title} ({unit})'.format(title=self.title, dimension=self.dimension)
