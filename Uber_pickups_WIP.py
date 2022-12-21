#Source:
##1. https://github.com/streamlit/streamlit/blob/develop/docs/tutorial/create_a_data_explorer_app.md
##2. https://docs.streamlit.io/_/downloads/en/stable/pdf/

# Step 1
import streamlit as st
import pandas as pd
import numpy as np

# Step 2 -- Page Title
st.title('Uber pickups in NYC')

# Step 3 - Download data
#-----------------------
DATE_COLUMN = 'date/time'
DATA_URL = ('https://s3-us-west-2.amazonaws.com/'
         'streamlit-demo-data/uber-raw-data-sep14.csv.gz')

# Step 4: Create function
#-----------------------
#@st.cache #add this later
@st.cache
def load_data(nrows):
    data = pd.read_csv(DATA_URL, nrows=nrows)
    lowercase = lambda x: str(x).lower()
    data.rename(lowercase, axis='columns', inplace=True)
    data[DATE_COLUMN] = pd.to_datetime(data[DATE_COLUMN])
    return data

# Step 5: Output sample
#-----------------------
#@st.cache #add this later
# Create a text element and let the reader know the data is loading.
data_load_state = st.text('Loading data...')
# Load 10,000 rows of data into the dataframe.
data = load_data(151000)
# Notify the reader that the data was successfully loaded.
data_load_state.text('Loading data...done!')

# Step 6: Let's Cache the data
#-----------------------------
data_load_state.text("Done! (using st.cache)")

# Step 7: Inspect raw data
#-----------------------------
#st.subheader('Raw data')
#st.write(data)

if st.checkbox('Show raw data'):
    st.subheader('Raw data')
    st.write(data)

# Step 8: Draw histogram
#-----------------------------

st.subheader('Number of pickups by hour')

hist_values = np.histogram(
    data[DATE_COLUMN].dt.hour, bins=24, range=(0,24))[0]

st.bar_chart(hist_values) #display chart

# Step 9a: Draw a Map
#-----------------------------

# Simple approach
st.subheader('Map of all pickups')
st.map(data)


# Step 9b: Draw a Map w/ filter
#------------------------------------
#hour_to_filter = 18
#hour_to_filter = st.slider('hour', 0, 23, 17)  # min: 0h, max: 23h, default: 17h
hour_to_filter = st.sidebar.slider('hour', 0, 23, 17)  # min: 0h, max: 23h, default: 17h
#hour_to_filter = 2
filtered_data = data[data[DATE_COLUMN].dt.hour == hour_to_filter]
st.subheader(f'Map of all pickups at {hour_to_filter}:00')
st.map(filtered_data)


## Step 10: Create Sidebar
#--------------------------------
# Add a slider to the sidebar:
add_slider = st.sidebar.slider(
    'Select a range of values',
    0.0, 100.0, (25.0, 75.0)
)
