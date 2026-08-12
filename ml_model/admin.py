from django.contrib import admin

from .models import CrowdPrediction


@admin.register(CrowdPrediction)
class CrowdPredictionAdmin(admin.ModelAdmin):
    list_display = ('destination', 'month', 'predicted_level', 'popularity_score', 'estimated_cost', 'created_at')
    list_filter = ('predicted_level', 'month')
