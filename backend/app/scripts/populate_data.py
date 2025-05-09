import requests

BASE_URL = "http://localhost:8000"

# English city/country names only
countries_with_cities = {
    "France": ["Paris", "Nice", "Lyon"],
    "Germany": ["Berlin", "Munich", "Hamburg"],
    "Italy": ["Rome", "Venice", "Milan"],
    "Spain": ["Madrid", "Barcelona", "Valencia"],
    "Netherlands": ["Amsterdam", "Rotterdam", "Utrecht"],
    "Greece": ["Athens", "Santorini", "Thessaloniki"],
    "Austria": ["Vienna", "Salzburg", "Innsbruck"],
    "Switzerland": ["Zurich", "Geneva", "Lucerne"],
    "Portugal": ["Lisbon", "Porto", "Faro"],
    "Czech Republic": ["Prague", "Brno", "Cesky Krumlov"]
}

def create_country(name):
    response = requests.post(f"{BASE_URL}/countries", json={"name": name})
    if response.status_code == 201:
        print(f"✅ Country created: {name}")
        return response.json()["id"]
    elif response.status_code == 400:
        print(f"⚠️ Country already exists: {name}")
        all_countries = requests.get(f"{BASE_URL}/countries").json()
        return next((c["id"] for c in all_countries if c["name"].lower() == name.lower()), None)
    else:
        print(f"❌ Error creating country: {name} — {response.text}")
        return None

def create_city(name, country_id):
    response = requests.post(f"{BASE_URL}/cities", json={"name": name, "country_id": country_id})
    if response.status_code == 201:
        print(f"   🏙️ City created: {name}")
    elif response.status_code == 400:
        print(f"   ⚠️ City already exists: {name}")
    else:
        print(f"   ❌ Error creating city: {name} — {response.text}")

def populate():
    for country, cities in countries_with_cities.items():
        country_id = create_country(country)
        if not country_id:
            continue
        for city in cities:
            create_city(city, country_id)

if __name__ == "__main__":
    populate()
