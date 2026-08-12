from django.contrib import admin

from .models import Destination, Review


@admin.register(Destination)
class DestinationAdmin(admin.ModelAdmin):
    list_display = ('name', 'country', 'category', 'average_cost_per_day', 'previous_visitor_count', 'is_featured')
    list_filter = ('category', 'is_featured', 'country')
    search_fields = ('name', 'country', 'city', 'tags')
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('destination', 'user', 'rating', 'created_at')
    list_filter = ('rating',)
