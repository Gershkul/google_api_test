# google-map-test-task
**Description:**

Project contains 2 directories:

1. maptest* – standard django-project folder, created via $ django-admin startproject maptest command. It has standard structure, the corresponding changes were added to settings.py and urls.py.

- settings.py changes:

        GOOGLE_API_OPTIONS = {
            "api_key": "AIzaSyAsCTUUgf20880DF1y8B5WXLSQwi6Q79qw",
            "table_id": "1L2MC8G8_HsloPzVPtajkBsWkC_bPQdL9BjVrwDjN",
             "latLng": {"lat": -34.397, "lng": 150.644},
              "zoom": 8
        }

    where:

    "api_key" – application key
    "table_id" - Fusion table ID
    "latLng": {"lat": -34.397, "lng": 150.644},
    "zoom": 8, - center coordinates and current map zoom rate

2. maptapp – application folder. The application was created via $python python manage.py  startapp maptapp command, there were following changes added to standard django-app structure:

- apllication contains 2 routers:
urls.py  -  Home Page router, that routes the main page only
urls_api.py - REST API router for implemented functionality routing

- views.py – contains 2 classes:
HomeView, MapApiView – both classes are extensions of django.views.generic.View class and oriented by request types according to REST rules.

- HomeView – displays Home Page, connects Google.maps.api and loads styles, js-libraries, connects 
map.js (the script, that displays and manages the main page content), bootstraps data for map.js

- MapApiView – the server part of map.js functionality

- models.py – contains ORM Object (Model) Address for addresses storing to DB, has a extended constructor, that defines address by provided coordinates on model creation via google maps reverse geocode service. The address availability is this model validity indicator (is_valid).
  attributes method – is used for suitable displaying of this data in visual tables.

- fusiontable.py – the adapter for Google Fusion Tables API, was implemented by Active Record pattern,

- test.json – Google Fusion Tables API authorization info

static/js/map.js – js-functionality  for the home page content management, implemented via set of functions with jQuery

**Resources: jQuery, Twitter Bootstrap**

**Project installing:**
1. Clone project: $ git clone https://github.com/Gershkul/google_api_test.git
2. Create virtualenv: $ virtualenv -p python3 env
3. Activate virtualenv: $source env/bin/activate 
4. Setup dependencies: (env) pip install -r requirements.txt
5. DB migration: (env) python manage.py migrate
6. Run server: (env) python manage.py runserver




