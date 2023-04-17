import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import datetime
from pathlib import Path

def sidebar(df):
    df["dteday"] = pd.to_datetime(df["dteday"])
    min_date = df["dteday"].min()
    max_date = df["dteday"].max()

    with st.sidebar:
        st.image("https://raw.githubusercontent.com/anddfian/Dicoding-BADP/main/Submission/Capital Bikeshare Logo.png")

        def on_change():
            st.session_state.date = date

        date = st.date_input(
            label="Rentang Waktu", 
            min_value=min_date, 
            max_value=max_date,
            value=[min_date, max_date],
            on_change=on_change
        )

    return date

if __name__ == "__main__":
    sns.set(style="dark")

    st.header("Bike Sharing Dashboard :bike:")

    day_df_csv = Path(__file__).parents[1] / 'Submission/day_clean.csv'

    day_df = pd.read_csv(day_df_csv)

    date = sidebar(day_df)
    if(len(date) == 2):
        main_df = day_df[(day_df["dteday"] >= str(date[0])) & (day_df["dteday"] <= str(date[1]))]
    else:
        main_df = day_df[(day_df["dteday"] >= str(st.session_state.date[0])) & (day_df["dteday"] <= str(st.session_state.date[1]))]

    year = datetime.date.today().year
    copyright = "Copyright © " + str(year) + " | Bike Sharing Dashboard | All Rights Reserved | " + "Made with :heart: by [@anddfian](https://www.linkedin.com/in/anddfian/)"
    st.caption(copyright)