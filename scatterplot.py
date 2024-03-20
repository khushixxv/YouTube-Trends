import plotly.express as px
import pandas as pd

def generate_scatterplot(): 
    # Load the datasets for each country
    df_br = pd.read_csv('archive/BR_youtube_trending_data.csv')  # Brazil
    df_ca = pd.read_csv('archive/CA_youtube_trending_data.csv')  # Canada
    """ df_de = pd.read_csv('archive/DE_youtube_trending_data.csv')  # Germany
    df_fr = pd.read_csv('archive/FR_youtube_trending_data.csv')  # France
    df_gb = pd.read_csv('archive/GB_youtube_trending_data.csv')  # Great Britain
    df_in = pd.read_csv('archive/IN_youtube_trending_data.csv')  # India
    df_jp = pd.read_csv('archive/JP_youtube_trending_data.csv')  # Japan
    df_kr = pd.read_csv('archive/KR_youtube_trending_data.csv')  # South Korea
    df_mx = pd.read_csv('archive/MX_youtube_trending_data.csv')  # Mexico
    df_ru = pd.read_csv('archive/RU_youtube_trending_data.csv')  # Russia
    df_us = pd.read_csv('archive/US_youtube_trending_data.csv')  # United States """
    
    # Add a column to distinguish the countries
    df_br['Country'] = 'Brazil'
    df_ca['Country'] = 'Canada'
    """ df_de['Country'] = 'Germany'
    df_fr['Country'] = 'France'
    df_gb['Country'] = 'Great Britain'
    df_in['Country'] = 'India'
    df_jp['Country'] = 'Japan'
    df_kr['Country'] = 'South Korea'
    df_mx['Country'] = 'Mexico'
    df_ru['Country'] = 'Russia'
    df_us['Country'] = 'United States' """
    # Concatenate all the DataFrames
    #df_combined = pd.concat([df_br, df_ca, df_de, df_fr, df_gb, df_in, df_jp, df_kr, df_mx, df_ru, df_us])
    
    df_combined = pd.concat([df_br, df_ca])
    
    # Custom color map for countries
    color_map = {
        'Brazil': 'blue',
        'Canada': 'red',
        #'Germany': 'green',
        #'France': 'yellow',
        #'Great Britain': 'purple',
        #'India': 'orange',
        #'Japan': 'pink',
        #'South Korea': 'lightgreen',
        #'Mexico': 'teal',
        #'Russia': 'gray',
        #'United States': 'darkblue'
    }
    # Create the scatter plot with 'comment_count' determining the size of the markers
    fig = px.scatter(df_combined, x='view_count', y='likes', color='Country', size='comment_count',
                 title='YouTube Trending Videos: View Count vs Likes by Country',
                 labels={'view_count': 'View Count (Millions)', 'likes': 'Likes (Millions)', 'comment_count': 'Comment Count'},
                 opacity=0.6,  # Adjust opacity here
                 color_discrete_map=color_map)
    # Show the figure
    #fig.show()
    
    
    # Convert the plot to HTML representation
    plot_html = fig.to_html(full_html=False)

    return plot_html
