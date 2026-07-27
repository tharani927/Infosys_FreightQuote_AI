"""
weather_context.py for FreightQuote AI
Simulates Indian marine ports and global trade route weather conditions.
"""
import random

GLOBAL_PORTS_WEATHER = {
    "Mumbai JNPT (IN)": {"status": "Monsoon Rain & High Winds", "temp_c": 28, "wind_kt": 32, "delay_penalty_multiplier": 1.15},
    "Mundra Port (IN)": {"status": "Clear / Dusty Gusts", "temp_c": 34, "wind_kt": 18, "delay_penalty_multiplier": 1.05},
    "Chennai Port (IN)": {"status": "Tropical Cyclone Watch", "temp_c": 31, "wind_kt": 36, "delay_penalty_multiplier": 1.20},
    "Cochin Port (IN)": {"status": "Monsoon Squalls", "temp_c": 27, "wind_kt": 24, "delay_penalty_multiplier": 1.10},
    "Kolkata Haldia (IN)": {"status": "Heavy River Fog & Tidal Delay", "temp_c": 26, "wind_kt": 14, "delay_penalty_multiplier": 1.12},
    "Shanghai (CN)": {"status": "High Winds & Typhoon Watch", "temp_c": 22, "wind_kt": 38, "delay_penalty_multiplier": 1.18},
    "Rotterdam (NL)": {"status": "Clear / Moderate Gale", "temp_c": 14, "wind_kt": 22, "delay_penalty_multiplier": 1.05},
    "Singapore (SG)": {"status": "Monsoon Rain Squalls", "temp_c": 29, "wind_kt": 26, "delay_penalty_multiplier": 1.08},
    "Suez Canal Hub": {"status": "Sandstorm & High Transit Queue", "temp_c": 35, "wind_kt": 30, "delay_penalty_multiplier": 1.25},
    "Panama Canal Hub": {"status": "Drought Water Level Restrictions", "temp_c": 31, "wind_kt": 15, "delay_penalty_multiplier": 1.30},
    "Dubai (AE)": {"status": "Clear / High Heat", "temp_c": 38, "wind_kt": 14, "delay_penalty_multiplier": 1.02},
    "Hamburg (DE)": {"status": "Heavy Fog & Berth Queue", "temp_c": 11, "wind_kt": 18, "delay_penalty_multiplier": 1.12}
}

def get_weather_report(port_name):
    for k, v in GLOBAL_PORTS_WEATHER.items():
        if k.lower() in port_name.lower() or port_name.lower() in k.lower():
            return {"port": k, **v}
    return {"port": port_name, "status": "Normal Marine Conditions", "temp_c": 25, "wind_kt": 15, "delay_penalty_multiplier": 1.00}

def get_route_weather_multiplier(origin, dest):
    w1 = get_weather_report(origin)
    w2 = get_weather_report(dest)
    return round((w1["delay_penalty_multiplier"] + w2["delay_penalty_multiplier"]) / 2, 3)

def get_city_weather(city_name):
    return {"city": city_name, "status": "Fair Weather Conditions", "temp_c": 30, "demand_impact_pct": 0.0, "supply_delay_days": 0, "attrition_stress": "Normal"}
