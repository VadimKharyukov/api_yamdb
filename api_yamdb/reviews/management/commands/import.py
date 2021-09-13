import io, csv
from django.core.management.base import BaseCommand
from reviews.models import Title, Category, Genre, GenreTitle

DATA_PATH = 'static/data/'


class Command(BaseCommand):

    help = 'Import data from project CSV files'

    def add_arguments(self, parser):
        parser.add_argument('file_name')
        parser.add_argument('model_name')

    def handle(self, *args, **options):
        with io.open(DATA_PATH + options['file_name'], mode="r", encoding="utf-8") as f_obj:
            reader = csv.DictReader(f_obj, delimiter=',')
            for line in reader:
                model = globals().get(options['model_name'])
                model.objects.create(**line)