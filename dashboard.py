import streamlit as st
import pandas as pd
import sqlite3
import matplotlib.pyplot as plt


@st.cache_data
def load_data():
    conn = sqlite3.connect("WS_results.db")
    df = pd.read_sql_query("SELECT * FROM WS_results", conn)
    conn.close()
    return df


df = load_data()

# Basic text elements
# Adds a big title at the top of the app
st.title("Elina's World Series POV via Python!")
# Adds a section header — good for breaking content into parts
st.header("Scroll through these mindblowing- er, historic results:")

# scroll through any year range you want
st.sidebar.title("Elina's filters")
year_min, year_max = df["Year"].min(), df["Year"].max()
year_range = st.sidebar.slider(
    "Select Year Range", year_min, year_max, (2000, year_max))


# series winner by year
def get_winner(row):
    return row["Team1"] if row["Score1"] > row["Score2"] else row["Team2"]


# dropdown list of teams
teams = sorted(set(df["Team1"]) | set(df["Team2"]))
team_filter = st.sidebar.selectbox("", ["All"] + teams)

# year range
filtered_df = df[(df["Year"] >= year_range[0]) & (df["Year"] <= year_range[1])]
if team_filter != "All":
    filtered_df = filtered_df[(filtered_df["Team1"] == team_filter) | (
        filtered_df["Team2"] == team_filter)]


filtered_df["Winner"] = filtered_df.apply(get_winner, axis=1)

# bar chart of wins by team

st.subheader("🏆 World Series Wins by Team")
wins = filtered_df["Winner"].value_counts().reset_index()
wins.columns = ["Team", "Wins"]

fig1, ax1 = plt.subplots()
ax1.bar(wins["Team"], wins["Wins"])
plt.xticks(rotation=45)
st.pyplot(fig1)


# dot plot of appearances
st.subheader("📈 Team Appearances Over Time")

appearances = pd.concat([
    filtered_df[["Team1"]].rename(columns={"Team1": "Team"}),
    filtered_df[["Team2"]].rename(columns={"Team2": "Team"})
])
team_counts = appearances["Team"].value_counts().reset_index()
team_counts.columns = ["Team", "Appearances"]
team_counts = team_counts.sort_values("Appearances")  # Sort for visual clarity

# Plot:
fig, ax = plt.subplots(figsize=(8, len(team_counts) * 0.3))
ax.scatter(team_counts["Appearances"], team_counts["Team"], s=100)

ax.set_xlabel("Number of Appearances")
ax.set_ylabel("Team")
ax.set_title("World Series Appearances by Team")

st.pyplot(fig)

# scrollable, filtered table
st.subheader("📋 Filtered World Series Results")
st.dataframe(
    filtered_df[["Year", "Team1", "Score1", "Team2", "Score2", "Winner"]])
