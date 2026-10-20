
import streamlit as st
from wilayah_api import get_provinces, get_regencies
from weather_api import get_coordinates, get_weather

# ==========================================
# CONFIG
# ==========================================
st.set_page_config(
    page_title="Weather Monitor Indonesia",
    page_icon="🌤️",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ==========================================
# CUSTOM CSS
# ==========================================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

:root {
    --bg: #07111f;
    --panel: #101e31;
    --border: rgba(148, 178, 220, 0.16);
    --text: #edf4ff;
    --muted: #91a4bf;
    --blue: #60a5fa;
}

.stApp {
    background:
        radial-gradient(ellipse at 10% 0%, rgba(37, 99, 235, .19), transparent 38%),
        radial-gradient(ellipse at 90% 15%, rgba(14, 165, 233, .11), transparent 32%),
        var(--bg);
    color: var(--text);
    font-family: 'Inter', sans-serif;
}

header[data-testid="stHeader"] {
    background: transparent;
}

.block-container {
    max-width: 1200px;
    padding-top: 2.5rem;
    padding-bottom: 4rem;
}

#MainMenu, footer {
    visibility: hidden;
}

.hero {
    padding: 30px 32px;
    margin-bottom: 26px;
    border: 1px solid var(--border);
    border-radius: 24px;
    background: linear-gradient(
        125deg,
        rgba(20, 42, 72, .95),
        rgba(12, 26, 44, .88)
    );
    box-shadow: 0 18px 60px rgba(0, 0, 0, .18);
    position: relative;
    overflow: hidden;
}

.hero::after {
    content: "";
    position: absolute;
    width: 230px;
    height: 230px;
    right: -70px;
    top: -100px;
    border-radius: 50%;
    background: rgba(59, 130, 246, .12);
    filter: blur(8px);
}

.eyebrow {
    color: #7dd3fc;
    font-size: 12px;
    font-weight: 700;
    letter-spacing: 2px;
    text-transform: uppercase;
    margin-bottom: 12px;
}

.hero h1 {
    color: #f3f7ff;
    font-size: clamp(28px, 4vw, 42px);
    font-weight: 800;
    letter-spacing: -1.5px;
    line-height: 1.15;
    margin: 0 0 12px 0;
}

.hero p {
    color: #a9bad2;
    font-size: 15px;
    line-height: 1.7;
    margin: 0;
    max-width: 620px;
}

.section-title {
    color: #f1f5f9;
    font-size: 19px;
    font-weight: 700;
    margin: 8px 0 4px 0;
}

.section-caption {
    color: var(--muted);
    font-size: 13px;
    margin-bottom: 20px;
}

div[data-testid="stVerticalBlockBorderWrapper"] {
    border: 1px solid var(--border);
    border-radius: 20px;
    background: rgba(15, 29, 48, .76);
}

div[data-testid="stSelectbox"] label {
    color: #c8d6e9;
    font-weight: 600;
    font-size: 13px;
}

div[data-baseweb="select"] > div {
    background: #101f33;
    border-color: rgba(148, 178, 220, .23);
    border-radius: 12px;
    color: #edf4ff;
    min-height: 46px;
}

div[data-baseweb="select"] input {
    color: #edf4ff;
}

div[data-testid="stButton"] > button {
    min-height: 48px;
    border: 1px solid rgba(96, 165, 250, .4);
    border-radius: 12px;
    background: linear-gradient(110deg, #2563eb, #0284c7);
    color: white;
    font-weight: 700;
    transition: all .2s ease;
}

div[data-testid="stButton"] > button:hover {
    border-color: #93c5fd;
    background: linear-gradient(110deg, #1d4ed8, #0369a1);
    box-shadow: 0 8px 25px rgba(37, 99, 235, .2);
    transform: translateY(-1px);
}

div[data-testid="stMetric"] {
    padding: 22px 20px;
    min-height: 140px;
    border: 1px solid var(--border);
    border-radius: 18px;
    background: linear-gradient(
        145deg,
        rgba(21, 40, 65, .94),
        rgba(12, 25, 42, .94)
    );
}

div[data-testid="stMetricLabel"] {
    color: #a7bad4;
    font-size: 13px;
    font-weight: 600;
}

div[data-testid="stMetricValue"] {
    color: #f1f7ff;
    font-size: clamp(22px, 2.5vw, 32px);
    font-weight: 800;
}

div[data-testid="stMetricDelta"] {
    color: #7dd3fc;
}

.info-card {
    padding: 20px;
    height: 100%;
    border: 1px solid var(--border);
    border-radius: 16px;
    background: rgba(16, 31, 51, .85);
}

.info-label {
    color: #9eb1cb;
    font-size: 13px;
    margin-bottom: 10px;
}

.info-value {
    color: #edf4ff;
    font-size: 21px;
    font-weight: 700;
    overflow-wrap: anywhere;
}

.location-card {
    padding: 20px 22px;
    margin: 22px 0 18px 0;
    border: 1px solid rgba(96, 165, 250, .24);
    border-radius: 17px;
    background: linear-gradient(
        110deg,
        rgba(30, 64, 110, .32),
        rgba(15, 29, 48, .65)
    );
}

.location-name {
    color: #f1f7ff;
    font-size: 20px;
    font-weight: 700;
    margin-bottom: 6px;
}

.location-coords {
    color: #9eb1cb;
    font-size: 12px;
}

.footer {
    text-align: center;
    color: #71839c;
    font-size: 12px;
    padding-top: 35px;
}

hr {
    border-color: var(--border);
}

[data-testid="stAlert"] {
    border-radius: 12px;
}

@media (max-width: 640px) {
    .block-container {
        padding-top: 1rem;
        padding-left: 1rem;
        padding-right: 1rem;
    }

    .hero {
        padding: 24px 20px;
        border-radius: 18px;
    }

    div[data-testid="stMetric"] {
        padding: 15px;
        min-height: 115px;
    }
}
</style>
""", unsafe_allow_html=True)

# ==========================================
# HEADER
# ==========================================
st.markdown("""
<div class="hero">
    <div class="eyebrow">INDONESIA · WEATHER INTELLIGENCE</div>
    <h1>Weather Monitor<br>Indonesia.</h1>
    <p>
        Pantau kondisi cuaca kabupaten dan kota di seluruh Indonesia.
        Pilih wilayah untuk melihat kondisi cuaca terkini secara praktis.
    </p>
</div>
""", unsafe_allow_html=True)

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
# PILIH WILAYAH
# ==========================================
st.markdown(
    '<div class="section-title">Pilih wilayah pemantauan</div>'
    '<div class="section-caption">'
    'Tentukan provinsi dan kabupaten/kota yang ingin kamu pantau.'
    '</div>',
    unsafe_allow_html=True,
)

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
    "🇮🇩 Provinsi",
    province_names,
    key="province_select",
)

province_data = next(
    p for p in provinces if p["name"] == selected_province
)

province_code = province_data.get("id", province_data.get("code"))

if province_code is None:
    st.error(f"ID provinsi tidak ditemukan: {province_data}")
    st.stop()

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
    "📍 Kabupaten/Kota",
    regency_names,
    key=f"regency_select_{province_code}",
)

st.write("")

# ==========================================
# TOMBOL AMBIL CUACA
# ==========================================
show_weather = st.button(
    "Tampilkan Cuaca  →",
    use_container_width=True,
)

if show_weather:
    with st.spinner("Mengambil koordinat dan data cuaca..."):
        try:
            location = get_coordinates(
                selected_regency,
                selected_province,
            )

            if location is None:
                st.error(
                    "Koordinat lokasi tidak ditemukan. "
                    "Coba periksa nama wilayah atau konfigurasi API."
                )
                st.stop()

            weather = get_weather(
                location["latitude"],
                location["longitude"],
            )

            if not weather or not weather.get("current"):
                st.error(
                    "Data cuaca gagal diambil. "
                    "Silakan coba lagi beberapa saat."
                )
                st.stop()

        except Exception as e:
            st.error(f"Terjadi kesalahan saat mengambil cuaca: {e}")
            st.stop()

    current = weather["current"]

    # ======================================
    # INFORMASI LOKASI
    # ======================================
    st.markdown(
        f"""
        <div class="location-card">
            <div class="eyebrow">CURRENT LOCATION</div>
            <div class="location-name">
                📍 {selected_regency}, {selected_province}
            </div>
            <div class="location-coords">
                Koordinat: {location['latitude']}, {location['longitude']}
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # ======================================
    # METRIK CUACA UTAMA
    # ======================================
    st.markdown(
        '<div class="section-title">Kondisi cuaca saat ini</div>'
        '<div class="section-caption">'
        'Ringkasan kondisi atmosfer di wilayah yang dipilih.'
        '</div>',
        unsafe_allow_html=True,
    )

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            "🌡️ Suhu udara",
            f"{current.get('temperature_2m', '-')} °C",
        )

    with col2:
        st.metric(
            "💧 Kelembapan",
            f"{current.get('relative_humidity_2m', '-')} %",
        )

    with col3:
        st.metric(
            "🌡️ Terasa seperti",
            f"{current.get('apparent_temperature', '-')} °C",
        )

    with col4:
        st.metric(
            "💨 Kecepatan angin",
            f"{current.get('wind_speed_10m', '-')} km/jam",
        )

    # ======================================
    # INFORMASI TAMBAHAN
    # ======================================
    st.write("")
    st.markdown(
        '<div class="section-title">Detail atmosfer</div>'
        '<div class="section-caption">'
        'Informasi tambahan dari data cuaca yang diterima.'
        '</div>',
        unsafe_allow_html=True,
    )

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown(
            f"""
            <div class="info-card">
                <div class="info-label">🌧️ Curah hujan</div>
                <div class="info-value">
                    {current.get('precipitation', '-')} mm
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with col2:
        st.markdown(
            f"""
            <div class="info-card">
                <div class="info-label">🧭 Arah angin</div>
                <div class="info-value">
                    {current.get('wind_direction_10m', '-')}°
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with col3:
        st.markdown(
            f"""
            <div class="info-card">
                <div class="info-label">🕐 Waktu data</div>
                <div class="info-value">
                    {current.get('time', '-')}
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

# ==========================================
# FOOTER
# ==========================================
st.markdown("""
<div class="footer">
    WEATHER MONITOR INDONESIA · Built for a more informed day.
</div>
""", unsafe_allow_html=True)
