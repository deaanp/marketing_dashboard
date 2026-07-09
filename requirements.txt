# KopiSeru Marketing Dashboard

Dashboard analitik internal untuk tim **Marketing** KopiSeru — dibangun dengan
[Streamlit](https://streamlit.io), [Plotly](https://plotly.com/python/), dan
[pandas](https://pandas.pydata.org/). 

## Fitur
- **Ringkasan Pemasaran** — trend revenue, kategori produk terlaris, kontribusi tiap kota
- **Efektivitas Promosi** — performa tiap jenis promo, tren tahunan, dampaknya ke kategori produk
- **Perilaku Pelanggan** — komposisi sales channel, pola weekday vs weekend
- **Peluang Pasar** — komposisi kategori per kota, promo per kota, kepuasan pelanggan per kota
- Filter interaktif: Tahun, Kota, Promo, Kategori, Tipe Cabang

## Prasyarat

- **Python 3.10 – 3.12** 
- `pip` untuk instalasi dependency
- Git (untuk clone repo)

## Instalasi

1. **Clone repository**

   ```bash
   git clone <url-repo-anda>
   cd <nama-folder-repo>
   ```

2. **Install dependency**

   ```bash
   pip install -r requirements.txt
   ```

## Menjalankan Dashboard

```bash
streamlit run app.py
```

Setelah berjalan, buka `http://localhost:8501` di browser.

Untuk menjalankan di port lain:

```bash
streamlit run app.py --server.port 8502
```

## Struktur Project

```
dashboard/
├── app.py
├── requirements.txt
├── data/
│   └── kopiseru_clean_final.csv
├── .streamlit/
│   └── config.toml
└── utils/
    ├── load_data.py
    ├── filters.py
    ├── charts.py
    ├── kpi.py
    ├── icons.py
    ├── theme.py
    └── style.py
```