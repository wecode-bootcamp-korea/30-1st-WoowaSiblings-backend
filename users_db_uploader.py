import os, django, csv

from pathlib import Path

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'moonbanggu.settings')
django.setup()

from users.models import Batch

CSV_PATH_BATCH = 'csv/batches.csv'

def insert_batch():
    with open(CSV_PATH_BATCH) as in_file:
        data_reader = csv.reader(in_file)
        next(data_reader, None)
        for row in data_reader:
            Batch.objects.create(
                batch = row[0]
            )

if __name__ == "__main__":
    insert_batch()