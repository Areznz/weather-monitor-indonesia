import requests
import streamlit as st

BASE_URL = "https://www.emsifa.com/api-wilayah-indonesia/v2"


@st.cache_data(ttl=86400)
def get_provinces():
    url = f"{BASE_URL}/provinces.json"
    response = requests.get(url, timeout=15)
    response.raise_for_status()

    result = response.json()
    return result["data"]


@st.cache_data(ttl=86400)
def get_regencies(province_code):
    url = f"{BASE_URL}/regencies/{province_code}.json"
    response = requests.get(url, timeout=15)
    response.raise_for_status()

    result = response.json()
    return result["data"]
