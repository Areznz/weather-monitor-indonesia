
import streamlit as st

from wilayah_api import get_provinces, get_regencies
from weather_api import get_coordinates, get_weather

# ==========================================
# CONFIG
# ==========================================
st.set_page_config(
    page_title="Weather Monitor Indonesia",
    page_icon="🌤️",
    layout="wide"
)

st.title("🌤️ Weather Monitor Indonesia")
st.write("Pemantauan cuaca kabupaten/kota di seluruh Indonesia.")


# ==========================================
# NORMALISASI DATA
# ==========================================
def normalize_data(data):
    if isinstance(data, dict):
        if isinstance(data.get("data"), list):
            data = data["data"]
        elif "name" in data:
            data = [data]
        else:
            return []

    if isinstance(data, list):
        return [
            item for item in data
            if isinstance(item, dict) and "name" in item
        ]

    return []


# ==========================================
# PROVINSI
# ==========================================
try:
    provinces = normalize_data(get_provinces())
except Exception as e:
    st.error(f"Gagal mengambil data provinsi: {e}")
    st.stop()

if not provinces:
    st.error("Data provinsi kosong atau format API tidak sesuai.")
    st.stop()

province_names = [p["name"] for p in provinces]

selected_province = st.selectbox(
    "🇮🇩 Pilih Provinsi",
    province_names
)

province_data = next(
    p for p in provinces if p["name"] == selected_province
)

province_code = province_data.get("id", province_data.get("code"))

if province_code is None:
    st.error(f"ID provinsi tidak ditemukan: {province_data}")
    st.stop()


# ==========================================
# KABUPATEN / KOTA
# ==========================================
try:
    regencies = normalize_data(get_regencies(province_code))
except Exception as e:
    st.error(f"Gagal mengambil data kabupaten/kota: {e}")
    st.stop()

if not regencies:
    st.error("Data kabupaten/kota kosong.")
    st.stop()

regency_names = [r["name"] for r in regencies]

selected_regency = st.selectbox(
    "📍 Pilih Kabupaten/Kota",
    regency_names
)


# ==========================================
# TOMBOL CUACA
# ==========================================
if st.button("🌤️ Tampilkan Cuaca", use_container_width=True):

    with st.spinner("Mencari koordinat dan mengambil data cuaca..."):

        # TES KOORDINAT
        st.write("### 🔎 Tes pencarian koordinat")
        st.write("Kabupaten/kota:", selected_regency)
        st.write("Provinsi:", selected_province)

        try:
            location = get_coordinates(
                selected_regency,
                selected_province
            )

            st.write("Hasil koordinat:", location)

            if location is None:
                st.error(
                    "Koordinat tidak ditemukan. "
                    "Fungsi get_coordinates() mengembalikan None."
                )
                st.info(
                    "Pencarian nama lokasi gagal. "
                    "Periksa weather_api.py atau gunakan database "
                    "koordinat lokal."
                )
                st.stop()

            weather = get_weather(
                location["latitude"],
                location["longitude"]
            )

            if not weather or not weather.get("current"):
                st.error(
                    "Koordinat ditemukan, tetapi data cuaca gagal diambil."
                )
                st.stop()

        except Exception as e:
            st.error(f"Terjadi kesalahan: {e}")
            st.stop()

    current = weather["current"]

    # ======================================
    # INFORMASI LOKASI
    # ======================================
    st.success(f"📍 {selected_regency}, {selected_province}")

    st.caption(
        f"Koordinat: {location['latitude']}, "
        f"{location['longitude']}"
    )

    # ======================================
    # KARTU CUACA
    # ======================================
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            "🌡️ Suhu",
            f"{current.get('temperature_2m', '-')} °C"
        )

    with col2:
        st.metric(
            "💧 Kelembapan",
            f"{current.get('relative_humidity_2m', '-')} %"
        )

    with col3:
        st.metric(
            "🌡️ Terasa",
            f"{current.get('apparent_temperature', '-')} °C"
        )

    with col4:
        st.metric(
            "💨 Angin",
            f"{current.get('wind_speed_10m', '-')} km/jam"
        )

    # ======================================
    # INFORMASI TAMBAHAN
    # ======================================
    st.divider()

    col1, col2, col3 = st.columns(3)

    with col1:
        st.write("🌧️ **Curah hujan**")
        st.write(f"{current.get('precipitation', '-')} mm")

    with col2:
        st.write("🧭 **Arah angin**")
        st.write(f"{current.get('wind_direction_10m', '-')}°")

    with col3:
        st.write("🕐 **Update**")
        st.write(current.get("time", "-"))
