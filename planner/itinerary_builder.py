"""
Rule-based itinerary generator ("AI Trip Planner").

It is intentionally simple (no external LLM call) so the whole pipeline can
run offline for a college demo: it combines destination metadata with any
scraped attraction data to produce a day-by-day plan.
"""

import random

CATEGORY_ACTIVITY_POOL = {
    'beach': [
        'Relax at the main beach and try water sports',
        'Sunset boat cruise along the coastline',
        'Visit a local seafood market and beachside shacks',
        'Snorkeling / scuba diving excursion',
        'Explore nearby lighthouse or coastal viewpoint',
        'Kayaking or stand-up paddleboarding session',
        'Visit a nearby fishing village and local harbor',
        'Beachside yoga or morning swim',
        'Island-hopping day trip by boat',
        'Evening bonfire and live music by the shore',
    ],
    'adventure': [
        'Guided trekking / hiking trail',
        'White-water rafting or ziplining session',
        'Rock climbing or rappelling with a local operator',
        'Camping and bonfire evening',
        'Paragliding or bungee jumping (weather permitting)',
        'Mountain biking on forest trails',
        'Cave exploration with a local guide',
        'ATV / off-roading excursion',
        'River crossing and canyoning session',
        'Night trek to a nearby viewpoint',
    ],
    'cultural': [
        'Guided heritage walk through the old city',
        'Visit the main temple/monument/museum',
        'Traditional cooking class with a local family',
        'Evening cultural show or folk performance',
        'Explore local handicraft and textile markets',
        'Visit a local art gallery or artisan workshop',
        'Historic fort or palace guided tour',
        'Traditional dance or music workshop',
        'Explore a local heritage neighborhood on foot',
        'Visit a nearby archaeological site',
    ],
    'hill': [
        'Sunrise viewpoint trek',
        'Visit local tea/coffee/spice plantation',
        'Nature walk through pine or cedar forests',
        'Cable car or ropeway ride',
        'Bonfire and stargazing night',
        'Visit a nearby waterfall',
        'Local village walk and homestay lunch',
        'Paragliding over the valley (weather permitting)',
        'Visit a botanical garden or nature park',
        'Short trek to a nearby monastery or fort',
    ],
    'wildlife': [
        'Morning jeep safari in the national park',
        'Guided nature trail with a naturalist',
        'Bird watching at the nearby lake/wetland',
        'Visit the interpretation centre / conservation park',
        'Evening safari and photography session',
        'Guided canopy walk through the forest reserve',
        'Visit a rescue/rehabilitation centre',
        'Nighttime nature walk with a ranger',
        'Boat safari along the river/wetland',
        'Nature photography workshop',
    ],
    'city': [
        'City sightseeing tour of key landmarks',
        'Visit a rooftop cafe or observation deck',
        'Shopping at the main market district',
        'Museum / art gallery visit',
        'Food-walk through the old town lanes',
        'Evening riverside or waterfront stroll',
        'Visit a local flea market or bazaar',
        'Guided street-art or local neighborhood tour',
        'Visit a planetarium or science centre',
        'Live music or theatre show in the evening',
    ],
    'pilgrimage': [
        'Morning darshan / prayers at the main shrine',
        'Visit nearby smaller temples and ghats',
        'Attend the evening aarti ceremony',
        'Explore the local prasad and handicraft market',
        'Guided heritage tour of the temple complex',
        'Visit a nearby holy river or bathing ghat',
        'Attend a satsang or spiritual discourse',
        "Explore the pilgrim town's old bazaar",
        'Visit a local ashram or meditation centre',
        'Sunrise/sunset prayer at the riverside',
    ],
}

DEFAULT_ACTIVITIES = [
    'Explore the main attractions of the area',
    'Try the local cuisine at a recommended restaurant',
    'Free time / leisure & shopping',
    'Guided sightseeing tour',
    'Relax and enjoy the local culture',
    'Visit a nearby local market',
    'Take a scenic walk around the town',
    'Visit a recommended viewpoint or landmark',
]

MEAL_SLOTS = ['Breakfast at hotel', 'Local lunch spot', 'Dinner with regional specialities']


def build_itinerary(destination, num_days, attractions=None):
    """Return a list of {day, title, activities, meals} dicts."""
    pool = CATEGORY_ACTIVITY_POOL.get(destination.category, DEFAULT_ACTIVITIES)
    attraction_names = [a.name for a in attractions] if attractions else []

    rng = random.Random(destination.id or 0)

    # Middle days (everything except arrival/departure) each need 3
    # activities. Instead of reshuffling the same small pool fresh for every
    # day -- which repeats activities almost immediately for longer trips --
    # build one long queue up front: shuffle the pool, and if more slots are
    # still needed, shuffle again and append. This guarantees no activity
    # repeats until every other activity in the pool has already been used
    # at least once.
    middle_days = max(num_days - 2, 0) if num_days > 1 else 0
    needed = middle_days * 3
    queue = []
    while len(queue) < needed:
        batch = list(pool)
        rng.shuffle(batch)
        queue.extend(batch)
    cursor = 0

    plan = []
    for day in range(1, num_days + 1):
        if day == 1:
            title = f"Arrival in {destination.city or destination.name} & Check-in"
            activities = ['Airport/station pickup and hotel check-in', 'Leisure evening walk around the locality']
        elif day == num_days and num_days > 1:
            title = 'Departure Day'
            activities = ['Last-minute shopping / leisure', 'Check-out and departure transfer']
        else:
            activities = queue[cursor:cursor + 3]
            cursor += 3
            if attraction_names:
                pick = attraction_names[(day - 2) % len(attraction_names)]
                activities.insert(0, f"Visit {pick}")
            title = f"Day {day}: Discover {destination.name}"

        plan.append({
            'day': day,
            'title': title,
            'activities': activities,
            'meals': MEAL_SLOTS,
        })
    return plan
