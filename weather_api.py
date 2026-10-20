import requests
import streamlit as st
import time

OPEN_METEO_GEO = "https://geocoding-api.open-meteo.com/v1/search"
NOMINATIM_URL = "https://nominatim.openstreetmap.org/search"
WEATHER_URL = "https://api.open-meteo.com/v1/forecast"


# Nama provinsi Indonesia dan variasi nama dari API
PROVINCE_ALIASES = {
    "aceh": ["aceh"],
    "sumatera utara": ["north sumatra", "sumatera utara"],
    "sumatera barat": ["west sumatra", "sumatera barat"],
    "riau": ["riau"],
    "kepulauan riau": ["riau islands", "kepulauan riau"],
    "jambi": ["jambi"],
    "sumatera selatan": ["south sumatra", "sumatera selatan"],
    "kepulauan bangka belitung": [
        "bangka belitung islands",
        "kepulauan bangka belitung",
    ],
    "bengkulu": ["bengkulu"],
    "lampung": ["lampung"],
    "dki jakarta": ["jakarta", "jakarta special capital region"],
    "jakarta": ["jakarta", "jakarta special capital region"],
    "jawa barat": ["west java", "jawa barat"],
    "jawa tengah": ["central java", "jawa tengah"],
    "di yogyakarta": [
        "yogyakarta",
        "special region of yogyakarta",
    ],
    "diy": ["yogyakarta", "special region of yogyakarta"],
    "jawa timur": ["east java", "jawa timur"],
    "banten": ["banten"],
    "bali": ["bali"],
    "nusa tenggara barat": ["west nusa tenggara"],
    "nusa tenggara timur": ["east nusa tenggara"],
    "kalimantan barat": ["west kalimantan"],
    "kalimantan tengah": ["central kalimantan"],
    "kalimantan selatan": ["south kalimantan"],
    "kalimantan timur": ["east kalimantan"],
    "kalimantan utara": ["north kalimantan"],
    "sulawesi utara": ["north sulawesi"],
    "gorontalo": ["gorontalo"],
    "sulawesi tengah": ["central sulawesi"],
    "sulawesi barat": ["west sulawesi"],
    "sulawesi selatan": ["south sulawesi"],
    "sulawesi tenggara": ["southeast sulawesi"],
    "maluku": ["maluku"],
    "maluku utara": ["north maluku"],
    "papua": ["papua"],
    "papua barat": ["west papua"],
    "papua selatan": ["south papua"],
    "papua tengah": ["central papua"],
    "papua pegunungan": ["highland papua"],
    "papua barat daya": ["southwest papua"],
}


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


def province_matches(api_province, requested_province):
    api_name = (api_province or "").casefold().strip()
    requested = requested_province.casefold().strip()

    aliases = PROVINCE_ALIASES.get(requested, [requested])
    aliases = [name.casefold().strip() for name in aliases]

    return any(
        alias == api_name
        or alias in api_name
        or api_name in alias
        for alias in aliases
        if alias
    )


@st.cache_data(ttl=86400)
def get_coordinates(regency_name, province_name):
    clean_name = clean_region_name(regency_name)

    queries = list(dict.fromkeys([
        f"{clean_name}, {province_name}",
        clean_name,
        regency_name.strip(),
    ]))

    # 1. Cari melalui Open-Meteo
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

            for item in results:
                if item.get("country_code", "").casefold() != "id":
                    continue

                latitude = item.get("latitude")
                longitude = item.get("longitude")

                if latitude is None or longitude is None:
                    continue

                admin1 = item.get("admin1", "")

                if province_matches(admin1, province_name):
                    return {
                        "latitude": latitude,
                        "longitude": longitude,
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
                    "limit": 10,
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

                # Pastikan hasil sesuai provinsi yang diminta
                

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
