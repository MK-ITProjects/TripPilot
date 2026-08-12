from django.contrib import admin

from .models import ScrapedAttraction, ScrapedEvent, ScrapedHotelPrice, ScrapedNews, WeatherData


@admin.register(ScrapedNews)
class ScrapedNewsAdmin(admin.ModelAdmin):
    list_display = ('title', 'source', 'published_at', 'scraped_at')
    search_fields = ('title', 'source')


@admin.register(WeatherData)
class WeatherDataAdmin(admin.ModelAdmin):
    list_display = ('city', 'temperature_c', 'condition', 'fetched_at')
    search_fields = ('city',)


@admin.register(ScrapedAttraction)
class ScrapedAttractionAdmin(admin.ModelAdmin):
    list_display = ('name', 'city', 'destination', 'scraped_at')
    search_fields = ('name', 'city')


@admin.register(ScrapedHotelPrice)
class ScrapedHotelPriceAdmin(admin.ModelAdmin):
    list_display = ('hotel_name', 'city', 'price_per_night', 'rating')
    search_fields = ('hotel_name', 'city')


@admin.register(ScrapedEvent)
class ScrapedEventAdmin(admin.ModelAdmin):
    list_display = ('name', 'city', 'event_date')
    search_fields = ('name', 'city')
