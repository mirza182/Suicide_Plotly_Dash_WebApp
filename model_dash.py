import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import pickle

# Load the trained model
model_path = 'model/random_forest_model.pkl'
with open(model_path, 'rb') as f:
    model = pickle.load(f)

# Initialize the Dash app
app = dash.Dash(__name__, url_base_pathname='/ml_model/')

# Define the layout of the Dash app
app.layout = html.Div([
    html.H1("Suicide Rate Prediction"),
    html.Div([
        html.Label("Number of suicides:"),
        dcc.Input(id='suicides-input', type='number', value=21, min=1, step=1),
        html.Br(),
        html.Label("Population:"),
        dcc.Input(id='population-input', type='number', value=312900, min=0, step=100),
        html.Br(),
        html.Label("Sex:"),
        dcc.Dropdown(
            id='sex-dropdown',
            options=[
                {'label': 'Male', 'value': 1},
                {'label': 'Female', 'value': 0}
            ],
            value=1,
            style={'color': 'black'}  # Set text color to black
        ),
        html.Br(),
        html.Button('Predict', id='predict-button', n_clicks=0),
        html.Hr(),
        html.H3(id='prediction-output', children='Predicted suicides/100k: ')
    ])
])

# Define the callback to update the prediction
@app.callback(
    Output('prediction-output', 'children'),
    [Input('predict-button', 'n_clicks')],
    [dash.dependencies.State('suicides-input', 'value'),
     dash.dependencies.State('population-input', 'value'),
     dash.dependencies.State('sex-dropdown', 'value')]
)
def update_prediction(n_clicks, suicides, population, sex):
    if n_clicks > 0:
        # Prepare the input data for prediction
        input_data = [[suicides, population, sex, 1 - sex]]  # [suicides, population, male, female]
        
        # Make the prediction using the loaded model
        prediction = model.predict(input_data)
        
        # Return the prediction result
        return f'Predicted suicides/100k: {prediction[0]:.2f}'
    return 'Predicted suicides/100k: '

if __name__ == '__main__':
    app.run_server(debug=True)