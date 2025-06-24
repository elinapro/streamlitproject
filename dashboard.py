import streamlit as st
import pandas as pd
import sqlite3
import matplotlib.pyplot as plt
from dash import dash_table, Dash, html


app = Dash(__name__)
server = app.server


@st.cache_data
def load_data():
    conn = sqlite3.connect("WS_results.db")
    df = pd.read_sql_query("SELECT * FROM WS_results", conn)
    conn.close()
    return df


df = load_data()

# Basic text elements
st.title("Elina's World Series POV")  # Adds a big title at the top of the app
# Adds a section header — good for breaking content into parts
st.header("Enjoy my results below:")


st.sidebar.title("Elina's World Series filters")
year_min, year_max = df["Year"].min(), df["Year"].max()
year_range = st.sidebar.slider(
    "Select Year Range", year_min, year_max, (2000, year_max))

# dropdown list of teams
teams = sorted(set(df["Team1"]) | set(df["Team2"]))
team_filter = st.sidebar.selectbox("Select Team (optional)", ["All"] + teams)

# year range
filtered_df = df[(df["Year"] >= year_range[0]) & (df["Year"] <= year_range[1])]
if team_filter != "All":
    filtered_df = filtered_df[(filtered_df["Team1"] == team_filter) | (
        filtered_df["Team2"] == team_filter)]


# series winner by year
def get_winner(row):
    return row["Team1"] if row["Score1"] > row["Score2"] else row["Team2"]


filtered_df["Winner"] = filtered_df.apply(get_winner, axis=1)

# bar chart of wins by team

st.subheader("🏆 World Series Wins by Team")
wins = filtered_df["Winner"].value_counts().reset_index()
wins.columns = ["Team", "Wins"]

fig1, ax1 = plt.subplots()
ax1.bar(wins["Team"], wins["Wins"])
plt.xticks(rotation=45)
st.pyplot(fig1)


# line chart of appearances
st.subheader("📈 Team Appearances Over Time")
appearances = pd.concat([
    filtered_df[["Year", "Team1"]].rename(columns={"Team1": "Team"}),
    filtered_df[["Year", "Team2"]].rename(columns={"Team2": "Team"})
])
# one column

timeline = appearances.groupby(["Year", "Team"]).size().unstack(fill_value=0)

fig2, ax2 = plt.subplots()
timeline.plot(ax=ax2)
plt.title("Appearances Over Time")
plt.ylabel("Appearances")
st.pyplot(fig2)

# scrollable, filtered table
st.subheader("📋 Filtered World Series Results")
st.dataframe(
    filtered_df[["Year", "Team1", "Score1", "Team2", "Score2", "Winner"]])
