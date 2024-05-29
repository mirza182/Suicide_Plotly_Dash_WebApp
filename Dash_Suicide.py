# app.py
from flask import Flask
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import mysql.connector
import pandas as pd
import plotly.express as px
from layout import get_layout

# Initialize Flask app
server = Flask(__name__)

# Initialize the Dash app
app = dash.Dash(__name__, server=server, url_base_pathname='/', assets_folder='assets')

# Function to establish a connection to the database
def create_connection():
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="hamza182",
        database="bootcamp_project"
    )
    return connection

# Function to fetch unique values for dropdown options
def fetch_unique_values(column):
    connection = create_connection()
    query = f"SELECT DISTINCT {column} FROM suicide_data"
    data = pd.read_sql(query, connection)
    connection.close()
    return data[column].tolist()

# Fetch unique values for country dropdown
unique_countries = fetch_unique_values('country')

# Function to fetch data from MySQL database
def fetch_data(country=None, year=None):
    query = "SELECT * FROM suicide_data WHERE 1=1"
    
    if country:
        query += f" AND country='{country}'"
    if year:
        query += f" AND year={year}"
    
    connection = create_connection()
    data = pd.read_sql(query, connection)
    connection.close()
    
    return data

# Function to fetch data for the line chart based on country
def fetch_data_by_country(country):
    query = f"SELECT year, SUM(suicides_no) AS total_suicides FROM suicide_data WHERE country='{country}' GROUP BY year"
    connection = create_connection()
    data = pd.read_sql(query, connection)
    connection.close()
    return data

# Function to fetch available years for a given country
def fetch_years_by_country(country):
    query = f"SELECT DISTINCT year FROM suicide_data WHERE country='{country}'"
    connection = create_connection()
    data = pd.read_sql(query, connection)
    connection.close()
    return data['year'].tolist()

# Set the layout of the dashboard using the imported layout function
app.layout = get_layout(unique_countries)

# Callback to update the line chart based on the selected country
@app.callback(
    Output('line-chart', 'figure'),
    [Input('country-dropdown', 'value')]
)
def update_line_chart(selected_country):
    data = fetch_data_by_country(selected_country)
    line_fig = px.line(data, x='year', y='total_suicides', title=f'Suicide Numbers Over Time in {selected_country}')
    return line_fig

# Callback to update the year dropdown based on the selected country
@app.callback(
    Output('year-dropdown', 'options'),
    [Input('country-dropdown', 'value')]
)
def update_year_dropdown(selected_country):
    available_years = fetch_years_by_country(selected_country)
    return [{'label': str(year), 'value': year} for year in available_years]

# Callback to update the year dropdown value to the first available year when the country changes
@app.callback(
    Output('year-dropdown', 'value'),
    [Input('year-dropdown', 'options')]
)
def set_year_dropdown_value(year_options):
    if year_options:
        return year_options[0]['value']
    return None

# Callback to update the other charts based on filters
@app.callback(
    [Output('pie-chart-male', 'figure'), Output('pie-chart-female', 'figure'), Output('bar-chart', 'figure'), Output('selected-year', 'children')],
    [Input('country-dropdown', 'value'), Input('year-dropdown', 'value')]
)
def update_other_charts(selected_country, selected_year):
    data = fetch_data(country=selected_country, year=selected_year)
    
    # Filter out age groups with no suicides
    male_data_filtered = data[(data['sex'] == 'male') & (data['suicides_no'] > 0)]
    female_data_filtered = data[(data['sex'] == 'female') & (data['suicides_no'] > 0)]
    
    # Data for male and female pie charts
    pie_fig_male = px.pie(male_data_filtered, names='age', values='suicides_no', title='Suicides by Age Group (Male)')
    pie_fig_female = px.pie(female_data_filtered, names='age', values='suicides_no', title='Suicides by Age Group (Female)')
    
    # Bar chart for suicides by gender for a selected year and country
    aggregated_data = data.groupby(['country', 'sex']).agg({'suicides_no': 'sum'}).reset_index()
    total_suicides_male = aggregated_data.loc[aggregated_data['sex'] == 'male', 'suicides_no'].iloc[0]
    total_suicides_female = aggregated_data.loc[aggregated_data['sex'] == 'female', 'suicides_no'].iloc[0]
    aggregated_data['suicides_percentage'] = 100 * aggregated_data['suicides_no'] / (total_suicides_male + total_suicides_female)
    
    # Round the percentage values to one decimal place
    aggregated_data['suicides_percentage'] = aggregated_data['suicides_percentage'].round(1)
    
    bar_fig = px.bar(aggregated_data, x='country', y='suicides_percentage', color='sex', barmode='group', 
                     title='Suicide Percentage by Gender', text='suicides_percentage', labels={'suicides_percentage': 'Suicide Percentage (%)'})
    
    return pie_fig_male, pie_fig_female, bar_fig, f"Selected Year: {selected_year}"

# Define Flask route to render the Dash app
@server.route('/')
def index():
    return app.index()

# Run the Flask app
if __name__ == '__main__':
    server.run(debug=True)
