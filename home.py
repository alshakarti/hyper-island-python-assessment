# importing necessary libraries
import streamlit as st

# importing necessary functions from src
from src.data_loading import (
    bigquery_authenticate,
    load_data
)
from src.data_processing import (
    drop_duplicates,
    convert_to_datetime,
    merge_chart_audio_features,
    aggregate_audio_features,
    merge_chart_track_features,
    aggregate_track_features,
    select_spotify_tracks,
    prepare_artist_data,
)
from src.data_processing import (
    convert_to_datetime,
    get_trending_artists
)

# customizing the page
st.set_page_config(
    page_title="What Makes A Hit Song",
    page_icon=":guitar:",
    layout="wide", 
    initial_sidebar_state="expanded"
)

@st.cache_data   
def load_and_cache(): 
    client = bigquery_authenticate()  
    
    # loading data from bigquery
    audio_features = load_data(client,'audio_features')
    chart_positions = load_data(client, 'chart_positions')
    tracks = load_data(client, 'tracks')
    mapping = load_data(client, 'tracks_artists_mapping')
    artists = load_data(client, 'artists')

    # cleaning data from bigquery
    audio_features_clean = drop_duplicates(audio_features)
    tracks_clean = drop_duplicates(tracks)
    chart_positions_clean = convert_to_datetime(chart_positions)
    artist_track_ = prepare_artist_data(tracks, mapping, artists)
    
    # getting trending artists 
    trending_artists = get_trending_artists(tracks, mapping, artists, chart_positions)

    # merging and cleaning tables to get all necessary field for app
    first_merge = merge_chart_audio_features(chart_positions_clean, audio_features_clean)
    second_merge = merge_chart_track_features(first_merge, tracks_clean)

    # aggregate tables for app
    audio_df = aggregate_audio_features(first_merge)
    track_df = aggregate_track_features(second_merge)
    spotify_df = select_spotify_tracks(second_merge)
    
    return audio_df, track_df, spotify_df, mapping, artists, artist_track_, audio_features, trending_artists


audio_df, track_df, spotify_songs, mapping, artists, artist_track_, audio_features, trending_artists = load_and_cache()