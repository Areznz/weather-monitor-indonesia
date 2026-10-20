
import json
import time
from pathlib import Path

import requests

BASE_URL = "https://www.emsifa.com/api-wilayah-indonesia/v2"
OUTPUT_FILE = Path(__file__).parent / "data" / "locations.json"


def fetch_data(url):
    response = requests.get(url, timeout=30)
    response.raise_for_status()

    result = response.json()
    return result.get("data", result)


def main():
    print("Mengunduh daftar provinsi Indonesia...")

    provinces = fetch_data(f"{BASE_URL}/provinces.json")
    locations = {}
    failed = []

    for index, province in enumerate(provinces, start=1):
        province_id = province["id"]
        province_name = province["name"]

        print(
            f"[{index}/{len(provinces)}] "
            f"Mengambil {province_name}..."
        )

        locations[province_name] = {}

        try:
            regencies = fetch_data(
                f"{BASE_URL}/regencies/{province_id}.json"
            )

            for regency in regencies:
                name = regency["name"]
                latitude = regency.get("lat")
                longitude = regency.get("lng")

                if latitude is None or longitude is None:
                    failed.append(
                        f"{province_name} - {name}: koordinat kosong"
                    )
                    continue

                locations[province_name][name] = {
                    "latitude": latitude,
                    "longitude": longitude
                }

            # Jeda kecil antarprovinsi
            time.sleep(0.2)

        except (requests.RequestException, ValueError, KeyError) as error:
            failed.append(f"{province_name}: {error}")

    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)

    with OUTPUT_FILE.open("w", encoding="utf-8") as file:
        json.dump(
            locations,
            file,
            ensure_ascii=False,
            indent=2
        )

    total = sum(len(items) for items in locations.values())

    print("\nSelesai!")
    print(f"Provinsi: {len(locations)}")
    print(f"Kabupaten/kota tersimpan: {total}")
    print(f"File: {OUTPUT_FILE.resolve()}")

    if failed:
        print(f"\nAda {len(failed)} data yang gagal:")
        for item in failed:
            print("-", item)

        print(
            "\nPeriksa daftar di atas dan jalankan ulang "
            "setup_location.py jika koneksi API bermasalah."
        )


if __name__ == "__main__":
    main()
