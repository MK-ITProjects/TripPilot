from django.core.management.base import BaseCommand

from scraper.models import ScrapedNews
from scraper.scraping import scrape_travel_news


class Command(BaseCommand):
    help = 'Scrape latest news headlines (Wikipedia "In the news") into ScrapedNews.'

    def handle(self, *args, **options):
        items = scrape_travel_news(limit=10)
        created = 0
        for item in items:
            _, was_created = ScrapedNews.objects.get_or_create(
                url=item['url'],
                defaults={
                    'title': item['title'],
                    'summary': item['summary'],
                    'source': item['source'],
                    'published_at': item['published_at'],
                },
            )
            created += int(was_created)
        self.stdout.write(self.style.SUCCESS(f'Scraped {len(items)} items, {created} new.'))
