# Dash Suicide Analysis Dashboard

This project consists of two main components: `app.py` and `model_dash.py`, along with supporting files for database setup (`database_setup.sql`), data loading (`load_data.sql`), and styling (`styles.css`). Below are the details of each component:

## 1. app.py

This file contains the code for the Dash web application that analyzes suicide data. It includes the following functionalities:

- Connects to a MySQL database containing suicide data.
- Fetches unique values for dropdown options (country and year) from the database.
- Sets up a Dash layout using the `layout.py` module.
- Defines callback functions to update charts based on user inputs.
- Renders the Dash app with Flask integration.

## 2. model_dash.py

This file contains the code for another Dash web application that predicts suicide rates using a machine learning model. It includes the following functionalities:

- Loads a trained machine learning model from a pickle file.
- Defines a Dash layout with input fields for number of suicides, population, and sex.
- Implements a callback function to predict suicide rates based on user inputs.

## 3. Database Setup (`database_setup.sql`)

This SQL script sets up the necessary database and table structure for storing suicide data. It creates a table named `suicide_data` with columns for country, year, sex, age, suicides number, population, GDP per capita, and generation.

## 4. Data Loading (`load_data.sql`)

This SQL script loads data from a CSV file (`master.csv`) into the `suicide_data` table. It uses the `LOAD DATA INFILE` command to efficiently import data.

## 5. Styling (`styles.css`)

This CSS file contains styles for the Dash web applications. It includes general styling for the body, containers, headers, labels, dropdowns, graphs, and other components.

## 6. Layout Module (`layout.py`)

This Python module provides a function (`get_layout`) to generate the layout for the Dash Suicide Analysis Dashboard. It creates HTML elements and Dash components for dropdowns, graphs, and other visualizations.
