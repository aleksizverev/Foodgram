# Generated by Django 3.1.4 on 2020-12-19 20:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0012_auto_20201219_2043'),
    ]

    operations = [
        migrations.RenameField(
            model_name='shoppinglist',
            old_name='recipes',
            new_name='recipe',
        ),
    ]
