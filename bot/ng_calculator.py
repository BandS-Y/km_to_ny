import os
import json
import math
from datetime import datetime, timedelta, timezone
from resources.ttn_cities_data import CITIES
from resources.ttn_translate import TRANSLATE

# Абсолютный путь для user_cities.json
USER_CITY_FILE = os.path.abspath(os.path.join(
    os.path.dirname(__file__), '../resources/user_cities.json'
))

def get_city_by_name(city_name):
    city_name = city_name.lower().strip()
    for city in CITIES:
        if city["name"].lower() == city_name or city.get("alt_name", "").lower() == city_name:
            return city
    return None

def get_user_city(user_id):
    if not os.path.exists(USER_CITY_FILE):
        return None
    with open(USER_CITY_FILE, "r", encoding="utf-8") as f:
        user_cities = json.load(f)
    return user_cities.get(str(user_id), None)

def save_user_city(user_id, name, latitude, tz_shift):
    if os.path.exists(USER_CITY_FILE):
        with open(USER_CITY_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
    else:
        data = {}
    data[str(user_id)] = {
        "name": name,
        "latitude": latitude,
        "tz_shift": tz_shift
    }
    with open(USER_CITY_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def get_city_info(user_id, city_arg=None):
    if city_arg:
        city = get_city_by_name(city_arg)
        if city:
            return city
    user_city = get_user_city(user_id)
    if user_city:
        return user_city
    return None

def get_city_localtime(city):
    utc_now = datetime.now(timezone.utc)
    tz_shift = city["tz_shift"]
    return utc_now + timedelta(hours=tz_shift)

def distance_to_new_year(now):
    new_year = now.replace(year=now.year + 1, month=1, day=1, hour=0, minute=0, second=0, microsecond=0)
    delta = new_year - now
    return delta.total_seconds()

def earth_orbit_distance(seconds):
    EARTH_ORBITAL_SPEED = 29.78  # км/с
    return EARTH_ORBITAL_SPEED * seconds

def rotation_speed_by_lat(lat):
    EARTH_ROTATION_SPEED_EQ = 465.1  # м/с
    return EARTH_ROTATION_SPEED_EQ * math.cos(math.radians(lat))

def earth_rotation_distance(lat, seconds):
    return rotation_speed_by_lat(lat) * seconds / 1000

def number_fmt(n):
    return "{:,}".format(int(round(n))).replace(",", " ")

def format_result(city, now, lang='ru'):
    seconds_left = distance_to_new_year(now)
    orbit_km = earth_orbit_distance(seconds_left)
    surface_km = earth_rotation_distance(city["latitude"], seconds_left)
    total_km = orbit_km + surface_km
    return (
        f'{TRANSLATE[lang]["city"]}: {city["name"]}\n'
        f'{TRANSLATE[lang]["current_time"]}: {now.strftime("%Y-%m-%d %H:%M:%S")}\n'
        f'{TRANSLATE[lang]["new_year_left"]}: {str(timedelta(seconds=int(seconds_left)))}\n'
        f'{TRANSLATE[lang]["latitude"]}: {city["latitude"]}\n'
        f'{TRANSLATE[lang]["orbit_distance"]}: {number_fmt(orbit_km)} км\n'
        f'{TRANSLATE[lang]["rotation_distance"]}: {number_fmt(surface_km)} км\n'
        f'{TRANSLATE[lang]["total_left"]}: {number_fmt(total_km)} км'
    )
