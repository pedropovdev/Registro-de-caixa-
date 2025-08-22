import pandas as pd
import plotly.express as px
from dash import Dash, dcc, html
from dash.dependencies import Input, Output  

df = pd.read_csv("qualidade_do_ar.csv")

app = Dash(__name__)

app.layout = html.Div([
    html.H1("🌍 Dashboard de Qualidade do Ar - Recôncavo Baiano", style={"textAlign": "center"}),

    dcc.Dropdown(
        id="cidade-dropdown",
        options=[{"label": cidade, "value": cidade} for cidade in df["cidade"].unique()],
        value="Salvador"
    ),

    dcc.Graph(id="grafico-poluentes"),
    dcc.Graph(id="grafico-comparativo")
])

# ✅ IDs corrigidos
@app.callback(
    [Output("grafico-poluentes", "figure"),
     Output("grafico-comparativo", "figure")],
    [Input("cidade-dropdown", "value")]
)
def update_graphs(cidade):
    df_cidade = df[df["cidade"] == cidade].melt(id_vars="cidade", var_name="Poluente", value_name="Concentração")

    fig1 = px.bar(df_cidade, x="Poluente", y="Concentração", 
                  title=f"Poluentes em {cidade}", color="Poluente")

    fig2 = px.line(
        df.melt(id_vars="cidade", var_name="Poluente", value_name="Concentração"),
        x="cidade", y="Concentração", color="Poluente", markers=True,
        title="Comparação entre Cidades"
    )

    return fig1, fig2

if __name__ == "__main__":
    app.run(debug=True)
