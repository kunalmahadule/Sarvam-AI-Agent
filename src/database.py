import json
import os

DATA_PATH = os.path.join("data", "restaurants.json")

def load_restaurants():
    with open(DATA_PATH, "r") as file:
        return json.load(file)

# ✅ Global reservation list to track user bookings
reservations = []

def find_restaurants(city=None, cuisine=None, seats_required=None):
    restaurants = load_restaurants()
    results = []

    for r in restaurants:
        if city and r["city"].lower() != city.lower():
            continue
        if cuisine and r["cuisine"].lower() != cuisine.lower():
            continue
        if seats_required and r["capacity"] < seats_required:
            continue
        results.append(r)

    return results
