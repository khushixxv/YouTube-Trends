import pandas as pd
import plotly.express as px

# Load the data from the CSV file
data = pd.read_csv('../archive/KR_youtube_trending_data.csv')

# Convert the trending_date to datetime format and extract the year
data['trending_date'] = pd.to_datetime(data['trending_date'], format='%Y-%m-%dT%H:%M:%SZ')
data['year'] = data['trending_date'].dt.year

# Group the data by channel and year, and count the number of videos for each
grouped_data = data.groupby(['channelId', 'channelTitle', 'year']).size().reset_index(name='video_count')

# Now, aggregate the counts to find the top 10 channels overall
channel_totals = grouped_data.groupby(['channelId', 'channelTitle']).sum().reset_index()
top_channels = channel_totals.nlargest(10, 'video_count')['channelId']

# Filter the grouped data to only include the top 10 channels
top_channel_data = grouped_data[grouped_data['channelId'].isin(top_channels)]

# Create the animated bar chart
fig = px.bar(top_channel_data, 
             x='channelTitle', 
             y='video_count', 
             color='channelTitle', 
             animation_frame='year', 
             animation_group='channelTitle', 
             labels={'video_count': 'Number of Trending Videos'},
             title='Number of Trending Videos Per Year for Top South Korea Channels')

fig.layout.updatemenus[0].buttons[0].args[1]['frame']['duration'] = 800
fig.show()

# Save the figure as an HTML file
fig.write_html("top_channels_KR.html")
