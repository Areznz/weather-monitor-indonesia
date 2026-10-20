
import requests
import streamlit as st
import time

OPEN_METEO_GEO = "https://geocoding-api.open-meteo.com/v1/search"
NOMINATIM_URL = "https://nominatim.openstreetmap.org/search"
WEATHER_URL = "https://api.open-meteo.com/v1/forecast"


def clean_region_name(name):
    prefixes = [
        "KABUPATEN ADMINISTRASI ",
        "KABUPATEN ",
        "KOTA ADMINISTRASI ",
        "KOTA ",
    ]

    result = name.strip()

    for prefix in prefixes:
        if result.upper().startswith(prefix):
            return result[len(prefix):].strip()

    return result


@st.cache_data(ttl=86400)
def get_coordinates(regency_name, province_name):
    clean_name = clean_region_name(regency_name)

    queries = list(dict.fromkeys([
        clean_name,
        regency_name.strip(),
    ]))

    province = province_name.casefold().strip()

    province_aliases = {
        "dki jakarta": [
            "jakarta",
            "jakarta special capital region",
        ],
        "di yogyakarta": [
            "yogyakarta",
            "special region of yogyakarta",
        ],
    }

    valid_province_names = province_aliases.get(
        province,
        [province],
    )

    # 1. Cari koordinat melalui Open-Meteo
    for query in queries:
        try:
            response = requests.get(
                OPEN_METEO_GEO,
                params={
                    "name": query,
                    "count": 100,
                    "language": "en",
                    "format": "json",
                    "countryCode": "ID",
                },
                timeout=15,
            )
            response.raise_for_status()

            results = response.json().get("results") or []

            candidates = [
                item for item in results
                if item.get("country_code", "").casefold() == "id"
                and item.get("latitude") is not None
                and item.get("longitude") is not None
            ]

            for item in candidates:
                admin1 = item.get("admin1", "").casefold().strip()

                if any(
                    name in admin1 or admin1 in name
                    for name in valid_province_names
                ):
                    return {
                        "latitude": item["latitude"],
                        "longitude": item["longitude"],
                        "name": item.get("name", clean_name),
                    }

        except (
            requests.RequestException,
            ValueError,
            TypeError,
        ) as e:
            print(f"[Open-Meteo] {query}: {e}")

    # 2. Fallback ke OpenStreetMap
    osm_queries = [
        f"{clean_name}, {province_name}, Indonesia",
        f"{regency_name}, {province_name}, Indonesia",
    ]

    for query in osm_queries:
        try:
            response = requests.get(
                NOMINATIM_URL,
                params={
                    "q": query,
                    "format": "jsonv2",
                    "limit": 5,
                    "countrycodes": "id",
                    "addressdetails": 1,
                },
                headers={
                    "User-Agent": "WeatherMonitorIndonesia/1.0"
                },
                timeout=20,
            )
            response.raise_for_status()

            for item in response.json():
                address = item.get("address", {})

                if address.get("country_code", "").casefold() != "id":
                    continue

                return {
                    "latitude": float(item["lat"]),
                    "longitude": float(item["lon"]),
                    "name": item.get("display_name", regency_name),
                }

        except (
            requests.RequestException,
            ValueError,
            KeyError,
            TypeError,
        ) as e:
            print(f"[Nominatim] {query}: {e}")

        time.sleep(1)

    print(
        f"[Geocoding gagal] {regency_name}, {province_name}"
    )
    return None


@st.cache_data(ttl=60)
def get_weather(latitude, longitude):
    try:
        response = requests.get(
            WEATHER_URL,
            params={
                "latitude": latitude,
                "longitude": longitude,
                "current": [
                    "temperature_2m",
                    "relative_humidity_2m",
                    "apparent_temperature",
                    "precipitation",
                    "weather_code",
                    "wind_speed_10m",
                    "wind_direction_10m",
                ],
                "timezone": "auto",
            },
            timeout=20,
        )

        response.raise_for_status()
        data = response.json()

        if "current" not in data:
            st.error("Respons API tidak memiliki data cuaca saat ini.")
            return None

        return data

    except requests.RequestException as e:
        st.error(f"Gagal mengambil data cuaca: {e}")
        return None
```
