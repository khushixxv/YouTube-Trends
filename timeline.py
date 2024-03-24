import plotly.express as px
import pandas as pd
import json

def generate_timeline():
    # Load the datasets for each country
    df_us = pd.read_csv('../archive/US_youtube_trending_data.csv')  

    df_combined = df_us

    # Convert 'trending_date' to datetime for proper plotting
    df_combined['trending_date'] = pd.to_datetime(df_combined['trending_date'])

    # Generate 'year_month' from 'trending_date'
    df_combined['year_month'] = df_combined['trending_date'].dt.strftime('%Y-%m')

    # Load the category names from the JSON file
    with open('../archive/US_category_id.json', 'r') as file:
        category_data = json.load(file)

    # Create a mapping of category IDs to their names
    category_id_to_name = {item['id']: item['snippet']['title'] for item in category_data['items']}

    # Map categoryId to category names, ensuring categoryId is treated as a string for matching
    df_combined['categoryId'] = df_combined['categoryId'].astype(str)
    df_combined['category_name'] = df_combined['categoryId'].map(category_id_to_name)

    # Group by 'year_month' and 'category_name', then count occurrences
    df_grouped = df_combined.groupby(['year_month', 'category_name']).size().reset_index(name='counts')

    # Calculate total videos per month for percentage calculation
    df_total_per_month = df_combined.groupby('year_month').size().reset_index(name='total')

    # Merge to get total per month in the grouped DataFrame
    df_grouped = pd.merge(df_grouped, df_total_per_month, on='year_month', how="inner", validate="many_to_many")

    # Calculate percentage
    df_grouped['percentage'] = (df_grouped['counts'] / df_grouped['total']) * 100

    # Now, create the graph with aggregated monthly data
    fig = px.line(df_grouped, x='year_month', y='percentage', color='category_name',
                  title='US Trending Video Categories Over Time',
                  labels={'percentage': 'Popularity Percentage', 'category_name': 'Category', 'year_month': 'Month'})

    # Adjust line sizes if needed
    fig.update_traces(line=dict(width=1))

    # Show the figure
    #fig.show()

    # Convert the plot to HTML representation
    plot_html = fig.to_html(full_html=False)

    return plot_html
