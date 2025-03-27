import csv

from django.core.management.base import BaseCommand

from letters_packages.settings import BASE_DIR
from packages.models import Client, PostOffice

path = str(BASE_DIR / 'static/data/')

models = {
    Client: 'clients.csv',
    PostOffice: 'post_offices.csv',
}


class Command(BaseCommand):
    help = 'Импорт клиентов и почтовых пунктов из CSV-файла в базу данных'

    def handle(self, *args, **options):
        for model, csv_file in models.items():
            with open(path + '/' + csv_file, 'r', encoding='utf-8') as file:
                try:
                    rows = csv.DictReader(file, delimiter=';')
                    records = [model(**row) for row in rows]
                    model.objects.bulk_create(records)
                    self.stdout.write(
                        self.style.SUCCESS(
                            f'База заполнена (модель {model.__name__})'
                        )
                    )
                except Exception as error:
                    self.stdout.write(
                        self.style.ERROR(
                            f'Ошибка {error} при записи {model.__name__}'
                        )
                    )
