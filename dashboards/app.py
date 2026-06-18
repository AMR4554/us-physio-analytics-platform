import pandas as pd

import dash
from dash import html, dcc, Input, Output, State, clientside_callback
import dash_bootstrap_components as dbc
import plotly.express as px

# =====================================
# LOAD DATA
# =====================================

kpi     = pd.read_csv("output/kpi_summary.csv")
clinic  = pd.read_csv("output/clinic_performance.csv")
monthly = pd.read_csv("output/monthly_revenue.csv")

# =====================================
# HELPER
# =====================================

def _kpi_card(card_id, title):
    return html.Div(
        [
            html.Div(title, className="kpi-title"),
            html.Div(id=card_id, className="kpi-value"),
        ],
        className="kpi-card"
    )


def _download_menu(btn_csv_id, btn_pdf_id, label="Download"):
    """Dropdown split-button: CSV (server) + PDF screenshot (client-side)."""
    return dbc.DropdownMenu(
        label=f"⬇ {label}",
        children=[
            dbc.DropdownMenuItem("📄 CSV",         id=btn_csv_id),
            dbc.DropdownMenuItem("🖼 PDF / Image", id=btn_pdf_id),
        ],
        color="outline-primary",  # Fixed: Handled via Bootstrap's outline class string
        size="sm",
        toggle_style={"fontSize": "0.8rem"},
    )

# =====================================
# APP
# =====================================

app = dash.Dash(
    __name__,
    external_stylesheets=[dbc.themes.BOOTSTRAP],
)

app.layout = dbc.Container(
    [
        # ── Stores & Dummy Utilities ─────────────────────────────────────────
        dcc.Store(id="store-selected-clinic", data=None),
        dcc.Store(id="store-filtered-clinic"),
        dcc.Store(id="store-filtered-monthly"),
        html.Div(id="dummy-clientside-output", style={"display": "none"}), # Fixed: Circular dependency workaround

        # ── Server-side CSV downloads ────────────────────────────────────────
        dcc.Download(id="download-clinic-csv"),
        dcc.Download(id="download-monthly-csv"),

        # ── Header ──────────────────────────────────────────────────────────
        html.H1("US Physiotherapy Analytics Platform", className="my-3"),

        # ── Filter badge + reset ─────────────────────────────────────────────
        dbc.Row(
            [
                dbc.Col(html.Div(id="filter-badge"), width="auto"),
                dbc.Col(
                    dbc.Button("✕ Reset Filter", id="btn-reset",
                               color="secondary", outline=True, size="sm"),
                    width="auto"
                ),
            ],
            className="mb-2",
            align="center",
        ),

        # ── KPI cards ───────────────────────────────────────────────────────
        dbc.Row(
            [
                dbc.Col(_kpi_card("kpi-revenue",  "Total Revenue")),
                dbc.Col(_kpi_card("kpi-visits",   "Total Visits")),
                dbc.Col(_kpi_card("kpi-patients", "Patients")),
                dbc.Col(_kpi_card("kpi-outcome",  "Avg Outcome")),
            ]
        ),

        html.Br(),

        # ── Charts ──────────────────────────────────────────────────────────
        dbc.Row(
            [
                # ── Clinic bar chart ────────────────────────────────────────
                dbc.Col(
                    [
                        dbc.Row(
                            [
                                dbc.Col(
                                    html.Small("Click a bar to filter all charts",
                                               className="text-muted")
                                ),
                                dbc.Col(
                                    _download_menu(
                                        "btn-clinic-csv",
                                        "btn-clinic-pdf",
                                        "Clinic Chart"
                                    ),
                                    width="auto"
                                ),
                            ],
                            align="center", className="mb-1"
                        ),
                        dcc.Graph(id="chart-clinic",
                                  config={"displayModeBar": False}),
                    ],
                    width=6
                ),

                # ── Monthly line chart ───────────────────────────────────────
                dbc.Col(
                    [
                        dbc.Row(
                            [
                                dbc.Col(
                                    html.Small("Reflects selected clinic",
                                               className="text-muted")
                                ),
                                dbc.Col(
                                    _download_menu(
                                        "btn-monthly-csv",
                                        "btn-monthly-pdf",
                                        "Monthly Chart"
                                    ),
                                    width="auto"
                                ),
                            ],
                            align="center", className="mb-1"
                        ),
                        dcc.Graph(id="chart-monthly",
                                  config={"displayModeBar": False}),
                    ],
                    width=6
                ),
            ]
        ),

        # ── Client-side JS for PDF/image export ─────────────────────────────
        html.Script("""
            window.downloadChartAsPdf = function(graphDivId, filename) {
                var gd = document.getElementById(graphDivId);
                if (!gd) { alert('Chart not found'); return; }
                Plotly.toImage(gd, {format: 'png', width: 1200, height: 600})
                    .then(function(dataUrl) {
                        var link = document.createElement('a');
                        link.href = dataUrl;
                        link.download = filename + '.png';
                        link.click();
                    });
            };
        """),
    ],
    fluid=True,
)

# =====================================================================
# CLIENT-SIDE CALLBACKS — PDF/image export (runs in browser)
# =====================================================================

# Clinic chart → PNG download
app.clientside_callback(
    """
    function(n_clicks) {
        if (!n_clicks) return window.dash_clientside.no_update;
        window.downloadChartAsPdf('chart-clinic', 'clinic_revenue_chart');
        return window.dash_clientside.no_update;
    }
    """,
    Output("dummy-clientside-output", "children", allow_duplicate=True),
    Input("btn-clinic-pdf",  "n_clicks"),
    prevent_initial_call=True,
)

# Monthly chart → PNG download
app.clientside_callback(
    """
    function(n_clicks) {
        if (!n_clicks) return window.dash_clientside.no_update;
        window.downloadChartAsPdf('chart-monthly', 'monthly_revenue_chart');
        return window.dash_clientside.no_update;
    }
    """,
    Output("dummy-clientside-output", "children", allow_duplicate=True),
    Input("btn-monthly-pdf",  "n_clicks"),
    prevent_initial_call=True,
)

# =====================================================================
# CALLBACK 1 — store selected clinic
# =====================================================================

@app.callback(
    Output("store-selected-clinic", "data"),
    Input("chart-clinic", "clickData"),
    Input("btn-reset",    "n_clicks"),
    State("store-selected-clinic", "data"),
    prevent_initial_call=True,
)
def store_selection(click_data, _reset, current):
    trigger = dash.ctx.triggered_id  # Fixed: Clean, modern tracker mechanism
    
    if trigger == "btn-reset":
        return None
    if trigger == "chart-clinic" and click_data:
        clicked = click_data["points"][0]["x"]
        return None if clicked == current else clicked
    return current


# =====================================================================
# CALLBACK 2 — update KPI cards, charts, badge
# =====================================================================

@app.callback(
    Output("kpi-revenue",  "children"),
    Output("kpi-visits",   "children"),
    Output("kpi-patients", "children"),
    Output("kpi-outcome",  "children"),
    Output("chart-clinic",  "figure"),
    Output("chart-monthly", "figure"),
    Output("filter-badge",  "children"),
    Output("store-filtered-clinic",  "data"),
    Output("store-filtered-monthly", "data"),
    Input("store-selected-clinic", "data"),
)
def update_all(selected_clinic):
    clinic_df  = clinic.copy()
    monthly_df = monthly.copy()

    if selected_clinic and "clinic_name" in monthly_df.columns:
        monthly_df = monthly_df[monthly_df["clinic_name"] == selected_clinic]

    # KPI recalc
    if selected_clinic and not monthly_df.empty:
        rev      = monthly_df["revenue_amount"].sum()      if "revenue_amount"    in monthly_df.columns else 0
        visits   = monthly_df["total_visits"].sum()        if "total_visits"      in monthly_df.columns else "—"
        patients = monthly_df["unique_patients"].nunique() if "unique_patients"   in monthly_df.columns else "—"
        outcome  = round(monthly_df["avg_outcome_score"].mean(), 2) if "avg_outcome_score" in monthly_df.columns else "—"
        kpi_rev      = f"${rev:,.0f}"
        kpi_visits   = f"{visits:,}"   if isinstance(visits,   (int, float)) else visits
        kpi_patients = f"{patients:,}" if isinstance(patients, (int, float)) else patients
        kpi_outcome  = str(outcome)
    else:
        kpi_rev      = f"${kpi['total_revenue'][0]:,.0f}"
        kpi_visits   = f"{kpi['total_visits'][0]:,}"
        kpi_patients = f"{kpi['unique_patients'][0]:,}"
        kpi_outcome  = str(kpi['avg_outcome_score'][0])

    # Clinic bar
    clinic_colors = [
        "#1f77b4" if (selected_clinic is None or row == selected_clinic) else "#d3d3d3"
        for row in clinic_df["clinic_name"]
    ]
    clinic_fig = px.bar(clinic_df, x="clinic_name", y="revenue",
                        title="Revenue by Clinic")
    clinic_fig.update_traces(marker_color=clinic_colors)
    clinic_fig.update_layout(clickmode="event+select",
                             xaxis_title="Clinic", yaxis_title="Revenue ($)")

    # Monthly line
    monthly_fig = px.line(monthly_df, x="month_year", y="revenue_amount",
                          title="Monthly Revenue Trend" +
                          (f" — {selected_clinic}" if selected_clinic else ""))
    monthly_fig.update_layout(xaxis_title="Month", yaxis_title="Revenue ($)")

    badge = (
        dbc.Badge(f"Filtered: {selected_clinic}", color="primary", className="me-2")
        if selected_clinic else ""
    )

    return (
        kpi_rev, kpi_visits, kpi_patients, kpi_outcome,
        clinic_fig, monthly_fig, badge,
        clinic_df.to_dict("records"),
        monthly_df.to_dict("records"),
    )


# =====================================================================
# CSV DOWNLOAD CALLBACKS
# =====================================================================

@app.callback(
    Output("download-clinic-csv", "data"),
    Input("btn-clinic-csv", "n_clicks"),
    State("store-filtered-clinic", "data"),
    prevent_initial_call=True,
)
def download_clinic_csv(_, stored):
    df = pd.DataFrame(stored) if stored else clinic
    return dcc.send_data_frame(df.to_csv, "clinic_performance.csv", index=False)


@app.callback(
    Output("download-monthly-csv", "data"),
    Input("btn-monthly-csv", "n_clicks"),
    State("store-filtered-monthly", "data"),
    prevent_initial_call=True,
)
def download_monthly_csv(_, stored):
    df = pd.DataFrame(stored) if stored else monthly
    return dcc.send_data_frame(df.to_csv, "monthly_revenue.csv", index=False)


# ── Run ───────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    app.run(debug=True)