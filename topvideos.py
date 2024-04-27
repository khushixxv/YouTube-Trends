import pandas as pd

# Paths to CSV files
file_paths = {
    'Brazil': '../archive/BR_youtube_trending_data.csv',
    'Canada': '../archive/CA_youtube_trending_data.csv',
    'Germany': '../archive/DE_youtube_trending_data.csv',
    'France': '../archive/FR_youtube_trending_data.csv',
    'Great Britain': '../archive/GB_youtube_trending_data.csv',
    'India': '../archive/IN_youtube_trending_data.csv',
    'Japan': '../archive/JP_youtube_trending_data.csv',
    'South Korea': '../archive/KR_youtube_trending_data.csv',
    'Mexico': '../archive/MX_youtube_trending_data.csv',
    'Russia': '../archive/RU_youtube_trending_data.csv',
    'United States': '../archive/US_youtube_trending_data.csv'
}

# Function to find the video with the most views in a dataset
def find_top_video(file_path):
    # Read the CSV file
    data = pd.read_csv(file_path)
    
    # Find the row with the maximum number of views
    max_views_row = data.loc[data['view_count'].idxmax()]
    
    return max_views_row

# Iterate through each country and find the top video
top_videos = {}
for country, path in file_paths.items():
    top_video = find_top_video(path)
    top_videos[country] = top_video

# Print the details of the top videos for each country
for country, video in top_videos.items():
    print(f"{country} - Video Title: {video['title']}, Channel: {video['channelTitle']}, Views: {video['view_count']}")
