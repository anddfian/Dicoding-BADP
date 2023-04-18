import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from babel.numbers import format_currency
from pathlib import Path

def create_daily_orders_df(df):
    daily_order_df = df.resample(rule="D", on="order_date").agg({
        "order_id": "nunique",
        "total_price": "sum"
    })
    daily_order_df = daily_order_df.reset_index()
    daily_order_df.rename(columns={
        "order_id": "order_count",
        "total_price": "revenue"
    }, inplace=True)

    return daily_order_df

def create_sum_order_items_df(df):
    sum_order_items_df = df.groupby("product_name").quantity_x.sum().sort_values(ascending=False).reset_index()

    return sum_order_items_df

def create_bygender_df(df):
    bygender_df = df.groupby(by="gender").customer_id.nunique().reset_index()
    bygender_df.rename(columns={
        "customer_id": "customer_count"
    }, inplace=True)

    return bygender_df

def create_byage_df(df):
    byage_df = df.groupby(by="age_group").customer_id.nunique().reset_index()
    byage_df.rename(columns={
        "customer_id": "customer_count"
    }, inplace=True)
    byage_df["age_group"] = pd.Categorical(byage_df["age_group"], ["Youth", "Adults", "Seniors"])

    return byage_df

def create_bystate_df(df):
    bystate_df = df.groupby(by="state").customer_id.nunique().reset_index()
    bystate_df.rename(columns={
        "customer_id": "customer_count"
    }, inplace=True)

    return bystate_df

def create_rfm_df(df):
    rfm_df = df.groupby(by="customer_id", as_index=False).agg({
        "order_date": "max",
        "order_id": "nunique",
        "total_price": "sum"
    })
    rfm_df.columns = ["customer_id", "max_order_timestamp", "frequency", "monetary"]

    rfm_df["max_order_timestamp"] = rfm_df["max_order_timestamp"].dt.date
    recent_date = df["order_date"].dt.date.max()
    rfm_df["recency"] = rfm_df["max_order_timestamp"].apply(lambda x: (recent_date - x).days)
    rfm_df.drop("max_order_timestamp", axis=1, inplace=True)

    return rfm_df

def sidebar(df):
    datetime_columns = ["order_date", "delivery_date"]
    df.sort_values(by="order_date", inplace=True)
    df.reset_index(inplace=True)

    for column in datetime_columns:
        df[column] = pd.to_datetime(df[column])

    min_date = df["order_date"].min()
    max_date = df["order_date"].max()

    with st.sidebar:
        st.image("https://github.com/dicodingacademy/assets/raw/main/logo.png")

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

def daily_orders(df):
    st.subheader("Daily Orders")

    col1, col2 = st.columns(2)

    with col1:
        total_orders = df.order_count.sum()
        st.metric("Total Orders", value=total_orders)

    with col2:
        total_revenue = format_currency(df.revenue.sum(), "AUD", locale="es_CO")
        st.metric("Total Revenue", value=total_revenue)

    fig, ax = plt.subplots(figsize=(16, 8))
    ax.plot(
        df["order_date"],
        df["order_count"],
        marker="o",
        linewidth=2,
        color="#90CAF9"
    )
    ax.tick_params(axis="y", labelsize=20)
    ax.tick_params(axis="x", labelsize=15)

    st.pyplot(fig)

def best_worst_performing_product(df):
    st.subheader("Best & Worst Performing Product")

    fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(35, 15))

    colors = ["#90CAF9", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3"]

    sns.barplot(x="quantity_x", y="product_name", data=df.head(5), palette=colors, ax=ax[0])
    ax[0].set_ylabel(None)
    ax[0].set_xlabel("Number of Sales", fontsize=30)
    ax[0].set_title("Best Performing Product", loc="center", fontsize=50)
    ax[0].tick_params(axis="y", labelsize=35)
    ax[0].tick_params(axis="x", labelsize=30)

    sns.barplot(x="quantity_x", y="product_name", data=df.sort_values(by="quantity_x", ascending=True).head(5), palette=colors, ax=ax[1])
    ax[1].set_ylabel(None)
    ax[1].set_xlabel("Number of Sales", fontsize=30)
    ax[1].invert_xaxis()
    ax[1].yaxis.set_label_position("right")
    ax[1].yaxis.tick_right()
    ax[1].set_title("Worst Performing Product", loc="center", fontsize=50)
    ax[1].tick_params(axis="y", labelsize=35)
    ax[1].tick_params(axis="x", labelsize=30)

    st.pyplot(fig)

def customer_demographics(gender, age, state):
    st.subheader("Customer Demographics")

    col1, col2 = st.columns(2)

    with col1:
        fig, ax = plt.subplots(figsize=(20, 10))

        colors = ["#90CAF9", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3"]

        sns.barplot(
            y="customer_count",
            x="gender",
            data=gender.sort_values(by="customer_count", ascending=False),
            palette=colors,
            ax=ax
        )
        ax.set_title("Number of Customer by Gender", loc="center", fontsize=50)
        ax.set_ylabel(None)
        ax.set_xlabel(None)
        ax.tick_params(axis="x", labelsize=35)
        ax.tick_params(axis="y", labelsize=30)
        st.pyplot(fig)

    with col2:
        fig, ax = plt.subplots(figsize=(20, 10))

        colors = ["#D3D3D3", "#90CAF9", "#D3D3D3", "#D3D3D3", "#D3D3D3"]

        sns.barplot(
            y="customer_count",
            x="age_group",
            data=age.sort_values(by="age_group", ascending=False),
            palette=colors,
            ax=ax
        )
        ax.set_title("Number of Customer by Age", loc="center", fontsize=50)
        ax.set_ylabel(None)
        ax.set_xlabel(None)
        ax.tick_params(axis="x", labelsize=35)
        ax.tick_params(axis="y", labelsize=30)
        st.pyplot(fig)

    fig, ax = plt.subplots(figsize=(20, 10))
    colors = ["#90CAF9", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3"]
    sns.barplot(
        x="customer_count",
        y="state",
        data=state.sort_values(by="customer_count", ascending=False),
        palette=colors,
        ax=ax
    )
    ax.set_title("Number of Customer by State", loc="center", fontsize=30)
    ax.set_ylabel(None)
    ax.set_xlabel(None)
    ax.tick_params(axis="y", labelsize=20)
    ax.tick_params(axis="x", labelsize=15)
    st.pyplot(fig)

def best_customer_based_on_rfm_parameters(df):
    st.subheader("Best Customer Based on RFM Parameters")

    col1, col2, col3 = st.columns(3)

    with col1:
        avg_recency = round(df.recency.mean(), 1)
        st.metric("Average Recency (days)", value=avg_recency)

    with col2:
        avg_frequency = round(df.frequency.mean(), 2)
        st.metric("Average Frequency", value=avg_frequency)

    with col3:
        avg_monetary = format_currency(df.monetary.mean(), "AUD", locale="es_CO")
        st.metric("Average Monetary", value=avg_monetary)

    fig, ax = plt.subplots(nrows=1, ncols=3, figsize=(35, 15))
    colors = ["#90CAF9", "#90CAF9", "#90CAF9", "#90CAF9", "#90CAF9"]

    sns.barplot(y="recency", x="customer_id", data=df.sort_values(by="recency", ascending=True).head(5), palette=colors, ax=ax[0])
    ax[0].set_ylabel(None)
    ax[0].set_xlabel("customer_id", fontsize=30)
    ax[0].set_title("By Recency (days)", loc="center", fontsize=50)
    ax[0].tick_params(axis="y", labelsize=30)
    ax[0].tick_params(axis="x", labelsize=35)

    sns.barplot(y="frequency", x="customer_id", data=df.sort_values(by="frequency", ascending=False).head(5), palette=colors, ax=ax[1])
    ax[1].set_ylabel(None)
    ax[1].set_xlabel("customer_id", fontsize=30)
    ax[1].set_title("By Frequency", loc="center", fontsize=50)
    ax[1].tick_params(axis="y", labelsize=30)
    ax[1].tick_params(axis="x", labelsize=35)

    sns.barplot(y="monetary", x="customer_id", data=df.sort_values(by="monetary", ascending=False).head(5), palette=colors, ax=ax[2])
    ax[2].set_ylabel(None)
    ax[2].set_xlabel("customer_id", fontsize=30)
    ax[2].set_title("By Monetary", loc="center", fontsize=50)
    ax[2].tick_params(axis="y", labelsize=30)
    ax[2].tick_params(axis="x", labelsize=35)

    st.pyplot(fig)

if __name__ == "__main__":
    sns.set(style="dark")

    st.header("Dicoding Collection Dashboard :sparkles:")

    all_data_csv = Path(__file__).parents[1] / 'dashboard/all_data.csv'

    all_df = pd.read_csv(all_data_csv)

    date = sidebar(all_df)
    if(len(date) == 2):
        main_df = all_df[(all_df["order_date"] >= str(date[0])) & (all_df["order_date"] <= str(date[1]))]
    else:
        main_df = all_df[(all_df["order_date"] >= str(st.session_state.date[0])) & (all_df["order_date"] <= str(st.session_state.date[1]))]

    daily_orders_df = create_daily_orders_df(main_df)
    daily_orders(daily_orders_df)
    sum_order_items_df = create_sum_order_items_df(main_df)
    best_worst_performing_product(sum_order_items_df)
    bygender_df = create_bygender_df(main_df)
    byage_df = create_byage_df(main_df)
    bystate_df = create_bystate_df(main_df)
    customer_demographics(bygender_df, byage_df, bystate_df)
    rfm_df = create_rfm_df(main_df)
    best_customer_based_on_rfm_parameters(rfm_df)

    st.caption("Copyright (c) Dicoding 2023")