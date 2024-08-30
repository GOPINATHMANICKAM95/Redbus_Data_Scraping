import streamlit as st
import pandas as pd
from sqlalchemy import create_engine, text
import plotly.express as px
# Set Streamlit page configuration
st.set_page_config(page_title="Redbus App", page_icon=':bus:', layout="wide", menu_items={'About': "mailto:gopinathmanickam95@gmail.com."})
# Sidebar for page navigation
st.sidebar.title("Navigation")
page = st.sidebar.selectbox("Select a page", ["Introduction", "Project"])
if page == "Introduction":
    st.title("Project Approach")
    st.write("""
    **Step 1: Understanding the Website**
    - Analyze the website's DOM structure using browser developer tools to identify key elements, classes, and IDs. This foundational step allows efficient automated scraping based on our SQL schema.

    **Step 2: Data Scraping**
    - Python code was used to scrape all necessary details. It took 4 minutes to scrape route names and links, and 222 minutes to scrape all the data for bus details in the specified schema.

    **Step 3: Push to Pandas for Cleaning**
    - The scraped data was stored in Excel for future reference as raw data. It was then processed using Pandas for cleaning, splitting, merging, changing data types, and removing whitespace.
    
    **Step 4: Push the Data to SQL**
    - The cleaned data was pushed to AWS RDS for scalable and secure storage using SQLAlchemy.
    
    **Step 5: Retrieve and Streamlit**
    - The data was retrieved from SQL and visualized in a Streamlit app with interactive filtering and graphing features, using Plotly Express for advanced visualizations.
    
    **Step 6: Tools Used**:
    - 🐍 **Python**
    - 🚗 **Selenium**
    - 📊 **Pandas**
    - 💾 **MySQL**
    - ☁️ **AWS**
    - 🎛️ **Streamlit**

    **Author:**
    - **Name**: M. Gopinath
    - **Education**: BE (EEE)
    - **LinkedIn**: [Gopinath Manickam](https://www.linkedin.com/in/gopinath-manickam-49aa06104/)
    - **Email**: gopinathmanikcam95@gmail.com
    - **GitHub**: [Gopinath Manickam](https://github.com/GOPINATHMANICKAM95)
""")

elif page == "Project":
    st.title("Redbus App")
    # Connect to MySQL database
    engine = create_engine("mysql+mysqlconnector://admin:gopi1234@gopids.c5ic8ayqm05z.ap-south-1.rds.amazonaws.com:3306/redbus")
    # Load the entire dataset initially to populate filters
    with engine.connect() as conn:
        initial_query = "SELECT * FROM redbus"
        df = pd.read_sql(text(initial_query), conn)
    state_filter = st.sidebar.selectbox('Select state', options=[''] + list(df['state'].unique()))
    # Bus ID filter
    st.sidebar.write('Transport Mode')
    selected_bus_ids = [bus_id for bus_id in df['transport_mode'].unique() if st.sidebar.checkbox(bus_id)]
    # Sidebar filters
    st.sidebar.header('Filters')
    # Horizontal layout for "From" and "To" filters
    col1, col2 = st.columns(2)
    filtered_df = df[df['transport_mode'].isin(selected_bus_ids)] if selected_bus_ids else df
    # Generate transport options
    rtc_options = [''] + list(filtered_df['transport'].unique())
    # Create the selectbox for transport types
    rtc_filter = st.selectbox('Select transportType', options=rtc_options)
    # "From" filter
    with col1:
        origin_filter = st.selectbox('From', options=[''] + list(df['from'].unique()))
    # "To" filter
    with col2:
        end_filter = st.selectbox('To', options=[''] + list(df[df['from'] == origin_filter]['to'].unique()) )
    # Seat type filter
    seat_type_filter = st.sidebar.multiselect('Select Seat Type', options=df['Seat_Type'].unique())
    # AC type filter
    ac_type_filter = st.sidebar.multiselect('Select AC Type', options=df['Actype'].unique())
    # Fare range filter
    fare_range = st.sidebar.slider('Fare Range', min_value=float(df['price'].min()), max_value=float(df['price'].max()), value=(float(df['price'].min()), float(df['price'].max())))
    # Rating range filter
    rating_range = st.sidebar.slider('Rating Range', min_value=float(df['star_rating'].min()), max_value=float(df['star_rating'].max()), value=(float(df['star_rating'].min()), float(df['star_rating'].max())))
    # Sort by filter
    sort_by = st.sidebar.selectbox('Sort By', options=['price',"dur_in_min", 'star_rating', 'departing_time'], index=0)
    # Start building the SQL query based on filters
    base_query = "SELECT * FROM redbus WHERE 1=1"
    if origin_filter:
        base_query += f" AND `from` = '{origin_filter}'"
    if end_filter:
        base_query += f" AND `to` = '{end_filter}'"
    if rtc_filter:
        base_query += f" AND transport= '{rtc_filter}'"
    if seat_type_filter:
        seat_type_filter_str = "','".join(seat_type_filter)
        base_query += f" AND Seat_Type IN ('{seat_type_filter_str}')"
    if ac_type_filter:
        ac_type_filter_str = "','".join(ac_type_filter)
        base_query += f" AND Actype IN ('{ac_type_filter_str}')"
    if state_filter:
        base_query += f" AND state = '{state_filter}'"
    if selected_bus_ids:
        selected_bus_ids_str = "','".join(selected_bus_ids)
        base_query += f" AND transport_Mode IN ('{selected_bus_ids_str}')"
    # Add fare range filter
    base_query += f" AND price BETWEEN {fare_range[0]} AND {fare_range[1]}"
    # Add rating range filter
    base_query += f" AND star_rating BETWEEN {rating_range[0]} AND {rating_range[1]}"
    # Add sorting
    base_query += f" ORDER BY {sort_by}"
    # Execute the SQL query
    with engine.connect() as conn:
        df_filtered = pd.read_sql(text(base_query), conn)
    summary = df_filtered.groupby('transport_mode').agg(
        Total_Buses=('transport_mode', 'count'),
        Seater=('Seat_Type', lambda x: (x == 'Seater').sum()),
        Push_Back=('Seat_Type', lambda x: (x == 'Push Back').sum()),
        Sleeper=('Seat_Type', lambda x: (x == 'Sleeper').sum()),
        Seater_Sleeper=('Seat_Type', lambda x: (x == 'Seater / Sleeper').sum()),
        Semi_Sleeper=('Seat_Type', lambda x: (x == 'Semi Sleeper').sum()),
        Semi_Sleeper_Sleeper=('Seat_Type', lambda x: (x == 'Semi Sleeper / Sleeper').sum()),
        AC=('Actype', lambda x: (x == 'AC').sum()),
        Non_AC=('Actype', lambda x: (x == 'Non-AC').sum()),
        Avg_Price=('price', 'mean'),
        Price_From=('price', 'min'),
        Price_To=('price', 'max'),
        Avg_Rating=('star_rating', 'mean'),
        Max_Rating=('star_rating', 'max'),
        Total_Seats=('seats_available','sum')
    ).reset_index()
    # Add a new column 'S.No' starting from 1
    summary.index = summary.index + 1
    summary.reset_index(inplace=True)
    summary.rename(columns={'index': 'S.No'}, inplace=True)
    # Add a total row to the summary
    total_row = pd.DataFrame({
        'S.No': ['Total'],
        'transport_mode': ['All'],
        'Total_Buses': [summary['Total_Buses'].sum()],
        'Seater': [summary['Seater'].sum()],
        'Push_Back': [summary['Push_Back'].sum()],
        'Sleeper': [summary['Sleeper'].sum()],
        'Seater_Sleeper': [summary['Seater_Sleeper'].sum()],
        'Semi_Sleeper': [summary['Semi_Sleeper'].sum()],
        'Semi_Sleeper_Sleeper': [summary['Semi_Sleeper_Sleeper'].sum()],
        'AC': [summary['AC'].sum()],
        'Non_AC': [summary['Non_AC'].sum()],
        'Avg_Price': [summary['Avg_Price'].mean()],
        'Price_From': [summary['Price_From'].min()],
        'Price_To': [summary['Price_To'].max()],
        'Avg_Rating': [summary['Avg_Rating'].mean()],
        'Max_Rating': [summary['Max_Rating'].max()],
        'Total_Seats': [summary['Total_Seats'].sum()]
    })
    # Use pd.concat to add the total row
    summary = pd.concat([summary, total_row], ignore_index=True)
    # Display the insights table
    st.title("Insights Table")
    st.dataframe(summary, use_container_width=True)
      # Exclude the "Total" row for plotting
    summary_no_total = summary[summary['S.No'] != 'Total']
    df_grouped = df_filtered.groupby(['transport_mode', 'Seat_Type', 'Actype']).size().reset_index(name='counts')
    bus_count_df = df_filtered.groupby(['from', 'to']).size().reset_index(name='Bus Count')
    fig5 = px.bar(bus_count_df, x='from', y='Bus Count', color='to', barmode='group',
            labels={'from': 'From Location', 'Bus Count': 'Number of Buses', 'to': 'To Location'},
            title="Number of Buses by Route")
    st.plotly_chart(fig5)
    c1, c2,c3,c4,c5= st.columns(5)
    with c1:
        # Create a pie chart for the distribution of transport modes
        fig = px.sunburst(df_grouped,path=['transport_mode', 'Seat_Type',"Actype"],values='counts',title='Distribution_of_Bus')
        st.plotly_chart(fig)
    with c2:
        fig2 = px.bar(summary_no_total,x='transport_mode', y='Avg_Price', text='Avg_Price', title='Average Price')
        fig2.update_traces(textposition='auto')
        fig2.update_layout(xaxis_title='Transport Mode', yaxis_title='Average Price')
        st.plotly_chart(fig2)
    # Bar chart for average ratings by transport mode
    with c3:
        fig3 = px.bar(summary_no_total,x='transport_mode', y='Avg_Rating', text='Avg_Rating', title='Average Rating')
        fig3.update_traces(textposition='auto')
        fig3.update_layout(xaxis_title='Transport Mode', yaxis_title='Average Rating')
        st.plotly_chart(fig3)
    with c4:
        fig4 = px.bar(summary_no_total,x='transport_mode', y='Total_Seats', text='Total_Seats', title='Seat_Count')
        fig4.update_traces(textposition='auto')
        fig4.update_layout(xaxis_title='Transport Mode', yaxis_title='Total_Seats')
        st.plotly_chart(fig4)
    with c5:
        fig4 = px.bar(summary_no_total,x='transport_mode', y='Total_Buses', text='Total_Buses', title='Bus_Count')
        fig4.update_traces(textposition='auto')
        fig4.update_layout(xaxis_title='Transport Mode', yaxis_title='Total_Buses')
        st.plotly_chart(fig4)

    st.title("Filtered Bus Data")
    st.dataframe(df_filtered[['from','to','busname', 'departing_time', 'reaching_time', 'duration', 'price', 'seats_available','Seat_Type','Actype', 'star_rating']], use_container_width=True)
