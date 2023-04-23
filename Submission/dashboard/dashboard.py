import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import datetime
from pathlib import Path

def create_season_df(df):
    byseason_df = df.groupby(by="season").instant.nunique().reset_index()
    byseason_df.rename(columns={
        "instant": "sum"
    }, inplace=True)

    return byseason_df

def create_yr_df(df):
    byyr_df = df.groupby(by="yr").instant.nunique().reset_index()
    byyr_df.rename(columns={
        "instant": "sum"
    }, inplace=True)

    return byyr_df

def create_holiday_df(df):
    byholidyday_df = df.groupby(by="holiday").instant.nunique().reset_index()
    byholidyday_df.rename(columns={
        "instant": "sum"
    }, inplace=True)
    
    return byholidyday_df

def create_workingday_df(df):
    byworkingday_df = df.groupby(by="workingday").instant.nunique().reset_index()
    byworkingday_df.rename(columns={
        "instant": "sum"
    }, inplace=True)
    
    return byworkingday_df

def create_weathersit_df(df):
    byweathersit_df = df.groupby(by="weathersit").instant.nunique().reset_index()
    byweathersit_df.rename(columns={
        "instant": "sum"
    }, inplace=True)

    return byweathersit_df

def sidebar(df):
    df["dteday"] = pd.to_datetime(df["dteday"])
    min_date = df["dteday"].min()
    max_date = df["dteday"].max()

    with st.sidebar:
        st.image("https://raw.githubusercontent.com/anddfian/Dicoding-BADP/main/Submission/dashboard/Capital Bikeshare Logo.png")

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

def season(df):
    st.subheader("Season")

    fig, ax = plt.subplots(figsize=(20, 10))
    sns.barplot(
        x="season",
        y="sum",
        data=df.sort_values(by="season", ascending=False),
        ax=ax
    )
    ax.set_title("Number of Bike Sharing by Season", loc="center", fontsize=30)
    ax.set_ylabel(None)
    ax.set_xlabel(None)
    ax.tick_params(axis="y", labelsize=20)
    ax.tick_params(axis="x", labelsize=15)
    st.pyplot(fig)

def year(df):
    st.subheader("Year")

    fig, ax = plt.subplots(figsize=(20, 10))
    sns.barplot(
        x="yr",
        y="sum",
        data=df.sort_values(by="yr", ascending=False),
        ax=ax
    )
    ax.set_title("Number of Bike Sharing by Year", loc="center", fontsize=30)
    ax.set_ylabel(None)
    ax.set_xlabel(None)
    ax.tick_params(axis="y", labelsize=20)
    ax.tick_params(axis="x", labelsize=15)
    st.pyplot(fig)

def month(df):
    st.subheader("Month")

    fig, ax = plt.subplots(figsize=(20, 10))
    sns.barplot(
        x="mnth",
        y="cnt",
        data=df.sort_values(by="mnth", ascending=False),
        ax=ax
    )
    ax.set_title("Number of Bike Sharing by Month", loc="center", fontsize=30)
    ax.set_ylabel(None)
    ax.set_xlabel(None)
    ax.tick_params(axis="x", labelsize=15)
    st.pyplot(fig)

def holiday(df):
    st.subheader("Holiday")

    fig, ax = plt.subplots(figsize=(20, 10))
    sns.barplot(
        x="holiday",
        y="sum",
        data=df.sort_values(by="holiday", ascending=False),
        ax=ax
    )
    ax.set_title("Number of Bike Sharing by Holiday", loc="center", fontsize=30)
    ax.set_ylabel(None)
    ax.set_xlabel(None)
    ax.tick_params(axis="y", labelsize=20)
    ax.tick_params(axis="x", labelsize=15)
    st.pyplot(fig)

def workingday(df):
    st.subheader("Working Day")

    fig, ax = plt.subplots(figsize=(20, 10))
    sns.barplot(
        x="workingday",
        y="sum",
        data=df.sort_values(by="workingday", ascending=False),
        ax=ax
    )
    ax.set_title("Number of Bike Sharing by Working Day", loc="center", fontsize=30)
    ax.set_ylabel(None)
    ax.set_xlabel(None)
    ax.tick_params(axis="y", labelsize=20)
    ax.tick_params(axis="x", labelsize=15)
    st.pyplot(fig)

def weathersit(df):
    st.subheader("Weather Sit")

    fig, ax = plt.subplots(figsize=(20, 10))
    sns.barplot(
        x="weathersit",
        y="sum",
        data=df.sort_values(by="weathersit", ascending=False),
        ax=ax
    )
    ax.set_title("Number of Bike Sharing by Weather Sit", loc="center", fontsize=30)
    ax.set_ylabel(None)
    ax.set_xlabel(None)
    ax.tick_params(axis="y", labelsize=20)
    ax.tick_params(axis="x", labelsize=15)
    st.pyplot(fig)

if __name__ == "__main__":
    sns.set(style="dark")

    st.header("Bike Sharing Dashboard :bike:")

    day_df_csv = Path(__file__).parents[1] / 'dashboard/day_clean.csv'

    day_df = pd.read_csv(day_df_csv)

    date = sidebar(day_df)
    if(len(date) == 2):
        main_df = day_df[(day_df["dteday"] >= str(date[0])) & (day_df["dteday"] <= str(date[1]))]
    else:
        main_df = day_df[(day_df["dteday"] >= str(st.session_state.date[0])) & (day_df["dteday"] <= str(st.session_state.date[1]))]

    season_df = create_season_df(main_df)
    season(season_df)
    year_df = create_yr_df(main_df)
    year(year_df)
    month(main_df)
    holiday_df = create_holiday_df(main_df)
    holiday(holiday_df)
    workingday_df = create_workingday_df(main_df)
    workingday(workingday_df)
    weathersit_df = create_weathersit_df(main_df)
    weathersit(weathersit_df)

    year_copyright = datetime.date.today().year
    copyright = "Copyright © " + str(year_copyright) + " | Bike Sharing Dashboard | All Rights Reserved | " + "Made with :heart: by [@anddfian](https://www.linkedin.com/in/anddfian/)"
    st.caption(copyright)