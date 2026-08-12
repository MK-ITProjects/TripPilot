from django.core.management.base import BaseCommand

from destinations.models import Destination
from scraper.models import WeatherData
from scraper.scraping import fetch_weather


class Command(BaseCommand):
    help = 'Fetch current weather for every distinct destination city.'

    def handle(self, *args, **options):
        cities = set(Destination.objects.exclude(city='').values_list('city', flat=True))
        cities |= set(Destination.objects.filter(city='').values_list('country', flat=True))

        created = 0
        for city in cities:
            try:
                data = fetch_weather(city)
            except Exception as exc:
                self.stderr.write(f'  ! {city}: {exc}')
                continue

            if not data:
                self.stdout.write(f'  - {city}: no weather data found')
                continue

            WeatherData.objects.create(**data)
            created += 1
            self.stdout.write(f'  + {city}: {data["temperature_c"]}°C, {data["condition"]}')

        self.stdout.write(self.style.SUCCESS(f'Fetched weather for {created} cities.'))
