import streamlit as st
import pandas as pd
import sqlalchemy
from sqlalchemy import create_engine
import mysql.connector


engine = sqlalchemy.create_engine("mysql+mysqlconnector://admin:redbus123@redbus.c5ic8ayqm05z.ap-south-1.rds.amazonaws.com:3306/redbus")
# Load the data

query = "SELECT * FROM new"

df = pd.read_sql(query, engine.connect())

# Sidebar filters
st.sidebar.header('Filters')

# Origin filter
origin_filter = st.sidebar.multiselect('Select From', df['Orgin'].unique())

# End filter
end_filter = st.sidebar.multiselect('Select End', df['End'].unique())

# Bus ID filter
bus_id_filter = st.sidebar.checkbox('Filter by Bus ID')
selected_bus_ids = None
if bus_id_filter:
    selected_bus_ids = st.sidebar.multiselect('Select Bus ID', df['Bus_Id'].unique())

# Seat type filter
seat_type_filter = st.sidebar.multiselect('Select Seat Type', df['Seat_Type'].unique())

# AC type filter
ac_type_filter = st.sidebar.multiselect('Select AC Type', df['Actype'].unique())

# Fare range filter
fare_range = st.sidebar.slider('Fare Range', float(df['fare'].min()), float(df['fare'].max()), (float(df['fare'].min()), float(df['fare'].max())))

# Rating range filter
rating_range = st.sidebar.slider('Rating Range', float(df['ratings'].min()), float(df['ratings'].max()), (float(df['ratings'].min()), float(df['ratings'].max())))

# Sort by filter
sort_by = st.sidebar.selectbox('Sort By', options=['fare', 'duration', 'ratings', 'starttime'], index=0)

# Apply filters
filtered_df = df.copy()

if origin_filter:
    filtered_df = filtered_df[filtered_df['Orgin'].isin(origin_filter)]

if end_filter:
    filtered_df = filtered_df[filtered_df['End'].isin(end_filter)]

if selected_bus_ids:
    filtered_df = filtered_df[filtered_df['Bus_Id'].isin(selected_bus_ids)]

if seat_type_filter:
    filtered_df = filtered_df[filtered_df['Seat_Type'].isin(seat_type_filter)]

if ac_type_filter:
    filtered_df = filtered_df[filtered_df['Actype'].isin(ac_type_filter)]

if fare_range:
    filtered_df = filtered_df[(filtered_df['fare'] >= fare_range[0]) & (filtered_df['fare'] <= fare_range[1])]

if rating_range:
    filtered_df = filtered_df[(filtered_df['ratings'] >= rating_range[0]) & (filtered_df['ratings'] <= rating_range[1])]

# Sort the data
filtered_df = filtered_df.sort_values(by=sort_by)

# Display the data
st.title('Bus Schedule and Fare Information')
st.dataframe(filtered_df[['route_Name','busname', 'bus_desc', 'starttime', 'endtime', 'duration', 'fare', 'seats','ratings']],use_container_width=True)

filtered_df = filtered_df.head(50)