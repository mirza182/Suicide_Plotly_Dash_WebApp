from dash import dcc, html

def get_layout(unique_countries):
    return html.Div(
        className='container',
        children=[
            html.H1("Suicide Analysis Dashboard", className='header'),
            
            html.Div(className='dropdown-container', children=[
                html.Label("Select Country:"),
                dcc.Dropdown(
                    id='country-dropdown',
                    options=[{'label': c, 'value': c} for c in unique_countries],
                    value=unique_countries[0],
                    className='dropdown'
                ),
            ]),
            
            html.Div(className='dropdown-container', children=[
                html.Label("Select Year:"),
                dcc.Dropdown(
                    id='year-dropdown',
                    className='dropdown'
                ),
            ]),
            
            dcc.Graph(id='line-chart', className='graph-container'),
            
            html.Div(
                className='flex-container',
                children=[
                    html.Div(
                        className='graph-container',
                        children=[dcc.Graph(id='pie-chart-male')]
                    ),
                    html.Div(
                        className='graph-container',
                        children=[dcc.Graph(id='pie-chart-female')]
                    )
                ]
            ),
            
            html.Div(id='selected-year', style={'textAlign': 'center', 'margin-top': '20px'}),
            
            dcc.Graph(id='bar-chart', className='graph-container')
        ]
    )
