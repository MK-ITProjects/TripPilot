import time

from django.core.management.base import BaseCommand

from destinations.models import Destination
from scraper.models import ScrapedAttraction
from scraper.scraping import scrape_wikipedia_summary


class Command(BaseCommand):
    help = 'Scrape a Wikipedia summary for every destination into ScrapedAttraction.'

    def handle(self, *args, **options):
        destinations = Destination.objects.all()
        created = 0
        for destination in destinations:
            lookup_names = [destination.name]
            if destination.city and destination.city != destination.name:
                lookup_names.append(destination.city)

            description = None
            matched_name = destination.name
            for name in lookup_names:
                try:
                    description = scrape_wikipedia_summary(name)
                except Exception as exc:  # network hiccups shouldn't kill the whole run
                    self.stderr.write(f'  ! {name}: {exc}')
                    continue
                if description:
                    matched_name = name
                    break

            if not description:
                self.stdout.write(f'  - {destination.name}: no summary found, skipping')
                continue

            ScrapedAttraction.objects.update_or_create(
                destination=destination,
                name=destination.name,
                defaults={
                    'city': destination.city or destination.country,
                    'description': description,
                    'source_url': f'https://en.wikipedia.org/wiki/{matched_name.replace(" ", "_")}',
                },
            )
            created += 1
            self.stdout.write(f'  + {destination.name}')
            time.sleep(1)  # be a polite scraper

        self.stdout.write(self.style.SUCCESS(f'Updated attraction info for {created} destinations.'))
