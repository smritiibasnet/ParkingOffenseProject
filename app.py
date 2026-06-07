import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="Parking Tickets Dashboard",
    layout="wide"
)

# Load data
@st.cache_data
def load_data():
    df = pd.read_csv("clean_parking_tickets.csv")
    df["ticket_start_time"] = pd.to_datetime(df["ticket_start_time"])
    df["ticket_end_time"] = pd.to_datetime(df["ticket_end_time"])
    return df

df = load_data()

st.title("Parking Tickets Interactive Dashboard")
st.write("This dashboard provides a big-picture overview of parking ticket patterns and allows filtering by district, street, state, vehicle make, and offense type.")

# Sidebar filters
st.sidebar.header("Filter Options")

district_options = ["All"] + sorted(df["district"].dropna().unique().tolist())
selected_district = st.sidebar.selectbox("Select District", district_options)

street_options = ["All"] + sorted(df["street"].dropna().unique().tolist())
selected_street = st.sidebar.selectbox("Select Street", street_options)

state_options = ["All"] + sorted(df["state"].dropna().unique().tolist())
selected_state = st.sidebar.selectbox("Select Vehicle State", state_options)

offense_options = ["All"] + sorted(df["offense_description"].dropna().unique().tolist())
selected_offense = st.sidebar.selectbox("Select Offense Type", offense_options)

# Apply filters
filtered_df = df.copy()

if selected_district != "All":
    filtered_df = filtered_df[filtered_df["district"] == selected_district]

if selected_street != "All":
    filtered_df = filtered_df[filtered_df["street"] == selected_street]

if selected_state != "All":
    filtered_df = filtered_df[filtered_df["state"] == selected_state]

if selected_offense != "All":
    filtered_df = filtered_df[filtered_df["offense_description"] == selected_offense]

# Big picture metrics
st.subheader("Big Picture Summary")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Total Tickets", f"{len(filtered_df):,}")

with col2:
    st.metric("Total Ticket Amount", f"${filtered_df['ticket_amount'].sum():,.0f}")

with col3:
    st.metric("Average Ticket Amount", f"${filtered_df['ticket_amount'].mean():.2f}")

with col4:
    st.metric("Unique Streets", f"{filtered_df['street'].nunique():,}")

# Charts
st.subheader("Ticket Trends and Patterns")

col1, col2 = st.columns(2)

with col1:
    tickets_by_district = filtered_df["district"].value_counts().reset_index()
    tickets_by_district.columns = ["district", "ticket_count"]

    fig_district = px.bar(
        tickets_by_district,
        x="district",
        y="ticket_count",
        title="Tickets by District",
        labels={"district": "District", "ticket_count": "Number of Tickets"}
    )
    st.plotly_chart(fig_district, use_container_width=True)

with col2:
    tickets_by_month = filtered_df.groupby("ticket_month").size().reset_index(name="ticket_count")

    fig_month = px.line(
        tickets_by_month,
        x="ticket_month",
        y="ticket_count",
        markers=True,
        title="Tickets by Month",
        labels={"ticket_month": "Month", "ticket_count": "Number of Tickets"}
    )
    st.plotly_chart(fig_month, use_container_width=True)

col3, col4 = st.columns(2)

with col3:
    top_streets = filtered_df["street"].value_counts().head(10).reset_index()
    top_streets.columns = ["street", "ticket_count"]

    fig_street = px.bar(
        top_streets,
        x="ticket_count",
        y="street",
        orientation="h",
        title="Top 10 Streets by Ticket Count",
        labels={"street": "Street", "ticket_count": "Number of Tickets"}
    )
    st.plotly_chart(fig_street, use_container_width=True)

with col4:
    top_offenses = filtered_df["offense_description"].value_counts().head(10).reset_index()
    top_offenses.columns = ["offense_description", "ticket_count"]

    fig_offense = px.bar(
        top_offenses,
        x="ticket_count",
        y="offense_description",
        orientation="h",
        title="Top 10 Offense Types",
        labels={"offense_description": "Offense Description", "ticket_count": "Number of Tickets"}
    )
    st.plotly_chart(fig_offense, use_container_width=True)

# Map
st.subheader("Ticket Locations Map")

map_df = filtered_df.dropna(subset=["latitude", "longitude"])

if not map_df.empty:
    st.map(map_df[["latitude", "longitude"]])
else:
    st.write("No location data available for the selected filters.")

# Detailed ticket table
st.subheader("Detailed Ticket Information")

st.dataframe(
    filtered_df[
        [
            "ticket_number",
            "district",
            "street",
            "ticket_start_time",
            "state",
            "vehicle_make",
            "offense_code",
            "offense_description",
            "ticket_amount"
        ]
    ],
    use_container_width=True
)