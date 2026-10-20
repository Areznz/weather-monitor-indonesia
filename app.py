import requests
import streamlit as st
from wilayah_api import get_provinces, get_regencies
from weather_api import get_coordinates, get_weather
from datetime import datetime

# =========================================================
# CONFIGURATION
# =========================================================
st.set_page_config(
    page_title="Weather Monitor Indonesia",
    page_icon="🌦️",
    layout="wide",
    initial_sidebar_state="collapsed",
)

st.subheader("Tes koneksi geocoding")

try:
    response = requests.get(
        "https://geocoding-api.open-meteo.com/v1/search",
        params={
            "name": "Jakarta",
            "count": 5,
            "language": "en",
            "format": "json",
            "countryCode": "ID",
        },
        timeout=15,
    )

    st.write("HTTP status:", response.status_code)
    st.json(response.json())

except Exception as e:
    st.error(f"Koneksi geocoding gagal: {type(e).__name__}: {e}")
# =========================================================
# DARK GLASS UI
# =========================================================
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

    :root {
        --bg: #070d1b;
        --panel: rgba(17, 29, 53, 0.78);
        --border: rgba(148, 180, 255, 0.14);
        --blue: #65aaff;
        --muted: #91a4c4;
        --white: #f2f6ff;
    }

    .stApp {
        background:
            radial-gradient(ellipse at 5% 0%, rgba(30, 91, 190, .22), transparent 36%),
            radial-gradient(ellipse at 95% 15%, rgba(34, 115, 210, .15), transparent 32%),
            linear-gradient(145deg, #070d1b 0%, #0a1428 55%, #080e1c 100%);
        color: var(--white);
        font-family: 'Inter', sans-serif;
    }

    [data-testid="stHeader"] {
        background: transparent;
    }

    [data-testid="stAppViewContainer"] .main .block-container {
        max-width: 1440px;
        padding: 2rem 3rem 4rem;
    }

    h1, h2, h3, p, label {
        font-family: 'Inter', sans-serif !important;
    }

    /* Top navigation */
    .topbar {
        display: flex;
        align-items: center;
        justify-content: space-between;
        gap: 16px;
        margin-bottom: 30px;
    }

    .brand {
        display: flex;
        align-items: center;
        gap: 13px;
    }

    .brand-icon {
        width: 48px;
        height: 48px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 25px;
        border-radius: 16px;
        background: linear-gradient(145deg, #2477e8, #143c86);
        box-shadow: 0 8px 28px rgba(31, 111, 235, .28);
    }

    .brand-name {
        color: #f2f6ff;
        font-size: 19px;
        font-weight: 800;
        letter-spacing: -.6px;
    }

    .brand-sub {
        color: #8da4c9;
        font-size: 11px;
        margin-top: 4px;
    }

    .live-pill {
        display: inline-flex;
        align-items: center;
        gap: 8px;
        padding: 10px 14px;
        border: 1px solid rgba(85, 220, 170, .22);
        border-radius: 30px;
        background: rgba(41, 177, 125, .08);
        color: #8deac4;
        font-size: 11px;
        font-weight: 700;
    }

    .live-dot {
        height: 7px;
        width: 7px;
        border-radius: 50%;
        background: #4fe0a5;
        box-shadow: 0 0 12px #4fe0a5;
    }

    /* Hero */
    .hero {
        position: relative;
        overflow: hidden;
        display: flex;
        align-items: center;
        justify-content: space-between;
        gap: 24px;
        min-height: 270px;
        padding: 34px 38px;
        border: 1px solid rgba(151, 189, 255, .2);
        border-radius: 28px;
        background:
            radial-gradient(circle at 80% 45%, rgba(65, 139, 255, .22), transparent 32%),
            linear-gradient(115deg, rgba(21, 46, 87, .96), rgba(12, 24, 48, .95));
        box-shadow: 0 22px 70px rgba(0, 0, 0, .19);
        margin-bottom: 27px;
    }

    .hero::before {
        content: "";
        position: absolute;
        width: 260px;
        height: 260px;
        border: 1px solid rgba(130, 177, 255, .12);
        border-radius: 50%;
        right: 10%;
        top: -80px;
    }

    .hero::after {
        content: "";
        position: absolute;
        width: 190px;
        height: 190px;
        border: 1px solid rgba(130, 177, 255, .10);
        border-radius: 50%;
        right: 14%;
        bottom: -115px;
    }

    .hero-copy, .hero-art {
        position: relative;
        z-index: 1;
    }

    .eyebrow {
        color: #83baff;
        font-size: 11px;
        font-weight: 800;
        letter-spacing: 2px;
        text-transform: uppercase;
        margin-bottom: 14px;
    }

    .hero-title {
        color: #f5f8ff;
        font-size: clamp(27px, 3.5vw, 43px);
        font-weight: 800;
        line-height: 1.18;
        letter-spacing: -1.5px;
        max-width: 550px;
    }

    .hero-desc {
        color: #a9bad7;
        font-size: 13px;
        line-height: 1.8;
        margin-top: 14px;
        max-width: 480px;
    }

    .hero-art {
        min-width: 175px;
        text-align: center;
        font-size: 104px;
        filter: drop-shadow(0 10px 25px rgba(82, 160, 255, .3));
    }

    .hero-art-label {
        color: #9fc5ff;
        font-size: 11px;
        font-weight: 700;
        letter-spacing: 1px;
        margin-top: -3px;
    }

    /* Section headings */
    .section-head {
        display: flex;
        align-items: center;
        gap: 12px;
        margin: 29px 0 15px;
    }

    .section-icon {
        display: flex;
        align-items: center;
        justify-content: center;
        width: 38px;
        height: 38px;
        flex-shrink: 0;
        border: 1px solid var(--border);
        border-radius: 13px;
        background: rgba(63, 123, 222, .12);
        font-size: 19px;
    }

    .section-title {
        color: #edf3ff;
        font-size: 16px;
        font-weight: 800;
    }

    .section-subtitle {
        color: #8397b8;
        font-size: 11px;
        margin-top: 4px;
    }

    /* Location panel */
    .panel {
        padding: 23px;
        border: 1px solid var(--border);
        border-radius: 22px;
        background: linear-gradient(
            145deg,
            rgba(20, 35, 62, .86),
            rgba(12, 23, 43, .78)
        );
        box-shadow: 0 15px 38px rgba(0, 0, 0, .12);
    }

    .field-label {
        color: #a8bddc;
        font-size: 11px;
        font-weight: 700;
        margin-bottom: 9px;
    }

    [data-testid="stSelectbox"] label {
        color: #a8bddc !important;
        font-size: 12px !important;
        font-weight: 600 !important;
    }

    [data-testid="stSelectbox"] div[data-baseweb="select"] > div {
        background: #111f38 !important;
        border: 1px solid rgba(135, 170, 230, .2) !important;
        border-radius: 12px !important;
        color: #eef4ff !important;
        min-height: 46px;
    }

    [data-testid="stSelectbox"] svg {
        fill: #83baff !important;
    }

    [data-testid="stButton"] button {
        min-height: 46px;
        border: 1px solid rgba(105, 168, 255, .25);
        border-radius: 12px;
        background: linear-gradient(100deg, #2779ee, #3d9bff);
        color: white;
        font-weight: 800;
        font-size: 13px;
        box-shadow: 0 8px 22px rgba(39, 121, 238, .2);
        transition: .2s ease;
    }

    [data-testid="stButton"] button:hover {
        border-color: #8cc4ff;
        background: linear-gradient(100deg, #3989fa, #5aabff);
        transform: translateY(-1px);
    }

    /* Weather summary */
    .weather-banner {
        display: flex;
        justify-content: space-between;
        align-items: center;
        gap: 20px;
        padding: 24px 27px;
        margin: 22px 0 18px;
        border-radius: 22px;
        border: 1px solid rgba(102, 166, 255, .2);
        background:
            radial-gradient(circle at 90% 20%, rgba(60, 134, 247, .16), transparent 30%),
            linear-gradient(115deg, rgba(20, 43, 78, .9), rgba(13, 25, 47, .9));
    }

    .location-kicker {
        color: #8bbcff;
        font-size: 10px;
        font-weight: 800;
        letter-spacing: 1.5px;
        text-transform: uppercase;
    }

    .location-name {
        color: #f2f6ff;
        font-size: 21px;
        font-weight: 800;
        margin-top: 8px;
        line-height: 1.4;
    }

    .location-coord {
        color: #8fa5c7;
        font-size: 11px;
        margin-top: 8px;
    }

    .temperature {
        color: #f5f8ff;
        font-size: 43px;
        font-weight: 800;
        letter-spacing: -2px;
        white-space: nowrap;
    }

    .temperature-caption {
        color: #a4bbdc;
        font-size: 11px;
        text-align: right;
        margin-top: 3px;
    }

    /* Metric cards */
    .metric-card {
        min-height: 155px;
        padding: 20px;
        border: 1px solid rgba(145, 178, 235, .15);
        border-radius: 19px;
        background: linear-gradient(
            150deg,
            rgba(23, 39, 67, .9),
            rgba(13, 24, 44, .9)
        );
        transition: transform .2s ease, border-color .2s ease;
    }

    .metric-icon {
        display: flex;
        align-items: center;
        justify-content: center;
        width: 43px;
        height: 43px;
        border-radius: 14px;
        background: rgba(70, 139, 245, .13);
        border: 1px solid rgba(98, 164, 255, .16);
        font-size: 22px;
        margin-bottom: 19px;
    }

    .metric-label {
        color: #93a8c8;
        font-size: 11px;
        font-weight: 600;
    }

    .metric-value {
        color: #f0f5ff;
        font-size: 25px;
        font-weight: 800;
        margin-top: 7px;
        letter-spacing: -.7px;
        overflow-wrap: anywhere;
    }

    .metric-note {
        color: #7189ad;
        font-size: 10px;
        margin-top: 5px;
    }

    /* Details and illustrations */
    .detail-card {
        padding: 19px;
        border: 1px solid var(--border);
        border-radius: 18px;
        background: rgba(17, 30, 52, .78);
        min-height: 118px;
    }

    .detail-top {
        color: #9aafd0;
        font-size: 11px;
        font-weight: 600;
    }

    .detail-value {
        color: #f0f5ff;
        font-size: 22px;
        font-weight: 800;
        margin-top: 13px;
    }

    .detail-icon {
        font-size: 21px;
        margin-bottom: 8px;
    }

    .illustration-strip {
        display: grid;
        grid-template-columns: repeat(4, minmax(0, 1fr));
        gap: 12px;
        margin-top: 18px;
    }

    .illustration {
        padding: 18px 10px;
        border-radius: 17px;
        text-align: center;
        border: 1px solid rgba(130, 169, 232, .12);
        background: rgba(20, 35, 60, .58);
    }

    .illustration-emoji {
        font-size: 30px;
        margin-bottom: 10px;
    }

    .illustration-title {
        color: #dbe8ff;
        font-size: 11px;
        font-weight: 700;
    }

    .illustration-desc {
        color: #7f96b9;
        font-size: 9px;
        margin-top: 5px;
    }

    .empty-state {
        text-align: center;
        padding: 28px 15px;
        border: 1px dashed rgba(126, 167, 236, .24);
        border-radius: 20px;
        background: rgba(16, 29, 51, .55);
    }

    .empty-emoji {
        font-size: 50px;
        margin-bottom: 12px;
    }

    .empty-title {
        color: #e8f0ff;
        font-size: 17px;
        font-weight: 800;
    }

    .empty-desc {
        color: #8da3c5;
        font-size: 12px;
        line-height: 1.8;
        max-width: 440px;
        margin: 9px auto 0;
    }

    .footer {
        margin-top: 38px;
        padding-top: 20px;
        border-top: 1px solid rgba(135, 166, 222, .12);
        text-align: center;
        color: #6e83a5;
        font-size: 10px;
        line-height: 1.8;
    }

    @media (max-width: 700px) {
        [data-testid="stAppViewContainer"] .main .block-container {
            padding: 1rem 1rem 2rem;
        }

        .hero {
            padding: 25px 22px;
            min-height: 220px;
        }

        .hero-art {
            min-width: 75px;
            font-size: 58px;
        }

        .hero-title {
            font-size: 27px;
        }

        .illustration-strip {
            grid-template-columns: repeat(2, minmax(0, 1fr));
        }

        .temperature {
            font-size: 31px;
        }

        .location-name {
            font-size: 16px;
        }
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# =========================================================
# REUSABLE COMPONENTS
# =========================================================
def section_heading(icon, title, subtitle):
    st.markdown(
        f"""
        <div class="section-head">
            <div class="section-icon">{icon}</div>
            <div>
                <div class="section-title">{title}</div>
                <div class="section-subtitle">{subtitle}</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def metric_card(icon, label, value, note):
    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-icon">{icon}</div>
            <div class="metric-label">{label}</div>
            <div class="metric-value">{value}</div>
            <div class="metric-note">{note}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def detail_card(icon, label, value):
    st.markdown(
        f"""
        <div class="detail-card">
            <div class="detail-icon">{icon}</div>
            <div class="detail-top">{label}</div>
            <div class="detail-value">{value}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def normalize_data(data):
    """Menormalkan respons API menjadi list berisi dictionary."""
    if isinstance(data, dict):
        if isinstance(data.get("data"), list):
            data = data["data"]
        elif "name" in data:
            data = [data]
        else:
            return []

    if isinstance(data, list):
        return [
            item
            for item in data
            if isinstance(item, dict) and "name" in item
        ]

    return []


def format_value(value, unit=""):
    """Menampilkan nilai yang tersedia tanpa mengarang data."""
    if value is None or value == "":
        return "—"

    return f"{value}{unit}"


# =========================================================
# TOP NAVIGATION
# =========================================================
today = datetime.now().strftime("%d %B %Y")

st.markdown(
    f"""
    <div class="topbar">
        <div class="brand">
            <div class="brand-icon">🌦️</div>
            <div>
                <div class="brand-name">Weather<span style="color:#65aaff">Monitor</span></div>
                <div class="brand-sub">INDONESIA WEATHER INTELLIGENCE</div>
            </div>
        </div>
        <div class="live-pill">
            <span class="live-dot"></span>
            WEATHER DASHBOARD
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

# =========================================================
# HERO SECTION
# =========================================================
st.markdown(
    f"""
    <div class="hero">
        <div class="hero-copy">
            <div class="eyebrow">✦ INDONESIA WEATHER CENTER</div>
            <div class="hero-title">
                Cuaca Indonesia,<br>
                dalam satu tampilan.
            </div>
            <div class="hero-desc">
                Pantau kondisi cuaca kabupaten dan kota di seluruh Indonesia.
                Pilih wilayahmu dan dapatkan informasi cuaca terkini.
            </div>
        </div>
        <div class="hero-art">
            🌤️
            <div class="hero-art-label">EXPLORE THE WEATHER</div>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

# =========================================================
# LOAD PROVINCES
# =========================================================
try:
    provinces = normalize_data(get_provinces())
except Exception as e:
    st.error(f"Gagal mengambil data provinsi: {e}")
    st.stop()

if not provinces:
    st.error("Data provinsi kosong atau format API tidak sesuai.")
    st.stop()

province_names = [p["name"] for p in provinces]

# =========================================================
# LOCATION SELECTOR
# =========================================================
section_heading(
    "📍",
    "Jelajahi wilayah",
    "Pilih provinsi dan kabupaten/kota untuk melihat kondisi cuaca.",
)

with st.container(border=True):
    st.markdown(
        """
        <div style="color:#e9f1ff;font-size:14px;font-weight:800;margin-bottom:5px">
            Tentukan lokasi pemantauan
        </div>
        <div style="color:#8298ba;font-size:11px;margin-bottom:18px">
            🇮🇩  Menjangkau berbagai wilayah di Indonesia
        </div>
        """,
        unsafe_allow_html=True,
    )

    province_col, regency_col = st.columns(2)

    with province_col:
        selected_province = st.selectbox(
            "🌏 Provinsi",
            province_names,
            key="selected_province",
        )

    province_data = next(
        p for p in provinces if p["name"] == selected_province
    )

    province_code = province_data.get(
        "id",
        province_data.get("code"),
    )

    if province_code is None:
        st.error(f"ID provinsi tidak ditemukan: {province_data}")
        st.stop()

    # Load regencies when province changes
    try:
        regencies = normalize_data(get_regencies(province_code))
    except Exception as e:
        st.error(f"Gagal mengambil data kabupaten/kota: {e}")
        st.stop()

    if not regencies:
        st.warning("Data kabupaten/kota untuk provinsi ini kosong.")
        st.stop()

    regency_names = [r["name"] for r in regencies]

    with regency_col:
        selected_regency = st.selectbox(
            "🏙️ Kabupaten / Kota",
            regency_names,
            key=f"regency_{province_code}",
        )

    st.markdown("<div style='height:5px'></div>", unsafe_allow_html=True)

    search_col, info_col = st.columns([1, 1.7])

    with search_col:
        search_weather = st.button(
            "🌦️  Tampilkan Cuaca",
            use_container_width=True,
            type="primary",
        )

    with info_col:
        st.markdown(
            """
            <div style="color:#8298ba;font-size:11px;padding:13px 2px">
                ✨ Data diambil saat kamu meminta pembaruan cuaca.
            </div>
            """,
            unsafe_allow_html=True,
        )

# =========================================================
# FETCH WEATHER
# =========================================================
if search_weather:
    try:
        with st.spinner("Mengambil koordinat dan data cuaca..."):
            location = get_coordinates(
                selected_regency,
                selected_province,
            )

            if location is None:
                st.session_state.pop("weather_result", None)
                st.error(
                    "Koordinat lokasi tidak ditemukan. "
                    "Coba periksa nama wilayah atau fungsi get_coordinates()."
                )
            else:
                weather = get_weather(
                    location["latitude"],
                    location["longitude"],
                )

                if not weather or not weather.get("current"):
                    st.session_state.pop("weather_result", None)
                    st.error(
                        "Data cuaca belum berhasil diambil. "
                        "Silakan coba lagi."
                    )
                else:
                    st.session_state["weather_result"] = {
                        "province": selected_province,
                        "regency": selected_regency,
                        "location": location,
                        "weather": weather,
                    }

    except Exception as e:
        st.session_state.pop("weather_result", None)
        st.error(f"Terjadi kesalahan saat mengambil data cuaca: {e}")

# =========================================================
# WEATHER RESULTS
# =========================================================
result = st.session_state.get("weather_result")

if result:
    # Avoid displaying old results as if they belonged to a new selection
    if (
        result["province"] != selected_province
        or result["regency"] != selected_regency
    ):
        result = None

if result:
    current = result["weather"]["current"]
    location = result["location"]

    temperature = format_value(current.get("temperature_2m"), "°C")
    humidity = format_value(current.get("relative_humidity_2m"), "%")
    feels_like = format_value(current.get("apparent_temperature"), "°C")
    wind_speed = format_value(current.get("wind_speed_10m"), " km/jam")

    section_heading(
        "🌤️",
        "Ringkasan cuaca",
        "Kondisi yang dilaporkan API untuk wilayah pilihanmu.",
    )

    st.markdown(
        f"""
        <div class="weather-banner">
            <div>
                <div class="location-kicker">📍 CURRENT LOCATION</div>
                <div class="location-name">
                    {result["regency"]}, {result["province"]}
                </div>
                <div class="location-coord">
                    Koordinat: {location["latitude"]}, {location["longitude"]}
                </div>
            </div>
            <div>
                <div class="temperature">{temperature}</div>
                <div class="temperature-caption">🌡️ Suhu saat ini</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Main metrics
    metric_columns = st.columns(4, gap="medium")

    with metric_columns[0]:
        metric_card(
            "🌡️",
            "SUHU UDARA",
            temperature,
            "Temperatur 2 meter",
        )

    with metric_columns[1]:
        metric_card(
            "💧",
            "KELEMBAPAN",
            humidity,
            "Kelembapan relatif",
        )

    with metric_columns[2]:
        metric_card(
            "🌡️",
            "SUHU TERASA",
            feels_like,
            "Apparent temperature",
        )

    with metric_columns[3]:
        metric_card(
            "💨",
            "KECEPATAN ANGIN",
            wind_speed,
            "Kecepatan angin 10 meter",
        )

    # Additional weather details
    section_heading(
        "🧭",
        "Detail atmosfer",
        "Informasi tambahan dari data cuaca yang tersedia.",
    )

    detail_columns = st.columns(3, gap="medium")

    with detail_columns[0]:
        detail_card(
            "🌧️",
            "Curah hujan",
            format_value(current.get("precipitation"), " mm"),
        )

    with detail_columns[1]:
        detail_card(
            "🧭",
            "Arah angin",
            format_value(current.get("wind_direction_10m"), "°"),
        )

    with detail_columns[2]:
        detail_card(
            "🕐",
            "Waktu data API",
            format_value(current.get("time")),
        )

    # Atmospheric illustration strip
    section_heading(
        "✨",
        "Weather atmosphere",
        "Elemen cuaca yang memperkaya dashboard.",
    )

    st.markdown(
        """
        <div class="illustration-strip">
            <div class="illustration">
                <div class="illustration-emoji">☀️</div>
                <div class="illustration-title">Solar</div>
                <div class="illustration-desc">Atmosfer cerah</div>
            </div>
            <div class="illustration">
                <div class="illustration-emoji">☁️</div>
                <div class="illustration-title">Clouds</div>
                <div class="illustration-desc">Langit berawan</div>
            </div>
            <div class="illustration">
                <div class="illustration-emoji">🌧️</div>
                <div class="illustration-title">Rain</div>
                <div class="illustration-desc">Presipitasi</div>
            </div>
            <div class="illustration">
                <div class="illustration-emoji">💨</div>
                <div class="illustration-title">Wind</div>
                <div class="illustration-desc">Aliran udara</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

else:
    # Empty state before the first successful request
    section_heading(
        "🛰️",
        "Weather overview",
        "Dashboard cuaca akan ditampilkan setelah lokasi dipilih.",
    )

    st.markdown(
        """
        <div class="empty-state">
            <div class="empty-emoji">🌍</div>
            <div class="empty-title">Siap memantau cuaca?</div>
            <div class="empty-desc">
                Pilih provinsi dan kabupaten/kota di atas, lalu tekan
                <b>Tampilkan Cuaca</b> untuk mengambil data cuaca terbaru
                yang tersedia dari API.
            </div>
        </div>
        <div class="illustration-strip">
            <div class="illustration">
                <div class="illustration-emoji">☀️</div>
                <div class="illustration-title">Temperature</div>
                <div class="illustration-desc">Suhu udara</div>
            </div>
            <div class="illustration">
                <div class="illustration-emoji">💧</div>
                <div class="illustration-title">Humidity</div>
                <div class="illustration-desc">Kelembapan</div>
            </div>
            <div class="illustration">
                <div class="illustration-emoji">🌧️</div>
                <div class="illustration-title">Precipitation</div>
                <div class="illustration-desc">Curah hujan</div>
            </div>
            <div class="illustration">
                <div class="illustration-emoji">💨</div>
                <div class="illustration-title">Wind</div>
                <div class="illustration-desc">Kecepatan angin</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

# =========================================================
# FOOTER
# =========================================================
st.markdown(
    """
    <div class="footer">
        <b style="color:#a9c8ff">WEATHER MONITOR INDONESIA</b><br>
        A weather monitoring dashboard for Indonesian regions.<br>
        Data ditampilkan berdasarkan respons API yang tersedia.
    </div>
    """,
    unsafe_allow_html=True,
)
