from django.core.management.base import BaseCommand

from destinations.models import Destination
from scraper.models import ScrapedEvent, ScrapedHotelPrice
from scraper.scraping import simulate_events, simulate_hotel_prices


class Command(BaseCommand):
    help = 'Populate simulated hotel price and local event data for every destination city.'

    def handle(self, *args, **options):
        cities = set(Destination.objects.exclude(city='').values_list('city', flat=True))
        cities |= set(Destination.objects.filter(city='').values_list('country', flat=True))

        for city in cities:
            for hotel in simulate_hotel_prices(city):
                ScrapedHotelPrice.objects.update_or_create(
                    city=hotel['city'], hotel_name=hotel['hotel_name'],
                    defaults={'price_per_night': hotel['price_per_night'], 'rating': hotel['rating']},
                )
            for event in simulate_events(city):
                ScrapedEvent.objects.update_or_create(
                    city=event['city'], name=event['name'], event_date=event['event_date'],
                    defaults={'description': event['description']},
                )

        self.stdout.write(self.style.SUCCESS(f'Populated hotel/event data for {len(cities)} cities.'))
