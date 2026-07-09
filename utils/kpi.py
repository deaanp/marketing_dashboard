from utils.theme import fmt_compact, fmt_rupiah


def overview_kpis(df):

    total_transaksi = df["total_transactions"].sum()

    avg_satisfaction = df["customer_satisfaction"].mean()

    promo_revenue = df.loc[df["promo_active"], "total_revenue"].sum()
    total_revenue = df["total_revenue"].sum()
    promo_share = (promo_revenue / total_revenue * 100) if total_revenue else 0

    top_category = (
        df.groupby("top_selling_category")["total_revenue"].sum().idxmax()
    )

    return [
        dict(label="Total Transaksi", value=fmt_compact(total_transaksi),
             sub="Volume interaksi pelanggan", icon="users", color="revenue"),
        dict(label="Kepuasan Pelanggan", value=f"{avg_satisfaction:.2f} / 5",
             sub="Rata-rata seluruh cabang", icon="satisfaction", color="customer"),
        dict(label="Kontribusi Revenue Promo", value=f"{promo_share:.1f}%",
             sub="Dari total revenue", icon="percent", color="promo"),
        dict(label="Kategori Terlaris", value=top_category,
             sub="Berdasarkan revenue", icon="category", color="category"),
    ]


def promo_kpis(df):

    promo_df = df[df["promo_active"]]

    transaksi_promo = promo_df["total_transactions"].sum()
    revenue_promo = promo_df["total_revenue"].sum()

    ticket_promo = promo_df["avg_ticket_size"].mean()
    ticket_non_promo = df.loc[~df["promo_active"], "avg_ticket_size"].mean()
    uplift = ((ticket_promo - ticket_non_promo) / ticket_non_promo * 100) if ticket_non_promo else 0

    if abs(uplift) < 0.05:
        uplift_sub = "Pertumbuhan stagnan."
    else:
        uplift_sub = "Promo vs non-promo"

    promo_terpopuler = (
        promo_df.groupby("promo_type")["total_transactions"].sum().idxmax()
    )

    return [
        dict(label="Transaksi via Promo", value=fmt_compact(transaksi_promo),
             sub="Total transaksi berpromo", icon="gift", color="promo"),
        dict(label="Revenue dari Promo", value=fmt_rupiah(revenue_promo),
             sub="Total kontribusi promo", icon="trend", color="promo"),
        dict(label="Uplift Ticket Size", value=f"{uplift:+.2f}%",
             sub=uplift_sub, icon="percent", color="customer"),
        dict(label="Promo Terpopuler", value=promo_terpopuler,
             sub="Transaksi terbanyak", icon="target", color="category"),
    ]


def behavior_kpis(df):

    dine_in = df["dine_in_percent"].mean()
    delivery = df["delivery_percent"].mean()
    takeaway = df["takeaway_percent"].mean()

    channel_map = {"Dine In": dine_in, "Delivery": delivery, "Take Away": takeaway}
    dominant_channel = max(channel_map, key=channel_map.get)

    weekday_avg = df.loc[~df["is_weekend"], "total_revenue"].mean()
    weekend_avg = df.loc[df["is_weekend"], "total_revenue"].mean()
    weekend_uplift = ((weekend_avg - weekday_avg) / weekday_avg * 100) if weekday_avg else 0

    top_delivery_city = (
        df.groupby("branch_city")["delivery_percent"].mean().idxmax()
    )

    channel_cols = {
        "Dine In": "dine_in_percent",
        "Delivery": "delivery_percent",
        "Take Away": "takeaway_percent",
    }
    weekday_mix = df.loc[~df["is_weekend"], list(channel_cols.values())].mean()
    weekend_mix = df.loc[df["is_weekend"], list(channel_cols.values())].mean()
    shift = weekend_mix - weekday_mix
    shift.index = list(channel_cols.keys())
    top_shift_channel = shift.abs().idxmax()
    top_shift_value = shift[top_shift_channel]

    return [
        dict(label="Channel Dominan", value=dominant_channel,
             sub=f"{channel_map[dominant_channel]:.1f}% dari transaksi",
             icon="users", color="customer"),
        dict(label="Selisih Revenue Weekend", value=f"{weekend_uplift:+.1f}%",
             sub="Dibanding rata-rata weekday", icon="calendar", color="revenue"),
        dict(label="Channel Paling Bergeser di Weekend", value=top_shift_channel,
             sub=f"menyusut {top_shift_value:+.1f} poin dibanding weekday",
             icon="trend", color="category"),
        dict(label="Kota Delivery Tertinggi", value=top_delivery_city,
             sub="Rata-rata persentase delivery", icon="map", color="promo"),
    ]

def opportunity_kpis(df):

    city_stats = (
        df.groupby("branch_city")
        .agg(revenue=("total_revenue", "sum"),
             satisfaction=("customer_satisfaction", "mean"))
        .reset_index()
    )

    top_city = city_stats.loc[city_stats["revenue"].idxmax(), "branch_city"]
    top_city_revenue = city_stats["revenue"].max()

    most_loyal_city = city_stats.loc[city_stats["satisfaction"].idxmax(), "branch_city"]
    most_loyal_score = city_stats["satisfaction"].max()

    promo_df = df[df["promo_active"]]
    best_promo = promo_df.groupby("promo_type")["total_revenue"].sum().idxmax()

    city_stats["revenue_rank"] = city_stats["revenue"].rank(ascending=False)
    city_stats["satisfaction_rank"] = city_stats["satisfaction"].rank(ascending=False)
    city_stats["opportunity_gap"] = city_stats["revenue_rank"] - city_stats["satisfaction_rank"]

    best_opportunity = city_stats.sort_values("opportunity_gap", ascending=False).iloc[0]

    if len(city_stats) > 1:
        opportunity_sub = (
            f"Kepuasan #{int(best_opportunity['satisfaction_rank'])}, "
            f"revenue #{int(best_opportunity['revenue_rank'])} — belum maksimal"
        )
    else:
        opportunity_sub = "Perluas filter kota untuk lihat perbandingan"

    return [
        dict(label="Kota Revenue Tertinggi", value=top_city,
             sub=fmt_rupiah(top_city_revenue), icon="map", color="revenue"),
        dict(label="Kota Paling Loyal", value=most_loyal_city,
             sub=f"Kepuasan {most_loyal_score:.2f} / 5", icon="satisfaction", color="category"),
        dict(label="Promo Paling Efektif", value=best_promo,
             sub="Revenue tertinggi lintas kota", icon="gift", color="promo"),
        dict(label="Peluang Ekspansi Tertinggi", value=best_opportunity["branch_city"],
             sub=opportunity_sub,
             icon="trend", color="customer"),
    ]
