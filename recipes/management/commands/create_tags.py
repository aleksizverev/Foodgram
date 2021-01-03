from django.core.management.base import BaseCommand

from recipes.models import Tag


class Command(BaseCommand):
    help = 'Load ingredients data to database'

    def handle(self, *args, **options):
        Tag.objects.create(title='Завтрак', color='orange', slug='breakfast')
        Tag.objects.create(title='Обед', color='green', slug='lunch')
        Tag.objects.create(title='Ужин', color='purple', slug='dinner')
