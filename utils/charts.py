import plotly.express as px

from utils.theme import (
    PLOTLY_LAYOUT, QUALITATIVE,
    COLOR_REVENUE, COLOR_PROMO, COLOR_CUSTOMER, COLOR_CATEGORY,
    SUBTEXT, CARD,
)

BAR_GAP = 0.35

MILIAR = 1_000_000_000


def _base(fig, legend=False):

    fig.update_layout(**PLOTLY_LAYOUT)

    fig.update_layout(
        margin=dict(
            l=10,
            r=15,
            t=30,
            b=30
        ),
        font=dict(size=12),
        hoverlabel=dict(font_size=12)
    )

    if legend:
        fig.update_layout(
            legend=dict(
                orientation="h",
                y=1.18,
                x=0,
                xanchor="left",
                yanchor="bottom",
                font=dict(size=10),
                itemwidth=30,
            )
        )

    return fig

def _single_bar(fig, color):
    fig.update_traces(
        marker=dict(color=color, line=dict(width=0)),
        textfont=dict(color=SUBTEXT, size=11),
        cliponaxis=False,
    )
    fig.update_layout(bargap=BAR_GAP, showlegend=False)
    return _base(fig)


def _multi_bar(fig):
    fig.update_traces(marker=dict(line=dict(width=0)), cliponaxis=False)
    fig.update_layout(bargap=BAR_GAP, bargroupgap=0.12)
    return _base(fig, legend=True)


def _line(fig):
    fig.update_traces(line=dict(width=2.2), marker=dict(size=5))
    return _base(fig, legend=True)


def _donut(fig):
    fig.update_traces(
        textposition="outside",
        textinfo="percent+label",
        textfont=dict(size=11, color=SUBTEXT),
        marker=dict(line=dict(color=CARD, width=2)),
    )
    fig.update_layout(showlegend=False)
    return _base(fig)


def _rev_axis_title():
    return "Revenue (Miliar Rp)"


def _dynamic_range(values, pad_ratio=0.35, min_pad=0.05, floor_at_zero=True):
    """
    Hitung range sumbu secara dinamis berdasarkan data yang sudah difilter,
    bukan angka hardcode. Mencegah bar 'hilang' saat filter membuat nilai
    data jauh lebih kecil/besar dari rentang yang sebelumnya di-hardcode.

    - values: iterable angka (misal kolom pandas)
    - pad_ratio: persentase padding dari selisih max-min
    - min_pad: padding minimum kalau semua nilai sama / cuma 1 titik
    - floor_at_zero: kalau True, batas bawah tidak akan turun di bawah 0
      (cocok untuk chart revenue yang tidak mungkin negatif)
    """
    values = [v for v in values if v == v]  # buang NaN

    if not values:
        return [0, 1]

    vmin, vmax = min(values), max(values)

    if vmin == vmax:
        pad = max(abs(vmin) * pad_ratio, min_pad)
    else:
        pad = max((vmax - vmin) * pad_ratio, min_pad)

    low = vmin - pad
    high = vmax + pad

    if floor_at_zero and low < 0 <= vmin:
        low = 0

    return [low, high]


# =====================================================
# TAB 1 — RINGKASAN PERFORMA PEMASARAN
# =====================================================
def revenue_trend(df):
    temp = (
        df.groupby(["year_month", "month_label"], as_index=False)["total_revenue"]
        .sum()
        .sort_values("year_month")
    )
    temp["revenue_m"] = temp["total_revenue"] / MILIAR
    month_order = temp["month_label"].tolist()

    fig = px.area(
        temp, x="month_label", y="revenue_m", markers=True,
        category_orders={"month_label": month_order},
    )

    fig.update_traces(
        line=dict(color=COLOR_REVENUE, width=2.6),
        marker=dict(color=COLOR_REVENUE, size=6),
        fillcolor="rgba(74,46,35,0.13)",
        hovertemplate="<b>%{x}</b><br>Revenue: Rp %{y:,.2f} Miliar<extra></extra>",
    )

    fig.update_layout(
        xaxis_title="", yaxis_title=_rev_axis_title(),
        hovermode="x unified",
        xaxis=dict(tickangle=-45),
    )

    return _base(fig)


def top_selling_category(df):
    temp = (
        df.groupby("top_selling_category", as_index=False)["total_revenue"]
        .sum()
        .sort_values("total_revenue", ascending=True)
    )
    temp["revenue_m"] = temp["total_revenue"] / MILIAR

    fig = px.bar(temp, x="revenue_m", y="top_selling_category", orientation="h")

    fig.update_traces(
        texttemplate="%{x:.1f} M",
        textposition="outside",
        hovertemplate="<b>%{y}</b><br>Revenue: Rp %{x:,.2f} Miliar<extra></extra>"
    )

    fig = _single_bar(fig, COLOR_CATEGORY)
    fig.update_layout(
        xaxis_title="Revenue (Miliar Rp)",
        yaxis_title="",
        # FIX: range dihitung dari data ter-filter, bukan angka tetap
        xaxis_range=_dynamic_range(temp["revenue_m"]),
        margin=dict(
            l=0,
            r=80,
            t=15,
            b=40
        ),
        yaxis=dict(
            automargin=True,
            ticklabelstandoff=4
        )
    )
    return fig

def city_contribution(df):
    temp = (
        df.groupby("branch_city", as_index=False)["total_revenue"]
        .sum()
        .sort_values("total_revenue", ascending=False)
    )

    fig = px.pie(
        temp, names="branch_city", values="total_revenue", hole=0.62,
        color_discrete_sequence=QUALITATIVE,
    )

    fig.update_traces(
        hovertemplate="<b>%{label}</b><br>Revenue: Rp %{value:,.0f}<extra></extra>",
    )

    return _donut(fig)


# =====================================================
# TAB 2 — EFEKTIVITAS PROMOSI
# =====================================================
def promo_revenue(df):
    """
    Chart 'Revenue per Jenis Promo'.

    FIX: xaxis_range sebelumnya di-hardcode (mis. [9.0, 12.5]) berdasarkan
    rentang nilai data TANPA filter. Begitu user apply filter (kota/tahun/
    tipe cabang dll), total revenue per promo bisa jauh lebih kecil dari
    9.0 Miliar, sehingga bar keluar dari rentang sumbu dan JADI TIDAK
    TERLIHAT SAMA SEKALI walau datanya ada. Sekarang range dihitung dinamis
    dari data yang sudah difilter (temp["revenue_m"]).
    """
    temp = (
        df[df["promo_active"]]
        .groupby("promo_type", as_index=False)["total_revenue"]
        .sum()
        .sort_values("total_revenue", ascending=True)
    )
    temp["revenue_m"] = temp["total_revenue"] / MILIAR

    fig = px.bar(temp, x="revenue_m", y="promo_type", orientation="h")

    fig.update_traces(
        texttemplate="%{x:.1f} M",
        textposition="outside",
        hovertemplate="<b>%{y}</b><br>Revenue: Rp %{x:,.2f} Miliar<extra></extra>"
    )

    fig = _single_bar(fig, COLOR_PROMO)

    fig.update_layout(
        xaxis_title="Revenue (Miliar Rp)",
        yaxis_title="",
        # FIX: dinamis, bukan hardcode [9.0, 12.5]
        xaxis_range=_dynamic_range(temp["revenue_m"]),
        margin=dict(
            l=0,
            r=45,
            t=15,
            b=40
        ),
        yaxis=dict(
            automargin=True,
            ticklabelstandoff=4,
            categoryorder="array",
            categoryarray=temp["promo_type"].tolist()
        )
    )
    return fig


def promo_trend(df):
    temp = (
        df[df["promo_active"]]
        .groupby(["year", "promo_type"], as_index=False)["total_revenue"]
        .sum()
        .sort_values("year")
    )
    temp["revenue_m"] = temp["total_revenue"] / MILIAR
    temp["year"] = temp["year"].astype(str)

    fig = px.bar(
        temp, x="year", y="revenue_m", color="promo_type",
        barmode="group", color_discrete_sequence=QUALITATIVE,
    )

    fig.update_layout(
        legend=dict(
            orientation="h",
            y=1.28,
            x=0,
            font=dict(size=10),
            itemwidth=30
        ),
        margin=dict(
            t=90,
            l=55,
            r=25
        )
    )
    fig.update_traces(
        hovertemplate="<b>%{x}</b><br>Rp %{y:,.2f} Miliar<extra></extra>",
    )

    return _multi_bar(fig)


def promo_vs_category(df):
    temp = (
        df[df["promo_active"]]
        .groupby(["top_selling_category", "promo_type"], as_index=False)["total_revenue"]
        .sum()
    )
    temp["revenue_m"] = temp["total_revenue"] / MILIAR

    fig = px.bar(
        temp, x="top_selling_category", y="revenue_m", color="promo_type",
        barmode="group", color_discrete_sequence=QUALITATIVE,
    )

    fig.update_layout(xaxis_title="", yaxis_title=_rev_axis_title(), legend_title="")
    fig.update_traces(
        hovertemplate="<b>%{x}</b><br>Rp %{y:,.2f} Miliar<extra></extra>",
    )

    return _multi_bar(fig)


# =====================================================
# TAB 3 — PREFERENSI CHANNEL & PERILAKU PELANGGAN
# =====================================================
def customer_channel(df):
    temp = go_channel_df(df)

    fig = px.pie(
        temp, names="Channel", values="Persentase", hole=0.62,
        color_discrete_sequence=[COLOR_CUSTOMER, "#7BC4B4", "#C7E4DC"],
    )

    fig.update_layout(
        margin=dict(l=40, r=40, t=35, b=20),
        uniformtext_minsize=10,
        uniformtext_mode="hide",
        showlegend=False,
        piecolorway=[COLOR_CUSTOMER, "#7BC4B4", "#C7E4DC"]
    )

    fig.update_traces(
        textposition="outside",
        automargin=True,
        pull=[0, 0, 0],
        sort=False,
        rotation=90
    )

    fig.update_layout(
        width=None,
    )

    return _donut(fig)


def go_channel_df(df):
    import pandas as pd
    return pd.DataFrame({
        "Channel": ["Dine In", "Delivery", "Take Away"],
        "Persentase": [
            df["dine_in_percent"].mean(),
            df["delivery_percent"].mean(),
            df["takeaway_percent"].mean(),
        ],
    })


def channel_by_city(df):
    temp = (
        df.groupby("branch_city")[["dine_in_percent", "delivery_percent", "takeaway_percent"]]
        .mean()
        .reset_index()
        .rename(columns={
            "dine_in_percent": "Dine In",
            "delivery_percent": "Delivery",
            "takeaway_percent": "Take Away",
        })
    )

    temp = temp.melt(id_vars="branch_city", var_name="Channel", value_name="Persentase")

    fig = px.bar(
        temp, x="branch_city", y="Persentase", color="Channel",
        barmode="group", color_discrete_sequence=[COLOR_CUSTOMER, "#7BC4B4", "#C7E4DC"],
    )

    fig.update_layout(xaxis_title="", yaxis_title="% Transaksi", legend_title="")
    fig.update_traces(hovertemplate="<b>%{x}</b><br>%{y:.1f}%<extra></extra>")

    return _multi_bar(fig)


def weekend_vs_weekday(df):
    temp = df.groupby("is_weekend", as_index=False)["total_revenue"].mean()
    temp["Hari"] = temp["is_weekend"].map({False: "Weekday", True: "Weekend"})
    temp = temp.sort_values("is_weekend")
    temp["revenue_jt"] = temp["total_revenue"] / 1_000_000
    ymin = temp["revenue_jt"].min()
    ymax = temp["revenue_jt"].max()

    padding = (ymax - ymin) * 0.4

    if padding < 0.05:
        padding = 0.05

    fig = px.bar(temp, x="Hari", y="revenue_jt")

    fig.update_traces(
        hovertemplate="<b>%{x}</b><br>Rata-rata Revenue: Rp %{y:,.2f} Juta<extra></extra>",
        texttemplate="%{y:.2f} Jt",
        textposition="outside",
    )
    fig.update_layout(
        yaxis=dict(
            title="Revenue (Juta Rp)",
            range=[
                ymin - padding,
                ymax + padding
            ]
        )
    )

    return _single_bar(fig, COLOR_CUSTOMER)


# =====================================================
# TAB 4 — PELUANG PASAR & SEGMENTASI
# =====================================================
def category_by_city(df):
    temp = (
        df.groupby(["branch_city", "top_selling_category"], as_index=False)["total_revenue"]
        .sum()
    )

    city_total = temp.groupby("branch_city")["total_revenue"].transform("sum")
    temp["share"] = temp["total_revenue"] / city_total * 100

    order = (
        df.groupby("branch_city")["total_revenue"].sum()
        .sort_values(ascending=False).index.tolist()
    )

    fig = px.bar(
        temp, x="branch_city", y="share", color="top_selling_category",
        barmode="stack", color_discrete_sequence=QUALITATIVE,
        category_orders={"branch_city": order},
    )

    fig.update_layout(xaxis_title="", yaxis_title="% Revenue per Kategori", legend_title="")
    fig.update_traces(hovertemplate="<b>%{x}</b><br>%{fullData.name}: %{y:.1f}%<extra></extra>")

    return _multi_bar(fig)


def promo_by_city(df):
    temp = (
        df[df["promo_active"]]
        .groupby(["branch_city", "promo_type"], as_index=False)["total_revenue"]
        .sum()
    )
    temp["revenue_m"] = temp["total_revenue"] / MILIAR

    fig = px.bar(
        temp, x="branch_city", y="revenue_m", color="promo_type",
        barmode="group", color_discrete_sequence=QUALITATIVE,
    )

    fig.update_layout(xaxis_title="", yaxis_title=_rev_axis_title(), legend_title="")
    fig.update_traces(hovertemplate="<b>%{x}</b><br>Rp %{y:,.2f} Miliar<extra></extra>")

    return _multi_bar(fig)


def satisfaction_by_city(df):
    """
    FIX: xaxis_range sebelumnya di-hardcode [3.75, 3.89] berdasarkan rentang
    skor kepuasan TANPA filter. Kalau filter membuat skor kepuasan di luar
    rentang sempit itu (atau cuma 1 kota tersisa), bar bisa hilang atau
    tampak 'penuh'/terpotong. Sekarang range dihitung dinamis dari data
    yang sudah difilter.
    """
    temp = (
        df.groupby("branch_city", as_index=False)["customer_satisfaction"]
        .mean()
        .sort_values("customer_satisfaction", ascending=True)
    )

    fig = px.bar(temp, x="customer_satisfaction", y="branch_city", orientation="h")

    fig.update_traces(
        texttemplate="%{x:.2f}",
        textposition="outside",
        hovertemplate="<b>%{y}</b><br>Kepuasan: %{x:.2f}/5<extra></extra>",
    )

    fig = _single_bar(fig, COLOR_REVENUE)

    fig.update_layout(
        xaxis_title="",
        yaxis_title="",
        # FIX: dinamis, bukan hardcode [3.75, 3.89]. Skala 0-5 diberi floor
        # supaya bar tetap proporsional & tidak melebihi skala penilaian asli.
        xaxis_range=_dynamic_range(temp["customer_satisfaction"], pad_ratio=0.6, min_pad=0.1),
        margin=dict(
            l=0,
            r=45,
            t=15,
            b=25
        ),
        yaxis=dict(
            automargin=True,
            ticklabelstandoff=4,
            categoryorder="array",
            categoryarray=temp["branch_city"].tolist()
        )
    )
    return fig