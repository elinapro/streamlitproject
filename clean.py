import pandas as pd

# load the uncleaned CSV
df = pd.read_csv("WS_results.csv", header=None)

# Drop unwanted rows (labels, future placeholders, invalid data)
df = df[~df[0].str.contains(
    "World Series,National League|To Be Determined|x Game Series", na=False)]

# Rename the first column from Title to Year
df.columns = ["Title", "Team1", "Score1", "Team2", "Score2"]
df["Year"] = df["Title"].str.extract(r"(\d{4})")
# Drop rows where year couldn't be extracted
df = df.dropna(subset=["Year"])
# Convert to integer
df["Year"] = df["Year"].astype(int)

# Clean up team names (remove bracketed series)
df["Team1"] = df["Team1"].str.replace(r"\[.*?\]", "", regex=True).str.strip()
df["Team2"] = df["Team2"].str.replace(r"\[.*?\]", "", regex=True).str.strip()

# Remove rows with non-numeric scores
df = df[df["Score1"].apply(lambda x: str(x).isdigit())
        & df["Score2"].apply(lambda x: str(x).isdigit())]

# Convert scores to integers
df["Score1"] = df["Score1"].astype(int)
df["Score2"] = df["Score2"].astype(int)

# Reorder columns: Year first
df = df[["Year", "Team1", "Score1", "Team2", "Score2"]]

# drop duplicates
df = df.drop_duplicates()

# Save to cleaned CSV
df.to_csv("WS_results_clean.csv", index=False)
print("Cleaned CSV saved!")
