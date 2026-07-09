import pandas as pd
import streamlit as st

CATEGORY_MAP = {
    "non-coffee": "Non-Coffee",
    "non coffee": "Non-Coffee",
    "noncoffee": "Non-Coffee",
    "espresso based": "Espresso Based",
    "espreso based": "Espresso Based",
    "kopi susu": "Kopi Susu",
    "tea": "Tea",
    "teh": "Tea",
    "snack & pastry": "Snack & Pastry",
    "snack and pastry": "Snack & Pastry",
}

@st.cache_data
def load_data():

    df = pd.read_csv("data/kopiseru_clean_final.csv")

    # ======================================
    # Date
    # ======================================
    df["date"] = pd.to_datetime(df["date"])
    df["year"] = df["date"].dt.year
    df["month"] = df["date"].dt.strftime("%b")
    df["month_num"] = df["date"].dt.month
    df["day"] = df["date"].dt.day
    df["month_label"] = df["date"].dt.strftime("%b %Y")
    df["year_month"] = df["year"] * 100 + df["month_num"]

    category_cols = [
        "branch_city",
        "branch_name",
        "promo_type",
        "weather",
        "top_selling_category",
        "branch_type",
    ]

    for col in category_cols:
        df[col] = df[col].astype("string").str.strip()

    df["top_selling_category"] = (
        df["top_selling_category"]
        .str.lower()
        .map(CATEGORY_MAP)
        .fillna(df["top_selling_category"])
    )

    df["branch_city"] = df["branch_city"].str.title()
    df["promo_type"] = df["promo_type"].str.title()

    df["promo_active"] = df["promo_active"].astype(bool)
    df["is_weekend"] = df["is_weekend"].astype(bool)

    return df
