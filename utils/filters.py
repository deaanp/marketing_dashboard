import streamlit as st


def top_filter(df):

    # ==========================================
    # FILTER CARD
    # ==========================================
    with st.container(border=True):

        col1, col2, col3, col4, col5 = st.columns(5)

        # ==========================
        # Tahun
        # ==========================
        with col1:

            year = st.selectbox(
                "Tahun",
                options=["Semua"] + sorted(df["year"].dropna().unique(), reverse=True),
                index=0
            )

        # ==========================
        # Kota
        # ==========================
        with col2:

            city = st.selectbox(
                "Kota",
                options=["Semua"] + sorted(df["branch_city"].dropna().unique()),
                index=0
            )

        # ==========================
        # Promo
        # ==========================
        with col3:

            promo = st.selectbox(
                "Promo",
                options=["Semua"] + sorted(df["promo_type"].dropna().unique()),
                index=0
            )

        # ==========================
        # Kategori
        # ==========================
        with col4:

            category = st.selectbox(
                "Kategori",
                options=["Semua"] + sorted(df["top_selling_category"].dropna().unique()),
                index=0
            )

        # ==========================
        # Tipe Cabang
        # ==========================
        with col5:

            branch_type = st.selectbox(
                "Tipe Cabang",
                options=["Semua"] + sorted(df["branch_type"].dropna().unique()),
                index=0
            )

    # ====================================================
    # FILTERING
    # ====================================================
    filtered_df = df.copy()

    if year != "Semua":
        filtered_df = filtered_df[
            filtered_df["year"] == year
        ]

    if city != "Semua":
        filtered_df = filtered_df[
            filtered_df["branch_city"] == city
        ]

    if promo != "Semua":
        filtered_df = filtered_df[
            filtered_df["promo_type"] == promo
        ]

    if category != "Semua":
        filtered_df = filtered_df[
            filtered_df["top_selling_category"] == category
        ]

    if branch_type != "Semua":
        filtered_df = filtered_df[
            filtered_df["branch_type"] == branch_type
        ]

    return filtered_df
