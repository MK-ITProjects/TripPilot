from datetime import timedelta

from django.core.mail import send_mail
from django.core.management.base import BaseCommand
from django.utils import timezone

from planner.models import TripPlan
from scraper.alerts import get_travel_alerts

REMINDER_DAYS_BEFORE = 3


class Command(BaseCommand):
    help = (
        'Email a reminder to users whose trip starts in '
        f'{REMINDER_DAYS_BEFORE} days (schedule this via cron / Windows Task Scheduler, '
        'e.g. once a day).'
    )

    def handle(self, *args, **options):
        target_date = timezone.now().date() + timedelta(days=REMINDER_DAYS_BEFORE)
        trips = TripPlan.objects.filter(start_date=target_date, reminder_sent=False)

        sent = 0
        for trip in trips:
            if not trip.user.email:
                continue

            alerts = get_travel_alerts(trip.destination.city or trip.destination.name, trip.destination.country)
            alert_lines = '\n'.join(f'- {a["message"]}' for a in alerts) or 'No active alerts right now.'

            message = (
                f"Hi {trip.user.first_name or trip.user.username},\n\n"
                f"Your trip to {trip.destination.name} starts in {REMINDER_DAYS_BEFORE} days "
                f"({trip.start_date:%d %b %Y}). Here's a quick reminder:\n\n"
                f"Destination: {trip.destination.name}, {trip.destination.country}\n"
                f"Dates: {trip.start_date:%d %b %Y} - {trip.end_date:%d %b %Y}\n"
                f"Travelers: {trip.travelers}\n"
                f"Estimated budget: ₹{trip.estimated_cost}\n\n"
                f"Current travel alerts for {trip.destination.name}:\n{alert_lines}\n\n"
                "Safe travels!\nTripPilot"
            )

            try:
                send_mail(
                    subject=f'Your trip to {trip.destination.name} is coming up!',
                    message=message,
                    from_email=None,
                    recipient_list=[trip.user.email],
                )
                trip.reminder_sent = True
                trip.save(update_fields=['reminder_sent'])
                sent += 1
            except Exception as exc:
                self.stderr.write(self.style.WARNING(f'Failed to email {trip.user.email}: {exc}'))

        self.stdout.write(self.style.SUCCESS(f'Sent {sent} of {trips.count()} pending trip reminders.'))
