# ── Icones do projeto ────────────────────────────────────────────────

GRAPH_ICON = "https://img.icons8.com/fluency-systems-filled/24/58A6FF/combo-chart.png"
CYCLE_ICON = "https://img.icons8.com/fluency-systems-filled/24/58A6FF/refresh.png"
ORDER_ICON = "https://img.icons8.com/fluency-systems-filled/24/58A6FF/sorting-arrows-horizontal.png"
IMPACT_ICON = "https://img.icons8.com/fluency-systems-filled/24/58A6FF/high-importance.png"


def section_title(icon_url, title):
    return f"""
    <div style="
        display:flex;
        align-items:center;
        gap:10px;
        margin-bottom:1rem;
    ">
        <img src="{icon_url}" width="22">
        <h3 style="margin:0; color:white;">{title}</h3>
    </div>
    """
