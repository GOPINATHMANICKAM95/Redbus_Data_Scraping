import streamlit as st
import pandas as pd
import sqlalchemy
from sqlalchemy import create_engine
import plotly.express as px
import plotly.graph_objects as go


engine = sqlalchemy.create_engine("mysql+mysqlconnector://admin:gopi1234@gopids.c5ic8ayqm05z.ap-south-1.rds.amazonaws.com:3306/gopids")
query = "SELECT * FROM redbus_web1"
df = pd.read_sql(query, engine.connect())

#set wise node is always on
st.set_page_config(page_title="redbus app",page_icon =':bus:',layout="wide",menu_items={'About':"mailto:gopinathmanickam95@gmail.com."})



# Sidebar filters
st.sidebar.header('Filters')

# Origin filter
origin_filter = st.sidebar.multiselect('Select From', df['Orgin'].unique())

# End filter
end_filter = st.sidebar.multiselect('Select End', df['End'].unique())  

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

# Bus ID filter

bus_ids = df['Bus_Id'].unique()
selected_bus_ids = []
for bus_id in bus_ids:
    if st.sidebar.checkbox(f'Bus ID: {bus_id}'):
        selected_bus_ids.append(bus_id)

# Apply filters
df = df.copy()

if origin_filter:
    df = df[df['Orgin'].isin(origin_filter)]

if end_filter:
    df = df[df['End'].isin(end_filter)]

if selected_bus_ids:
    df = df[df['Bus_Id'].isin(selected_bus_ids)]

if seat_type_filter:
    df = df[df['Seat_Type'].isin(seat_type_filter)]

if ac_type_filter:
    df = df[df['Actype'].isin(ac_type_filter)]

if fare_range:
    df = df[(df['fare'] >= fare_range[0]) & (df['fare'] <= fare_range[1])]

if rating_range:
    df = df[(df['ratings'] >= rating_range[0]) & (df['ratings'] <= rating_range[1])]




# Sort the data
df = df.sort_values(by=sort_by)

st.title("Bus Schedule and Fare Information")

# Display the data
st.dataframe(df[['route_Name','busname', 'starttime', 'endtime', 'duration', 'fare', 'seats','ratings']],use_container_width=True)



