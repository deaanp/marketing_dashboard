import streamlit as st
from utils.theme import ACCENTS

_ICON_BODY = {

    "overview": '<path d="M3 17V13M9 17V9M15 17V5M21 17V11" stroke-linecap="round" stroke-linejoin="round"/>',

    "satisfaction": '<path d="M12 3l2.5 5.2 5.7.8-4.1 4 1 5.7L12 16l-5.1 2.7 1-5.7-4.1-4 5.7-.8L12 3z" stroke-linejoin="round"/>',

    "percent": '<circle cx="7" cy="7" r="2.3"/><circle cx="17" cy="17" r="2.3"/><path d="M18 6L6 18" stroke-linecap="round"/>',

    "category": '<path d="M12 3l8 4.5v9L12 21l-8-4.5v-9L12 3z" stroke-linejoin="round"/><path d="M12 3v18M4 7.5l8 4.5 8-4.5" stroke-linejoin="round"/>',

    "gift": '<rect x="3" y="9" width="18" height="4" rx="1"/><rect x="5" y="13" width="14" height="8" rx="1"/><path d="M12 9v12M12 9c-1.6-3.2-6-3.5-6-.7C6 9.6 8 9 12 9zm0 0c1.6-3.2 6-3.5 6-.7 0 1.3-2 .7-6 .7z" stroke-linejoin="round"/>',

    "trend": '<path d="M4 16l5.2-5.6L13 14l6.5-7" stroke-linecap="round" stroke-linejoin="round"/><path d="M15 6.5h4.5V11" stroke-linecap="round" stroke-linejoin="round"/>',

    "users": '<circle cx="9" cy="8" r="3"/><path d="M3.5 19c0-3.3 2.5-5.5 5.5-5.5s5.5 2.2 5.5 5.5" stroke-linecap="round"/><circle cx="17.3" cy="9" r="2.4"/><path d="M15.5 13.7c2.5.3 4.3 2.2 4.3 5.3" stroke-linecap="round"/>',

    "calendar": '<rect x="3.5" y="5" width="17" height="15" rx="2"/><path d="M3.5 9.5h17M8 3v3.5M16 3v3.5" stroke-linecap="round"/>',

    "map": '<path d="M12 21s6.5-6.1 6.5-11A6.5 6.5 0 105.5 10c0 4.9 6.5 11 6.5 11z" stroke-linejoin="round"/><circle cx="12" cy="10" r="2.3"/>',

    "layers": '<path d="M12 3l8 4.5-8 4.5-8-4.5L12 3z" stroke-linejoin="round"/><path d="M4 12l8 4.5 8-4.5M4 16.5L12 21l8-4.5" stroke-linejoin="round"/>',

    "target": '<circle cx="12" cy="12" r="8"/><circle cx="12" cy="12" r="4.2"/><circle cx="12" cy="12" r="0.6" fill="currentColor"/>',

    "clock": '<circle cx="12" cy="12" r="8.3"/><path d="M12 7.5V12l3.2 2" stroke-linecap="round" stroke-linejoin="round"/>',

    "cup": '<path d="M5 9h11v6a5 5 0 01-5 5H9a4 4 0 01-4-4V9z" stroke-linejoin="round"/><path d="M16 10.5h1.6a2.4 2.4 0 010 4.8H16" stroke-linejoin="round"/><path d="M8.5 6c-.4-.9.2-1.4.4-2M12 6c-.4-.9.2-1.4.4-2" stroke-linecap="round"/>',

    "cloud": '<path d="M7 18h10.5a3.5 3.5 0 000-7 5.5 5.5 0 00-10.6-1.7A4 4 0 007 18z" stroke-linejoin="round"/>',
}


def icon(name, size=18, color="currentColor"):
    body = _ICON_BODY.get(name, _ICON_BODY["overview"])
    return (
        f'<svg width="{size}" height="{size}" viewBox="0 0 24 24" '
        f'fill="none" stroke="{color}" stroke-width="1.7">{body}</svg>'
    )

def _accent(key):
    return ACCENTS.get(key, ACCENTS["revenue"])

def section_header(title, subtitle, icon_name, accent_key="revenue"):
    color, tint = _accent(accent_key)

    html = (
        '<div class="section-head">'
        f'<div class="section-head-icon" style="color:{color};background:{tint};">'
        f'{icon(icon_name, size=17)}'
        '</div>'
        '<div>'
        f'<div class="section-head-title">{title}</div>'
        f'<div class="section-head-sub">{subtitle}</div>'
        '</div>'
        '</div>'
    )

    st.markdown(html, unsafe_allow_html=True)


def metric_row(items):
    """items: list of dict(label, value, sub, icon, color) — color pakai
    salah satu key: revenue / promo / customer / category."""

    card_html_list = []

    for it in items:
        color, tint = _accent(it.get("color", "revenue"))

        card = (
            '<div class="kpi-card">'
            f'<div class="kpi-icon" style="color:{color};background:{tint};">'
            f'{icon(it["icon"], size=16)}'
            '</div>'
            '<div class="kpi-text">'
            f'<div class="kpi-label">{it["label"]}</div>'
            f'<div class="kpi-value">{it["value"]}</div>'
            f'<div class="kpi-sub">{it.get("sub", "")}</div>'
            '</div>'
            '</div>'
        )

        card_html_list.append(card)

    html = '<div class="kpi-row">' + "".join(card_html_list) + '</div>'

    st.markdown(html, unsafe_allow_html=True)
