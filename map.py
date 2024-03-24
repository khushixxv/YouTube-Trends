import pandas as pd
import plotly.graph_objects as go
import json
import numpy as np
import plotly.express as px

def generate_map():
# Custom color map for countries
    country_keys = ['Brazil', 'Canada', 'Germany', 'France', 'Great Britain', 'India', 'Japan', 'South Korea', 'Mexico', 'Russia', 'United States']

    color_map = {
        'Brazil': 'blue',
        'Canada': 'red',
        'Germany': 'green',
        'France': 'yellow',
        'Great Britain': 'purple',
        'India': 'orange',
        'Japan': 'pink',
        'South Korea': 'lightgreen',
        'Mexico': 'teal',
        'Russia': 'gray',
        'United States': 'darkblue'
    }
        
    # ISO names mapping for the countries..
    country_iso_map = {
        'Brazil': 'BRA',
        'Canada': 'CAN',
        'Germany': 'DEU',
        'France': 'FRA',
        'Great Britain': 'GBR',
        'India': 'IND',
        'Japan': 'JPN',
        'South Korea': 'KOR',
        'Mexico': 'MEX',
        'Russia': 'RUS',
        'United States': 'USA'
    }

    # Load the datasets for each country
    df_combined = pd.DataFrame()
    for country in zip(["BR", "CA", "DE", "FR", "GB", "IN", "JP", "KR", "MX", "RU", "US"], country_keys):
        df = pd.read_csv(f'archive/{country[0]}_youtube_trending_data.csv') # load data from csv
        df['country'] = country[1] # add a column to distinguish the countries
        df_combined = pd.concat([df_combined, df]) # Concatenate all the DataFrames
    
    
    df_combined['iso-locations'] = [country_iso_map[key] for key in df_combined['country']] # add a column to map the countries to their ISO names

    # Convert 'trending_date' to datetime for proper plotting
    df_combined['trending_date'] = pd.to_datetime(df_combined['trending_date'])
    # Generate 'year' from 'trending_date'
    df_combined['year'] = df_combined['trending_date'].dt.strftime('%Y')

    # Load the category names from the JSON file
    with open('archive/category_id.json', 'r') as file: #NOTE: changed json file name because they're all the same
        category_data = json.load(file)

    # Create a mapping of category IDs to their names
    category_id_to_name = {item['id']: item['snippet']['title'] for item in category_data['items']}

    # Map categoryId to category names, ensuring categoryId is treated as a string for matching
    df_combined['categoryId'] = df_combined['categoryId'].astype(str)
    df_combined['category_name'] = df_combined['categoryId'].map(category_id_to_name)


    # Get the index of the video with the greatest views from each country, for each year
    idx = df_combined.groupby(['country', 'year'])['view_count'].idxmax()

    # Use these indices to get the corresponding videos
    greatest_views = df_combined.loc[idx]

    # Calculate the log-transformed view counts
    greatest_views['log_view_counts'] = np.log(greatest_views['view_count'])
    # Divide the log view counts into 10 evenly split tick bars
    log_tickvals = np.linspace(greatest_views['log_view_counts'].min(), greatest_views['log_view_counts'].max(), 10)
    # Transform the log tick values back to real values
    real_tickvals = np.exp(log_tickvals)
    # Format the real tick values as strings
    real_ticktext = [f'{val:.1e}' for val in real_tickvals]

    # Create a new column in 'greatest_views' that contains the tooltip text for each country
    greatest_views['tooltip_text'] = 'Title: ' + greatest_views['title'] + '<br>Views: ' + greatest_views['view_count'].astype(str) + '<br>Category: ' + greatest_views['category_name']

    # fig = go.Figure(data=go.Choropleth(
    #     locations=[country_iso_map[f'{key}'] for key in country_keys],
    #     locationmode='ISO-3',
    #     z=log_view_counts,
    #     text=greatest_views['tooltip_text'],
    #     hoverinfo='text',
    #     colorscale="rainbow",
    #     colorbar=dict(
    #         title='Log View Count of Most Viewed Video',
    #         tickvals=log_tickvals,  # Specify the positions of the tick labels
    #         ticktext=real_ticktext,  # Specify the text of the tick labels
    #     ),
    # ))


    fig = px.choropleth(
        greatest_views,  # Pass the DataFrame directly to px.choropleth
        locations='iso-locations', # [country_iso_map[f'{key}'] for key in country_keys],
        locationmode='ISO-3',
        color='log_view_counts',  # Use the 'color' parameter to specify the column to map to the color scale
        hover_name='tooltip_text',  # Use the 'hover_name' parameter to specify the column to use for the hover text
        color_continuous_scale="rainbow",
        labels={'color': 'Log View Count of Most Viewed Video'},  # Use the 'labels' parameter to specify the label for the color scale
        animation_frame='year'  # Add a timeline selector
    )

    fig.update_layout(coloraxis_colorbar=dict(
        title='Log View Count of Most Viewed Video',
        tickvals=log_tickvals,  # Specify the positions of the tick labels
        ticktext=real_ticktext,  # Specify the text of the tick labels
    ))

    # fig = go.Figure(data = go.Choropleth(locations=[country_iso_map[f'{key}'] for key in country_keys], locationmode='ISO-3', z=np.log(greatest_views['log_view_count']), colorscale="rainbow", colorbar=)))
    
    #  fig.show()
    # plot_html = fig.to_html(full_html=False)
    # return plot_html
    fig.write_html('static/map.html')
    fig.show()

generate_map()