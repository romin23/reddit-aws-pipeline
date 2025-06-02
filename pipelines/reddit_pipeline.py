from utils.constants import CLIENT_ID, SECRET, OUTPUT_PATH
from etls.reddit_etl import connect_reddit, posts_extract, transform_data, load_df_to_csv
import pandas as pd

def reddit_pipeline(file_name:str, subreddit:str, time_filter='day', limit=None):
    # connection to redit
    rdt_instance = connect_reddit(CLIENT_ID, SECRET, 'Airscholar Agent')
    # extraction od data
    posts = posts_extract(rdt_instance, subreddit, time_filter, limit)
    post_df = pd.DataFrame(posts)
    # transforming data
    post_df = transform_data(post_df) 
    # loding in csv 
    data_path = f'{OUTPUT_PATH}/{file_name}.csv'
    load_df_to_csv(post_df, data_path)
    return data_path
