# Generated by Django 3.1.4 on 2020-12-16 11:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0007_favoriterecipe'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='favoriterecipe',
            name='recipe',
        ),
        migrations.AddField(
            model_name='favoriterecipe',
            name='recipe',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='favorite_recipe', to='recipes.recipe'),
        ),
    ]
