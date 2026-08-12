# TripPilot Clone — Django + ML + Web Scraping (College Project)

A travel-planning web app inspired by trippilot.com, rebuilt with Python/Django,
Bootstrap, web scraping (BeautifulSoup/Requests) and machine learning (scikit-learn).

## 1. Prerequisites

- Python 3.11+ installed and on PATH (`python --version`)
- pip

## 2. Setup

```bash
cd d:\trippilot

# create and activate a virtual environment
python -m venv venv
venv\Scripts\activate        # Windows
# source venv/bin/activate   # macOS/Linux

# install dependencies
pip install -r requirements.txt

# create the database tables
python manage.py makemigrations
python manage.py migrate

# create an admin account
python manage.py createsuperuser

# load ~12 sample Indian destinations so the site isn't empty
python manage.py loaddata destinations/fixtures/sample_destinations.json

# train the ML models (crowd classifier, cost regressor, cluster model)
python manage.py train_models

# scrape live data (news, attraction summaries, weather, hotels/events)
python manage.py run_all_scrapers

# run the dev server
python manage.py runserver
```

Visit http://127.0.0.1:8000/ and http://127.0.0.1:8000/admin/ (admin panel).

## 3. Keeping scraped data fresh

`run_all_scrapers` should be re-run periodically so news/weather stay current.
Schedule it with **Windows Task Scheduler** (Action: start a program,
`venv\Scripts\python.exe`, arguments `manage.py run_all_scrapers`, working
directory the project root) or a cron job on Linux/macOS, e.g. every 6 hours:

```
0 */6 * * * cd /path/to/trippilot && venv/bin/python manage.py run_all_scrapers
```

You can also run the individual commands separately:
`scrape_news`, `scrape_attractions`, `scrape_weather`, `scrape_hotels_events`.

## 4. Pages

| Page | URL |
|---|---|
| Home | `/` |
| Explore Destinations | `/destinations/` |
| Destination Detail | `/destinations/<slug>/` |
| AI Trip Planner | `/planner/ai-trip-planner/` |
| Budget Calculator | `/planner/budget-calculator/` |
| Crowd Prediction (ML) | `/predictions/crowd/` |
| Travel News (scraped) | `/news/` |
| Weather & Travel Alerts | `/news/weather/` |
| Chatbot Assistant | `/chatbot/` |
| About Project | `/about/` |
| Contact | `/contact/` |
| Login / Signup | `/accounts/login/`, `/accounts/signup/` |
| User Dashboard | `/dashboard/` |

## 5. Project structure

```
config/            Django settings, root urls
users/             Auth, profile, favorites
destinations/      Destination + Review models, explore/detail pages
planner/           AI trip itinerary builder + budget calculator
scraper/           BeautifulSoup/Requests scrapers + management commands
ml_model/          Synthetic dataset + Decision Tree / Random Forest /
                   Linear Regression / K-Means training scripts + predict.py
chatbot/           Rule-based/retrieval chatbot over stored destination data
dashboard/         Logged-in user's saved trips & favorites
templates/         All HTML templates (Bootstrap 5)
static/            CSS/JS
```

## 6. Notes on the ML & scraping approach (for your project report)

- **ML models** are trained on a *synthetic* dataset generated from each
  destination's stored cost/visitor-count fields combined with hand-tuned
  seasonality rules (`ml_model/ml/dataset.py`). This is a common, defensible
  approach for a college project since months of real booking/footfall logs
  aren't available — swap `generate_crowd_and_cost_dataset()` for real
  historical data later without touching the training scripts.
- **Web scraping** targets Wikipedia (news + attraction summaries) because it
  explicitly permits automated reading, unlike most commercial travel/booking
  sites whose Terms of Service forbid scraping. Weather comes from the free
  Open-Meteo API. Hotel prices/events are simulated sample generators — swap
  in a real Requests/BeautifulSoup/Selenium scraper against a site you have
  permission to scrape if your instructor wants a second live source.
