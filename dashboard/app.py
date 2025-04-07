import dash
from dash import Dash, html, dcc, dash_table, Input, Output
import pandas as pd
import plotly.express as px

app = Dash(__name__)

# Fonction qui recharge les données depuis le CSV
def load_data():
    try:
        df = pd.read_csv("data/bitcoin_prices.csv")
    except Exception as e:
        print("Erreur lecture CSV :", e)
        df = pd.DataFrame(columns=["timestamp", "price"])
    return df

app.layout = html.Div([
    html.H1("Bitcoin Price Dashboard"),
    
    dcc.Interval(
        id='interval-update',
        interval=4 * 60 * 1000,  # toutes les 4 minutes en millisecondes
        n_intervals=0
    ),
    
    dash_table.DataTable(
        id='price-table',
        columns=[{"name": i, "id": i} for i in ["timestamp", "price"]],
        data=load_data().to_dict("records")
    ),
    # Ce composant permet de déclencher le callback au chargement de la page
    dcc.Interval(
        id='trigger-on-load',
        interval=1*1000,  # 1 seconde (se déclenche une fois)
        n_intervals=0
    )
])

@app.callback(
    Output('price-table', 'data'),
    Input('trigger-on-load', 'n_intervals')
)

@app.callback(
    dash.dependencies.Output("price-table", "data"),
    dash.dependencies.Input("interval-update", "n_intervals")
)
def update_table(n):
    df = load_data()
    return df.to_dict("records")

# Je charge mes données
prices_df = pd.read_csv('data/bitcoin_prices.csv')
report_df = pd.read_csv('data/daily_report.csv')

# J'ajoute des lignes pour que les colonnes soient bien nommées
prices_df["Datetime"] = pd.to_datetime(prices_df["Date"] + " " + prices_df["Heure"])
report_df.columns = ["Date", "Open", "Close", "High", "Low"]

# Je plot la courbe des prix
fig = px.line(prices_df, x="Datetime", y="Prix", title="Évolution du prix du Bitcoin (USD)")

# Je crée l'app Dash
app = dash.Dash(__name__)
app.title = "Dashboard ELAYEB Projet Advanced Python GIt Linux for BI"

app.layout = html.Div([
    html.H1("Dashboard Bitcoin", style={'textAlign': 'center'}),
    dcc.Graph(figure=fig),
    html.H2("Données brutes (scrape)", style={'marginTop': '40px'}),
    dash_table.DataTable(
        data=prices_df.to_dict('records'),
        columns=[{"name": i, "id": i} for i in ["Date", "Heure", "Prix"]],
        page_size=10,
        style_table={'overflowX': 'auto'},),
    html.H2("Rapport journalier", style={'marginTop': '40px'}),
    dash_table.DataTable(
        data=report_df.to_dict('records'),
        columns=[{"name": i, "id": i} for i in report_df.columns],
        page_size=5,
        style_table={'overflowX': 'auto'},)
])

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8050)
