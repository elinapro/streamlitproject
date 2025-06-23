from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import os
import time

# Set headless mode for Streamlit compatibility
options = Options()
options.add_argument('--headless')
options.add_argument('--disable-gpu')
options.add_argument('--no-sandbox')
options.add_argument("user-agent=Mozilla/5.0")

# Initialize driver
driver = webdriver.Chrome(service=ChromeService(
    ChromeDriverManager().install()), options=options)

try:
    driver.get("https://www.baseball-almanac.com/ws/wsmenu.shtml")
    wait = WebDriverWait(driver, 10)
    table = wait.until(EC.presence_of_element_located((By.TAG_NAME, "table")))

    rows = table.find_elements(By.TAG_NAME, "tr")[1:]

    data = []
    for row in rows:
        try:
            cells = row.find_elements(By.TAG_NAME, "td")
            if len(cells) == 5:
                title = cells[0].text.strip()
                team1 = cells[1].text.strip()
                score1 = cells[2].text.strip()
                team2 = cells[3].text.strip()
                score2 = cells[4].text.strip()
                data.append([title, team1, score1, team2, score2])
        except Exception as row_err:
            print(f"Error parsing row: {row_err}")

finally:
    driver.quit()


# Save dataframe to CSV
try:
    df = pd.DataFrame(
        data, columns=["Title", "Team1", "Score1", "Team2", "Score2"])
    df.to_csv("WS_results.csv", index=False)
    print("Saved the CSV to csv/WS_results.csv")

except Exception as file_err:
    print(f"Error writing CSV: {file_err}")


app = Dash(__name__)
server = app.server
