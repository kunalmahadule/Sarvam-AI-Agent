import uuid
from src.database import load_restaurants, reservations

def find_restaurants(city, cuisine=None, seats_required=1):
    restaurants = load_restaurants()
    matched = []

    for res in restaurants:
        if res["city"].lower() == city.lower():
            if cuisine and cuisine.lower() not in res["cuisine"].lower():
                continue
            if res["capacity"] >= seats_required:
                matched.append(res)

    return matched

def make_reservation(restaurant_name, user_name, time):
    reservation_id = str(uuid.uuid4())
    reservation = {
        "reservation_id": reservation_id,
        "restaurant_name": restaurant_name,
        "user_name": user_name,
        "time": time
    }
    reservations.append(reservation)
    return {
        "message": "Reservation successful.",
        "reservation_id": reservation_id
    }

def cancel_reservation(reservation_id):
    for res in reservations:
        if res["reservation_id"] == reservation_id:
            reservations.remove(res)
            return {"message": "Reservation cancelled successfully."}
    return {"message": "Reservation ID not found."}
