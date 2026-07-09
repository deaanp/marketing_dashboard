# =====================================================
# BRAND COLOR SYSTEM
# =====================================================
ESPRESSO = "#4A2E23"
CARAMEL = "#E08A3C"
TEAL = "#2F8F7A"
TERRACOTTA = "#C1666B"
GOLD = "#E4B363"
SLATE = "#7A6F63"

BACKGROUND = "#FAF7F3"
CARD = "#FFFFFF"
BORDER = "#EAE0D4"
TEXT = "#2B211D"
SUBTEXT = "#8A7B6C"
GRID = "#EFE7DC"

QUALITATIVE = [ESPRESSO, CARAMEL, TEAL, TERRACOTTA, GOLD, SLATE]

COLOR_REVENUE = ESPRESSO
COLOR_PROMO = CARAMEL
COLOR_CUSTOMER = TEAL
COLOR_CATEGORY = TERRACOTTA

ACCENTS = {
    "revenue": (ESPRESSO, f"{ESPRESSO}1F"),
    "promo": (CARAMEL, f"{CARAMEL}1F"),
    "customer": (TEAL, f"{TEAL}1F"),
    "category": (TERRACOTTA, f"{TERRACOTTA}1F"),
}

FONT_FAMILY = "Inter, -apple-system, Segoe UI, sans-serif"

PLOTLY_LAYOUT = dict(
    template="simple_white",
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(family=FONT_FAMILY, color=TEXT, size=12),
    hoverlabel=dict(bgcolor=CARD, font_size=12, font_family=FONT_FAMILY,
                     bordercolor=BORDER),
    legend=dict(
        orientation="h",
        yanchor="bottom", y=1.03,
        xanchor="left", x=0,
        font=dict(size=10, color=SUBTEXT),
        title=None,
        itemsizing="constant",
        tracegroupgap=2,
    ),
    xaxis=dict(showgrid=False, zeroline=False, showline=True,
               linecolor=BORDER, tickfont=dict(color=SUBTEXT, size=11)),
    yaxis=dict(showgrid=True, gridcolor=GRID, zeroline=False,
               showline=False, tickfont=dict(color=SUBTEXT, size=11)),
)


def fmt_compact(value, prefix=""):
    v = float(value)
    sign = "-" if v < 0 else ""
    v = abs(v)
    if v >= 1_000_000_000:
        return f"{sign}{prefix}{v/1_000_000_000:,.2f} M"
    if v >= 1_000_000:
        return f"{sign}{prefix}{v/1_000_000:,.1f} Jt"
    if v >= 1_000:
        return f"{sign}{prefix}{v/1_000:,.1f} Rb"
    return f"{sign}{prefix}{v:,.0f}"


def fmt_rupiah(value):
    return fmt_compact(value, prefix="Rp ")
