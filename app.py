import streamlit as st

# ======================================
# IMPORT MODULE
# ======================================
from utils.load_data import load_data
from utils.filters import top_filter
from utils.style import load_css
from utils.icons import icon, section_header, metric_row
from utils import kpi

from utils.charts import (
    revenue_trend,
    top_selling_category,
    city_contribution,

    promo_revenue,
    promo_trend,
    promo_vs_category,

    customer_channel,
    channel_by_city,
    weekend_vs_weekday,

    category_by_city,
    promo_by_city,
    satisfaction_by_city,
)

# =====================================================
# PAGE CONFIG
# =====================================================

st.set_page_config(
    page_title="KopiSeru Marketing Dashboard",
    layout="wide",
    initial_sidebar_state="collapsed",
)

load_css()

# =====================================================
# LOAD DATA
# =====================================================

df = load_data()

# =====================================================
# HEADER
# =====================================================

st.markdown(
    f"""
    <div class="app-header">
        <div class="mark">{icon("cup", size=20, color="#FFFFFF")}</div>
        <div>
            <h1>KopiSeru Marketing Dashboard</h1>
            <p class="subtitle">Analitik performa pemasaran & kampanye — tim Marketing</p>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

# =====================================================
# FILTER
# =====================================================

filtered_df = top_filter(df)

if filtered_df.empty:
    st.warning("Tidak ada data yang sesuai dengan filter yang dipilih.")
    st.stop()

# =====================================================
# HELPER
# =====================================================

CHART_HEIGHT = 225


def show_chart(fig, height=CHART_HEIGHT):
    fig.update_layout(height=height)
    st.plotly_chart(
        fig,
        width="stretch",
        config={"displayModeBar": False, "responsive": True},
    )


def chart_card(title, fig, height=CHART_HEIGHT):
    with st.container(border=True):
        st.markdown(
            f'<div style="font-size:12.5px; font-weight:600; color:var(--text); '
            f'margin-bottom:2px;">{title}</div>',
            unsafe_allow_html=True,
        )
        show_chart(fig, height=height)


# =====================================================
# TAB MENU
# =====================================================

tab1, tab2, tab3, tab4 = st.tabs([
    "Ringkasan Pemasaran",
    "Efektivitas Promosi",
    "Perilaku Pelanggan",
    "Peluang Pasar",
])

# =====================================================
# TAB 1 — RINGKASAN PEMASARAN
# =====================================================

with tab1:

    section_header(
        "Ringkasan Performa Pemasaran",
        "Gambaran umum reach, kepuasan pelanggan, dan kontribusi promo terhadap revenue",
        "overview",
        accent_key="revenue",
    )

    metric_row(kpi.overview_kpis(filtered_df))

    col1, col2, col3 = st.columns([1.1, 1, 1])

    with col1:
        chart_card("Trend Revenue Bulanan", revenue_trend(filtered_df))

    with col2:
        chart_card("Kategori Produk Terlaris", top_selling_category(filtered_df))

    with col3:
        chart_card("Kontribusi Revenue per Kota", city_contribution(filtered_df))

# =====================================================
# TAB 2 — EFEKTIVITAS PROMOSI
# =====================================================

with tab2:

    section_header(
        "Efektivitas Promosi",
        "Jenis promo mana yang paling mendorong revenue, dan kategori apa yang paling terdampak",
        "gift",
        accent_key="promo",
    )

    metric_row(kpi.promo_kpis(filtered_df))

    col1, col2, col3 = st.columns([1, 1.1, 1.1])

    with col1:
        chart_card("Revenue per Jenis Promo", promo_revenue(filtered_df))

    with col2:
        chart_card("Revenue Promo per Tahun", promo_trend(filtered_df))

    with col3:
        chart_card("Promo vs Kategori Produk", promo_vs_category(filtered_df))

# =====================================================
# TAB 3 — PERILAKU PELANGGAN
# =====================================================

with tab3:

    section_header(
        "Perilaku & Preferensi Pelanggan",
        "Channel favorit pelanggan dan pola waktu transaksi untuk menentukan waktu & kanal campaign",
        "users",
        accent_key="customer",
    )

    metric_row(kpi.behavior_kpis(filtered_df))

    col1, col2, col3 = st.columns([0.9, 1.2, 0.9])

    with col1:
        chart_card("Komposisi Sales Channel", customer_channel(filtered_df))

    with col2:
        chart_card("Sales Channel per Kota", channel_by_city(filtered_df))

    with col3:
        chart_card("Rata-rata Revenue: Weekday vs Weekend", weekend_vs_weekday(filtered_df))

# =====================================================
# TAB 4 — PELUANG PASAR
# =====================================================

with tab4:

    section_header(
        "Peluang Pasar & Segmentasi",
        "Kota dengan potensi tertinggi untuk ekspansi campaign berdasarkan kategori, promo, dan loyalitas",
        "map",
        accent_key="category",
    )

    metric_row(kpi.opportunity_kpis(filtered_df))

    col1, col2, col3 = st.columns([1.1, 1.1, 0.9])

    with col1:
        chart_card("Komposisi Kategori per Kota", category_by_city(filtered_df))

    with col2:
        chart_card("Revenue Promo per Kota", promo_by_city(filtered_df))

    with col3:
        chart_card("Kepuasan Pelanggan per Kota", satisfaction_by_city(filtered_df))
