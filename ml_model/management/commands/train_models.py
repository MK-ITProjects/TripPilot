from django.core.management.base import BaseCommand

from ml_model.ml import train_cost_model, train_crowd_model, train_cluster_model


class Command(BaseCommand):
    help = 'Generate the synthetic training dataset and (re)train all ML models.'

    def handle(self, *args, **options):
        self.stdout.write('Training crowd-level classifier (Decision Tree + Random Forest)...')
        crowd_result = train_crowd_model.train()
        self.stdout.write(self.style.SUCCESS(f'  -> {crowd_result}'))

        self.stdout.write('Training trip-cost Linear Regression model...')
        cost_result = train_cost_model.train()
        self.stdout.write(self.style.SUCCESS(f'  -> {cost_result}'))

        self.stdout.write('Training destination K-Means clustering model...')
        cluster_result = train_cluster_model.train()
        self.stdout.write(self.style.SUCCESS(f'  -> {cluster_result}'))

        self.stdout.write(self.style.SUCCESS('All ML models trained and saved to ml_model/trained_models/'))
