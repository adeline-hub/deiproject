import dash
from dash import dcc, html, Input, Output
import pandas as pd
import plotly.express as px

# Load dataset
df = pd.read_csv("deities-v2.csv")  # Replace with your full file path if needed

# Initialize app with meta tags
app = dash.Dash(
    __name__,
    assets_folder='assets',
    meta_tags=[
        {"name": "description", "content": "Explore a world of deities through data"},
        {"property": "og:image", "content": "/assets/share.png"},
        {"name": "twitter:image", "content": "/assets/share.png"},
    ]
)
server = app.server
app.title = "Mythic Atlas"

# Layout
app.layout = html.Div(style={"backgroundColor": "black", "color": "white", "fontFamily": "Courier New"}, children=[
    html.H1("Mythic Atlas: Explore Global Deities", style={"textAlign": "center"}),

    html.Div([
        html.Label("Filter by Pantheon"),
        dcc.Dropdown(
            id='pantheon-filter',
            options=[{"label": p, "value": p} for p in sorted(df['Pantheon'].dropna().unique())],
            placeholder="Select Pantheon"
        ),

        html.Label("Filter by Sex"),
        dcc.Dropdown(
            id='sex-filter',
            options=[{"label": s, "value": s} for s in sorted(df['Sex'].dropna().unique())],
            placeholder="Select Sex"
        ),

        html.Label("Filter by Title"),
        dcc.Dropdown(
            id='title-filter',
            options=[{"label": t, "value": t} for t in sorted(df['Title'].dropna().unique())],
            placeholder="Select Title"
        ),
    ], style={"width": "30%", "float": "left"}),

    html.Div(id='deity-output', style={"marginLeft": "35%"}),

    dcc.Graph(id='sex-pie'),
    dcc.Graph(id='pantheon-bar'),
    dcc.Graph(id='values-treemap')
])

# Callbacks
@app.callback(
    Output('deity-output', 'children'),
    Output('sex-pie', 'figure'),
    Output('pantheon-bar', 'figure'),
    Output('values-treemap', 'figure'),
    Input('pantheon-filter', 'value'),
    Input('sex-filter', 'value'),
    Input('title-filter', 'value')
)
def update_output(pantheon, sex, title):
    filtered_df = df.copy()
    if pantheon:
        filtered_df = filtered_df[filtered_df['Pantheon'] == pantheon]
    if sex:
        filtered_df = filtered_df[filtered_df['Sex'] == sex]
    if title:
        filtered_df = filtered_df[filtered_df['Title'] == title]

    deity_info = html.Ul([
        html.Li(f"{row['Name']} ({row['Pantheon']} - {row['Sex']}) — {row['Function']}")
        for _, row in filtered_df.iterrows()
    ]) if not filtered_df.empty else "No deities match the selected filters."

    pie = px.pie(filtered_df, names='Sex', title='Deities by Sex')
    bar = px.bar(filtered_df['Pantheon'].value_counts().reset_index(),
                 x='index', y='Pantheon', labels={'index': 'Pantheon', 'Pantheon': 'Count'},
                 title='Number of Deities per Pantheon')
    treemap = px.treemap(filtered_df, path=['Values'], title='Treemap of Values')

    for fig in (pie, bar, treemap):
        fig.update_layout(paper_bgcolor='black', font_color='white')

    return deity_info, pie, bar, treemap

if __name__ == '__main__':
    app.run_server(debug=True)



