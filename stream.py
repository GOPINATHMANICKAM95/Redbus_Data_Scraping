import streamlit as st
import pandas as pd
import sqlalchemy
from sqlalchemy import create_engine

# Connect to MySQL database
engine = sqlalchemy.create_engine("mysql+mysqlconnector://admin:gopi1234@gopids.c5ic8ayqm05z.ap-south-1.rds.amazonaws.com:3306/gopids")
query = "SELECT * FROM redbus_web1"
df = pd.read_sql(query, engine.connect())

# Set Streamlit page configuration
st.set_page_config(page_title="Redbus App", page_icon=':bus:', layout="wide", menu_items={'About': "mailto:gopinathmanickam95@gmail.com."})

# Sidebar filters
st.sidebar.header('Filters')

# Origin filter
origin_filter = st.sidebar.selectbox('Select From', options=[''] + list(df['Orgin'].unique()))

# Filter 'End' options based on selected 'Orgin'
if origin_filter:
    filtered_end_options = df[df['Orgin'] == origin_filter]['End'].unique()
else:
    filtered_end_options = df['End'].unique()

# End filter
end_filter = st.sidebar.selectbox('Select End', options=[''] + list(filtered_end_options))

# Seat type filter
seat_type_filter = st.sidebar.multiselect('Select Seat Type', options=[''] + list(df['Seat_Type'].unique()))

# AC type filter
ac_type_filter = st.sidebar.multiselect('Select AC Type', options=[''] + list(df['Actype'].unique()))

# Fare range filter
fare_range = st.sidebar.slider('Fare Range', float(df['fare'].min()), float(df['fare'].max()), (float(df['fare'].min()), float(df['fare'].max())))

# Rating range filter
rating_range = st.sidebar.slider('Rating Range', float(df['ratings'].min()), float(df['ratings'].max()), (float(df['ratings'].min()), float(df['ratings'].max())))

# Sort by filter
sort_by = st.sidebar.selectbox('Sort By', options=['fare', 'duration', 'ratings', 'starttime'], index=0)

# Bus ID filter
bus_ids = df['Bus_Mode'].unique()
selected_bus_ids = [bus_id for bus_id in bus_ids if st.sidebar.checkbox(f'Transport_Mode: {bus_id}')]

# Apply filters
df_filtered = df.copy()

if origin_filter:
    df_filtered = df_filtered[df_filtered['Orgin'] == origin_filter]

if end_filter:
    df_filtered = df_filtered[df_filtered['End'] == end_filter]

if selected_bus_ids:
    df_filtered = df_filtered[df_filtered['Bus_Mode'].isin(selected_bus_ids)]

if seat_type_filter:
    df_filtered = df_filtered[df_filtered['Seat_Type'].isin(seat_type_filter)]

if ac_type_filter:
    df_filtered = df_filtered[df_filtered['Actype'].isin(ac_type_filter)]

if fare_range:
    df_filtered = df_filtered[(df_filtered['fare'] >= fare_range[0]) & (df_filtered['fare'] <= fare_range[1])]

if rating_range:
    df_filtered = df_filtered[(df_filtered['ratings'] >= rating_range[0]) & (df_filtered['ratings'] <= rating_range[1])]

# Sort the data
df_filtered = df_filtered.sort_values(by=sort_by)

# Display the data
st.title("Redbus Application:")
st.dataframe(df_filtered[['route_Name', 'busname', 'starttime', 'endtime', 'duration', 'fare', 'seats', 'ratings']], use_container_width=True)
