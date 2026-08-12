from django.core.management import call_command
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Run every scraper in sequence (news, attractions, weather, hotels/events). Schedule this with cron / Windows Task Scheduler.'

    def handle(self, *args, **options):
        call_command('scrape_news')
        call_command('scrape_attractions')
        call_command('scrape_weather')
        call_command('scrape_hotels_events')
        self.stdout.write(self.style.SUCCESS('All scrapers finished.'))
