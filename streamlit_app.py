import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from sqlalchemy import create_engine, text

# neon db postgres
DB_URL = st.secrets.get("DB_URL") or os.environ.get("DB_URL")
if not DB_URL:
    st.error("Database URL is not set. Please configure DB_URL in Streamlit secrets or as an environment variable.")
    st.stop()
    
engine = create_engine(DB_URL)
def run_query(query):
    with engine.connect() as conn:
        return pd.read_sql(text(query), conn)


# Mock data - replace with your actual data
trip_data = {
    'places': pd.DataFrame({
        'name': ['Paris', 'Rome', 'Barcelona', 'Amsterdam'],
        'lat': [48.8566, 41.9028, 41.3851, 52.3676],
        'lon': [2.3522, 12.4964, 2.1734, 4.9041],
        'spent': [1500, 1200, 1000, 800]
    }),
    'favorite_foods': ['Croissant', 'Pizza', 'Paella', 'Stroopwafel'],
    'expenses': pd.DataFrame({
        'category': ['Food', 'Hotels', 'Transportation', 'Activities'],
        'amount': [1500, 2000, 800, 700]
    }),
    'tips': 250,
    'servicio': 150,
    'hotel_charges': 2000
}

st.set_page_config(layout="wide")

st.title("Europe Trip Dashboard")

# Places Visited Map
st.subheader("Places Visited")
fig = px.scatter_mapbox(trip_data['places'], 
                        lat="lat", 
                        lon="lon", 
                        size="spent",  # This determines the size of the markers
                        color="spent",  # This colors the markers based on spending
                        hover_name="name", 
                        hover_data={"spent": True, "lat": False, "lon": False},
                        zoom=3, 
                        mapbox_style="open-street-map",
                        size_max=50,  # Maximum size of markers
                        color_continuous_scale=px.colors.sequential.Viridis)

fig.update_layout(mapbox_style="open-street-map")
fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})

st.plotly_chart(fig, use_container_width=True)

# Expenses Breakdown
col1, col2 = st.columns(2)

with col1:
    st.subheader("Expense Breakdown")
    # Changed from pie chart to bar chart
    fig = px.bar(trip_data['expenses'], x='category', y='amount', 
                 title='Expenses by Category',
                 labels={'amount': 'Amount Spent (€)', 'category': 'Category'},
                 color='category')
    fig.update_layout(showlegend=False)  # Hide legend as it's redundant for a bar chart
    st.plotly_chart(fig, use_container_width=True)

# Favorite Foods
with col2:
    st.subheader("Favorite Foods")
    for food in trip_data['favorite_foods']:
        st.write(f"- {food}")

# Additional Expenses
st.subheader("Additional Expenses")
additional_expenses = pd.DataFrame({
    'category': ['Tips', 'Servicio', 'Hotel Charges'],
    'amount': [trip_data['tips'], trip_data['servicio'], trip_data['hotel_charges']]
})
fig = px.bar(additional_expenses, x='category', y='amount')
st.plotly_chart(fig, use_container_width=True)

# Total Spent
total_spent = trip_data['expenses']['amount'].sum() + trip_data['tips'] + trip_data['servicio']
st.metric("Total Spent", f"€{total_spent}")

# Data Tables
st.subheader("Detailed Data")
tab1, tab2 = st.tabs(["Places", "Expenses"])

with tab1:
    st.dataframe(trip_data['places'])

with tab2:
    st.dataframe(trip_data['expenses'])
