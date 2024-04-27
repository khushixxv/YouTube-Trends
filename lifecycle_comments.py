import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import json

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
    df = df[["video_id", "title", "comment_count", "trending_date"]]
    df["country"] = country_names[country]
    dfs.append(df)

df_combined = pd.concat(dfs)

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

# Concatenate all the DataFrames
# get year/month
df_combined['trending_date'] = pd.to_datetime(df_combined['trending_date'])
df_combined = df_combined[df_combined['trending_date'].dt.year == 2023]
# df_combined['trending_date'] = df_combined['trending_date'].dt.month

df_combined = df_combined.groupby(['video_id', 'trending_date']).agg({
    'country': lambda x: list(set(x)),
    'comment_count': 'mean',
    'title': 'first',
}).head(20000).reset_index()

print(df_combined[50:75])

df_combined = df_combined.groupby('video_id').apply(lambda x: x.sort_values('trending_date')).reset_index(drop=True)
# df_combined['days_past_first'] = df_combined['trending_date'].transform(lambda x: (x - x.min()).dt.days)
# df_combined['view_count_change'] = df_combined['view_count'].diff()
# df_combined['view_count_change'] = df_combined['view_count_change'].fillna(0)
# print(df_combined[["video_id", "days_past_first", "view_count_change"]])

# df_processed = df_combined[["video_id", "title", "view_count", "trending_date", "country"]].reset_index(drop=True)
# print(df_combined.groupby('video_id').get_group(df_combined.groupby('video_id').groups.keys()))
# print(df_combined[50:75])
grouped = df_combined.groupby('video_id')#.drop('video_id', axis=1)
# print(df_combined[50:75])
# print('abt to sort and...')
count = 0
fig = go.Figure()
for name, group in grouped:
    count+=1
    # if count == 1000:
    #     break
    # print(group[['title', 'days_past_first', 'view_count_change']])
    # group = group.apply(lambda x: x.sort_values('trending_date')) # .reset_index(drop=True)
    # group = group.sort_values('trending_date')
    # print(group)
    for row in group:
        group['days_past_first'] = group['trending_date'].transform(lambda x: (x - x.min()).dt.days)
        group['comment_count_change'] = group['comment_count'].diff()
    
    # print(group['title'])

    fig.add_trace(go.Scatter(
        x=group['days_past_first'], 
        y=group['comment_count_change'], 
        mode='lines', 
        line=dict(color=color_map[group['country'].iloc[0][0]]), 
        name=group['title'].iloc[0][0:25] + "...",
        hovertemplate =
            '<i>Days past first</i>: %{x}<br>'+
            '<b>Comment count change</b>: %{y}<br>',
            # '<b>Video ID</b>: %{name} <br>' +
            # '<b>Countries Trending</b>: %{text}<br>',
        text=group['country'].iloc[0]
        ))
        
    fig.update_layout(
        title="Video Life Cycle Analysis - COMMENTS",
        xaxis_title="Day Trending",
        yaxis_title="Rate of Change in Comments",
        legend_title="Video Title",
    )

# fig = px.line(df_combined, x='days_past_first', y='view_count_change', color='video_id')
# fig.update_layout(title='View Count Change Over Time by Video ID')
# fig.update_xaxes(title='Days Trending')
# fig.update_yaxes(title='View Count Change')

fig.show()

fig.write_html('static/lifecycle_comments.html')