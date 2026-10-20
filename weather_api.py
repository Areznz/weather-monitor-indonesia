
import requests
import streamlit as st
import time

OPEN_METEO_GEO = (
    "https://geocoding-api.open-meteo.com/v1/search"
)
NOMINATIM_URL = "https://nominatim.openstreetmap.org/search"
WEATHER_URL = "https://api.open-meteo.com/v1/forecast"


def clean_region_name(name):
    prefixes = [
        "KABUPATEN ADMINISTRASI ",
        "KABUPATEN ",
        "KOTA ADMINISTRASI ",
        "KOTA "
    ]

    result = name.strip()

    for prefix in prefixes:
        if result.upper().startswith(prefix):
            return result[len(prefix):].strip()

    return result


@st.cache_data(ttl=86400)
def get_coordinates(regency_name, province_name):
    clean_name = clean_region_name(regency_name)

    # 1. Cari melalui Open-Meteo
    queries = [
        f"{clean_name}, {province_name}",
        f"{regency_name}, {province_name}",
        clean_name,
    ]

    for index, query in enumerate(queries):
        try:
            response = requests.get(
                OPEN_METEO_GEO,
                params={
                    "name": query,
                    "count": 10,
                    "language": "id",
                    "format": "json",
                    "countryCode": "ID",
                },
                timeout=15,
            )
            response.raise_for_status()

            results = response.json().get("results") or []

            # Hanya ambil hasil dari Indonesia
            candidates = [
                item for item in results
                if item.get("country_code", "").casefold() == "id"
                and "latitude" in item
                and "longitude" in item
            ]

            if not candidates:
                continue

            province = province_name.casefold().strip()

            # Utamakan kecocokan nama provinsi
            for item in candidates:
                admin1 = item.get("admin1", "").casefold().strip()

                if province in admin1 or admin1 in province:
                    return {
                        "latitude": item["latitude"],
                        "longitude": item["longitude"],
                        "name": item.get("name", clean_name),
                    }

            # Pencarian pertama sudah menyertakan nama provinsi
            # sehingga bisa menjadi fallback jika admin1 berbeda format.
            if index == 0:
                item = candidates[0]
                return {
                    "latitude": item["latitude"],
                    "longitude": item["longitude"],
                    "name": item.get("name", clean_name),
                }

        except (requests.RequestException, ValueError, TypeError) as e:
            print(f"[Open-Meteo] {query}: {e}")

    # 2. Fallback melalui OpenStreetMap Nominatim
    osm_queries = [
        f"{regency_name}, {province_name}, Indonesia",
        f"{clean_name}, {province_name}, Indonesia",
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

            results = response.json()

            for item in results:
                address = item.get("address", {})
                country = address.get("country_code", "").casefold()

                if country != "id":
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
        f"[Geocoding gagal] "
        f"Kabupaten/kota: {regency_name}, "
        f"Provinsi: {province_name}"
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
                    "wind_direction_10m"
                ],
                "timezone": "auto"
            },
            timeout=20
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

if __name__ == "__main__":
    import requests

    try:
        r = requests.get(
            "https://geocoding-api.open-meteo.com/v1/search",
            params={
                "name": "Jakarta",
                "count": 5,
                "language": "id",
                "format": "json",
                "countryCode": "ID",
            },
            timeout=15,
        )

        print("STATUS:", r.status_code)
        print("HASIL:", r.text[:1500])

    except Exception as e:
        print("ERROR:", repr(e))
