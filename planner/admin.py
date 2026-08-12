from django.contrib import admin

from .models import TripPlan, TripStop


class TripStopInline(admin.TabularInline):
    model = TripStop
    extra = 0


@admin.register(TripPlan)
class TripPlanAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'destination', 'origin_city', 'start_date', 'end_date', 'travelers', 'trip_style', 'estimated_cost')
    list_filter = ('trip_style',)
    search_fields = ('title', 'user__username', 'destination__name')
    inlines = [TripStopInline]
