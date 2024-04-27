import plotly.express as px
import pandas as pd

# Map abbreviations to full country names
country_names = {
    'BR': 'Brazil',
    'CA': 'Canada',
    'DE': 'Germany',
    'FR': 'France',
    'GB': 'Great Britain',
    'IN': 'India',
    'JP': 'Japan',
    'KR': 'South Korea',
    'MX': 'Mexico',
    'RU': 'Russia',
    'US': 'United States'
}

dfs= []
for country in ['BR', 'CA', 'DE', 'FR', 'GB', 'IN', 'JP', 'KR', 'MX', 'RU', 'US']:
    df = pd.read_csv(f'../archive/{country}_youtube_trending_data.csv')
    df = df[["video_id", "title", "view_count", "likes", "comment_count", "trending_date"]]
    df["country"] = country_names[country]
    df['trending_date'] = pd.to_datetime(df['trending_date'])
    df = df[df['trending_date'].dt.year == 2023]
    df = df.groupby('trending_date').head(75).reset_index()
    dfs.append(df)
df_combined = pd.concat(dfs)
df_combined['anim_frame'] = df_combined['trending_date'].dt.dayofyear

# Custom color map for countries
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
# Create the scatter plot with 'comment_count' determining the size of the markers
import plotly.express as px
import pandas as pd


fig = px.scatter(df_combined, x='view_count', y='likes', color='country', size='comment_count',
                title='2023 Trending Videos: View Count vs Likes by Country',
                labels={'title': 'Title', 'view_count': 'View Count (Millions)', 'likes': 'Likes (Millions)', 'comment_count': 'Comment Count'},
                opacity=0.6,  # Adjust opacity here
                color_discrete_map=color_map, 
                log_x=True,
                log_y=True,
                animation_frame='anim_frame')

# Remove the white border from each node
fig.update_traces(marker=dict(line=dict(width=0)))

fig.show()



# Save as an interactive HTML file named "scatterplot_brazil_canada.html"
fig.write_html('static/scatterplot.html')


