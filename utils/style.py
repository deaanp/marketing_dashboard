import streamlit as st


def load_css():

    st.markdown("""
    <style>

    /* ==========================================================
                            GOOGLE FONT
    ========================================================== */

    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

    html, body, [class*="css"]{
        font-family:'Inter', sans-serif;
    }

    /* ==========================================================
                            COLOR SYSTEM
    ========================================================== */

    :root{

        --primary:#4A2E23;
        --c-revenue:#4A2E23;
        --c-promo:#E08A3C;
        --c-customer:#2F8F7A;
        --c-category:#C1666B;

        --background:#FAF7F3;
        --card:#FFFFFF;
        --border:#EAE0D4;

        --text:#2B211D;
        --subtext:#8A7B6C;
    }

    /* ==========================================================
                            PAGE / NO SCROLL
    ========================================================== */

    .stApp{ background:var(--background); }

    .block-container{
        padding-top:0.9rem;
        padding-bottom:0.6rem;
        padding-left:1.8rem;
        padding-right:1.8rem;
        max-width:1500px;
    }

    div[data-testid="stVerticalBlockBorderWrapper"]{ gap:0.5rem; }

    section[data-testid="stSidebar"]{ display:none; }
                
    svg{ display:block; }

    /* ==========================================================
                                HEADER
       ========================================================== */

    .app-header{
        display:flex;
        align-items:center;
        gap:12px;
        margin-bottom:2px;
    }

    .app-header .mark{
        width:38px;
        height:38px;
        border-radius:10px;
        background:var(--primary);
        display:flex;
        align-items:center;
        justify-content:center;
        color:#fff;
        font-weight:700;
        font-size:16px;
        flex-shrink:0;
    }

    .app-header h1{
        color:var(--text);
        font-size:22px;
        font-weight:700;
        margin:0;
        line-height:1.1;
    }

    .app-header .subtitle{
        color:var(--subtext);
        font-size:12.5px;
        margin-top: -2px !important;
        margin-bottom: 0;
    }

    /* ==========================================================
                            SECTION HEADER (per tab)
    ========================================================== */

    .section-head{
        display:flex;
        align-items:center;
        gap:10px;
        margin: 4px 0 10px 0;
    }

    .section-head-icon{
        width:30px;
        height:30px;
        border-radius:8px;
        display:flex;
        align-items:center;
        justify-content:center;
        flex-shrink:0;
    }

    .section-head-title{
        color:var(--text);
        font-size:15.5px;
        font-weight:700;
        line-height:1.2;
    }

    .section-head-sub{
        color:var(--subtext);
        font-size:12px;
        line-height:1.3;
    }

    /* ==========================================================
                            KPI CARD ROW
    ========================================================== */

    .kpi-row{
        display:grid;
        grid-template-columns:repeat(4, 1fr);
        gap:12px;
        margin-bottom:10px;
    }

    .kpi-card{
        background:var(--card);
        border:1px solid var(--border);
        border-radius:12px;
        padding:12px 14px;
        display:flex;
        align-items:center;
        gap:10px;
        box-shadow:0 1px 4px rgba(74,46,35,.04);
    }

    .kpi-icon{
        width:30px;
        height:30px;
        border-radius:8px;
        display:flex;
        align-items:center;
        justify-content:center;
        flex-shrink:0;
    }

    .kpi-label{
        color:var(--subtext);
        font-size:11.5px;
        font-weight:600;
        text-transform:uppercase;
        letter-spacing:.02em;
        margin-bottom:2px;
    }

    .kpi-value{
        color:var(--text);
        font-size:19px;
        font-weight:700;
        line-height:1.2;
    }

    .kpi-sub{
        color:var(--subtext);
        font-size:11px;
        margin-top:1px;
    }

    /* ==========================================================
                            CHART CARD
    ========================================================== */

    div[data-testid="stVerticalBlock"] > div:has(> div > div[data-testid="stPlotlyChart"]){
        background:var(--card);
        border:1px solid var(--border);
        border-radius:14px;
        padding:12px 14px 6px 14px;
        box-shadow:0 1px 4px rgba(74,46,35,.04);
    }

    
    /* ==========================================================
                            FILTER BAR
    ========================================================== */

    div[data-testid="stVerticalBlockBorderWrapper"]:has(div[data-baseweb="select"]){
        padding: 2px 10px 2px 10px !important;
        margin-bottom: -22px !important;
    }

    div[data-testid="stVerticalBlockBorderWrapper"]:has(div[data-baseweb="select"]) 
        div[data-testid="stVerticalBlock"]{
        gap: 0rem !important;
    }
    div[data-testid="stHorizontalBlock"]{ 
        gap: 0.5rem !important; 
    }

    div[data-testid="stVerticalBlockBorderWrapper"]:has(div[data-baseweb="select"]) label {
        display: none !important;
    }

    div[data-baseweb="select"] > div{
        border-radius: 5px !important;
        border-color: var(--border) !important;
        min-height: 24px !important;
        height: 24px !important;
    }

    div[data-baseweb="select"] div[data-testid="stMarkdownContainer"] p {
        font-size: 11px !important;
        line-height: 24px !important; 
        margin: 0 !important;
        padding: 0 !important;
    }

    div[data-baseweb="select"] svg {
        width: 14px !important;
        height: 14px !important;
    }

    div[data-baseweb="select"] > div > div {
        padding-top: 0px !important;
        padding-bottom: 0px !important;
        padding-left: 6px !important;
        padding-right: 4px !important;
    }

    /* ==========================================================
                            TABS
    ========================================================== */

    div[data-testid="stTabs"]{ margin-top:4px; }

    button[data-baseweb="tab"]{
        font-weight:600;
        font-size:13.5px;
        color:var(--subtext);
        padding:8px 16px;
        border-radius:9px 9px 0 0;
    }

    button[data-baseweb="tab"][aria-selected="true"]{
        color:var(--primary);
        background:#EFE4D6;
    }

    div[data-baseweb="tab-highlight"]{ background:var(--primary); }
    div[data-baseweb="tab-border"]{ background:var(--border); }

    /* ==========================================================
                            MISC
    ========================================================== */

    div[data-testid="stAlert"]{ border-radius:12px; border:none; }

    hr{ border:none; border-top:1px solid var(--border); margin:8px 0; }

    #MainMenu, footer, header{ visibility:hidden; height:0; }

    ::-webkit-scrollbar{ width:8px; height:8px; }
    ::-webkit-scrollbar-thumb{ background:#D8C6B4; border-radius:8px; }

    /* Tab strip: kalau ada banyak tab & layar sempit, scroll ke samping
       daripada teks tab saling bertabrakan/terpotong. */
    div[data-baseweb="tab-list"]{
        overflow-x:auto;
        overflow-y:hidden;
        flex-wrap:nowrap;
        scrollbar-width:none;
    }
    div[data-baseweb="tab-list"]::-webkit-scrollbar{ display:none; }

    /* ==========================================================
       RESPONSIF — TABLET (laptop kecil, iPad, dsb)
       Chart & filter Streamlit sendiri sudah otomatis susun ulang
       (stack) di layar sempit; bagian ini menyesuaikan elemen HTML
       custom (KPI card, header, filter) supaya ikut menyesuaikan.
    ========================================================== */

    @media (max-width: 1100px){

        .block-container{
            padding-left:1.1rem;
            padding-right:1.1rem;
        }

        .kpi-row{
            grid-template-columns:repeat(2, 1fr);
        }
    }

    /* ==========================================================
       RESPONSIF — HANDPHONE
    ========================================================== */

    @media (max-width: 640px){

        .block-container{
            padding-top:0.6rem;
            padding-left:0.7rem;
            padding-right:0.7rem;
        }

        /* Header brand */
        .app-header{ gap:9px; }
        .app-header .mark{ width:32px; height:32px; border-radius:9px; }
        .app-header h1{ font-size:17px; line-height:1.25; }
        .app-header .subtitle{ font-size:11.5px; }

        /* Section header per tab */
        .section-head{ align-items:flex-start; }
        .section-head-icon{ width:26px; height:26px; }
        .section-head-title{ font-size:14px; }
        .section-head-sub{ font-size:11px; }

        /* KPI card: 1 kolom penuh, lebih mudah dibaca sambil scroll */
        .kpi-row{
            grid-template-columns:1fr;
            gap:8px;
        }
        .kpi-value{ font-size:17px; }

        /* Chart card: rapatkan sedikit padding di layar sempit */
        div[data-testid="stVerticalBlock"] > div:has(> div > div[data-testid="stPlotlyChart"]){
            padding:10px 10px 4px 10px;
        }

        /* Filter: kembalikan label & perbesar target tap supaya nyaman
           disentuh jari, dan filter (yang di HP tersusun vertikal
           satu per satu) tetap jelas mana Tahun/Kota/Promo/dst. */
        div[data-testid="stVerticalBlockBorderWrapper"]:has(div[data-baseweb="select"]){
            margin-bottom:8px !important;
            padding:10px 12px !important;
        }
        div[data-testid="stVerticalBlockBorderWrapper"]:has(div[data-baseweb="select"])
            div[data-testid="stVerticalBlock"]{
            gap:0.5rem !important;
        }
        div[data-testid="stVerticalBlockBorderWrapper"]:has(div[data-baseweb="select"]) label{
            display:block !important;
            font-size:10.5px !important;
        }
        div[data-baseweb="select"] > div{
            min-height:38px !important;
            height:38px !important;
        }
        div[data-baseweb="select"] div[data-testid="stMarkdownContainer"] p{
            font-size:13px !important;
            line-height:38px !important;
        }
        div[data-baseweb="select"] svg{
            width:16px !important;
            height:16px !important;
        }

        /* Tab: teks & padding lebih kecil supaya ke-4 tab tetap muat
           berdampingan / mudah discroll di layar sempit. */
        button[data-baseweb="tab"]{
            font-size:12px;
            padding:7px 11px;
        }
    }

    </style>
    """, unsafe_allow_html=True)
