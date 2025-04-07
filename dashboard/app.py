import dash
from dash import Dash, html, dcc, dash_table, Input, Output
import pandas as pd
import plotly.express as px

app = Dash(__name__)
app.title = "Dashboard ELAYEB Projet Advanced Python GIT Linux for BI"

def load_prices():
    try:
        df = pd.read_csv("data/bitcoin_prices.csv", names=["Date", "Heure", "Prix"], header=None)
        df["Datetime"] = pd.to_datetime(df["Date"] + " " + df["Heure"], format="%Y-%m-%d %H:%M:%S", errors="coerce")
        df["Prix"] = pd.to_numeric(df["Prix"], errors="coerce")
        df = df.dropna(subset=["Datetime", "Prix"]).sort_values("Datetime")
        return df
    except Exception as e:
        print("Erreur chargement bitcoin_prices.csv :", e)
        return pd.DataFrame(columns=["Date", "Heure", "Prix", "Datetime"])


def load_report():
    try:
        df = pd.read_csv("data/daily_report.csv", header=None)
        df.columns = ["Date", "Open", "Close", "High", "Low"]
        return df
    except Exception as e:
        print("Erreur chargement daily_report.csv :", e)
        return pd.DataFrame(columns=["Date", "Open", "Close", "High", "Low"])

app.layout = html.Div([
    html.H1("Dashboard Bitcoin", style={'textAlign': 'center'}),

    dcc.Interval(
        id='interval-refresh',
        interval=4 * 60 * 1000,  # 4 minutes
        n_intervals=0
    ),

    dcc.Graph(id="price-graph"),

    html.H2("Données brutes (scrape)", style={'marginTop': '40px'}),
    dash_table.DataTable(
        id='price-table',
        columns=[{"name": i, "id": i} for i in ["Date", "Heure", "Prix"]],
        page_size=10,
        style_table={'overflowX': 'auto'},
    ),

    html.H2("Rapport journalier", style={'marginTop': '40px'}),
    dash_table.DataTable(
        id='report-table',
        columns=[{"name": i, "id": i} for i in ["Date", "Open", "Close", "High", "Low"]],
        page_size=5,
        style_table={'overflowX': 'auto'},
    ),
])

@app.callback(
    [Output("price-graph", "figure"),
     Output("price-table", "data"),
     Output("report-table", "data")],
    Input("interval-refresh", "n_intervals")
)
def update_dashboard(n):
    prices_df = load_prices()
    report_df = load_report()
    fig = px.line(prices_df, x="Datetime", y="Prix", title="Évolution du prix du Bitcoin (USD)")
    return fig, prices_df.to_dict("records"), report_df.to_dict("records")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8050)
