"""
Live travel alerts, derived from data this project already collects (real
Open-Meteo weather readings + real scraped travel news) rather than a
simulated alerts feed -- there's no free legitimate API for road
closures/floods, so this surfaces genuine risk signals from data we already
have instead of inventing fake ones.
"""
import re

from .models import ScrapedNews, WeatherData

# (severity, message) per Open-Meteo condition string -- see scraping.fetch_weather.
WEATHER_CONDITION_ALERTS = {
    'Thunderstorm': ('high', 'Thunderstorm expected -- outdoor plans may be disrupted.'),
    'Heavy rain': ('high', 'Heavy rain expected -- possible waterlogging and travel delays.'),
    'Rain showers': ('medium', 'Rain showers expected -- carry rain gear.'),
    'Moderate rain': ('medium', 'Moderate rain expected -- carry rain gear.'),
    'Slight rain': ('low', 'Light rain expected.'),
    'Light drizzle': ('low', 'Light drizzle expected.'),
    'Slight snow': ('medium', 'Snowfall expected -- check road/pass conditions before traveling.'),
    'Fog': ('medium', 'Low visibility due to fog -- possible flight/road delays.'),
}

NEWS_RISK_KEYWORDS = [
    'flood', 'landslide', 'cyclone', 'storm', 'earthquake', 'wildfire',
    'evacuat', 'road closed', 'road closure', 'closed indefinitely',
    'protest', 'strike', 'curfew', 'disruption', 'warning', 'alert',
]


def _weather_alert(weather):
    if not weather:
        return None
    alert = WEATHER_CONDITION_ALERTS.get(weather.condition)
    if alert:
        severity, message = alert
        return {'severity': severity, 'category': 'weather', 'message': message, 'source': 'Open-Meteo'}
    if weather.wind_speed_kmh and weather.wind_speed_kmh >= 40:
        return {'severity': 'medium', 'category': 'weather', 'message': f'High winds ({weather.wind_speed_kmh} km/h) reported.', 'source': 'Open-Meteo'}
    if weather.temperature_c is not None and (weather.temperature_c >= 42 or weather.temperature_c <= 2):
        return {'severity': 'medium', 'category': 'weather', 'message': f'Extreme temperature ({weather.temperature_c}°C) reported.', 'source': 'Open-Meteo'}
    return None


def _news_alerts_for_city(city, country=None, limit=3):
    if not city:
        return []
    pattern = re.compile('|'.join(re.escape(k) for k in NEWS_RISK_KEYWORDS), re.IGNORECASE)
    place_pattern = re.compile(re.escape(city) + (f'|{re.escape(country)}' if country else ''), re.IGNORECASE)

    alerts = []
    for item in ScrapedNews.objects.all()[:100]:
        text = f'{item.title} {item.summary}'
        if pattern.search(text) and place_pattern.search(text):
            alerts.append({
                'severity': 'medium', 'category': 'news',
                'message': item.title, 'source': item.source or 'Travel News', 'url': item.url,
            })
            if len(alerts) >= limit:
                break
    return alerts


def get_travel_alerts(city, country=None):
    """Return a list of {severity, category, message, source} alert dicts for a city,
    derived from real weather readings and real scraped news -- empty list if none apply."""
    alerts = []
    weather = WeatherData.objects.filter(city__iexact=city).first() if city else None
    weather_alert = _weather_alert(weather)
    if weather_alert:
        alerts.append(weather_alert)
    alerts.extend(_news_alerts_for_city(city, country))
    return alerts
