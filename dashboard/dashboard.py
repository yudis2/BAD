import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from babel.numbers import format_currency

sns.set(style='dark')

# Helper function yang dibutuhkan untuk menyiapkan berbagai dataframe
def create_daily_user_df(df):
    daily_user_df = df.resample(rule='D', on='dteday').agg({
        "instant": "nunique",
        "cnt": "sum"
    })
    daily_user_df = daily_user_df.reset_index()
    daily_user_df.rename(columns={
        "instant": "instant_count",
        "cnt": "total_user"
    }, inplace=True)
    
    return daily_user_df

def create_weather_user_df(df):
    grouped = df.groupby("season_name")[["casual", "registered"]].sum().reset_index()
    long_df = grouped.melt(
        id_vars="season_name", 
        value_vars=["casual", "registered"], 
        var_name="User Type", 
        value_name="Total Rentals"
    )
    return long_df

# Load cleaned data
all_df = pd.read_csv("dashboard/all_data.csv")

datetime_columns = ["dteday"]
all_df.sort_values(by="dteday", inplace=True)
all_df.reset_index(inplace=True)

for column in datetime_columns:
    all_df[column] = pd.to_datetime(all_df[column])

# Filter data
min_date = all_df["dteday"].min()
max_date = all_df["dteday"].max()

with st.sidebar:
    # Menambahkan logo perusahaan
    st.image("https://docomo-cycle.jp/assets/img/common/page/contactus/pc/top_img.jpg")
    
    # Mengambil start_date & end_date dari date_input
    start_date, end_date = st.date_input(
        label='Pick A Date',min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )

main_df = all_df[(all_df["dteday"] >= str(start_date)) & 
                (all_df["dteday"] <= str(end_date))]

# # Menyiapkan berbagai dataframe
daily_user_df = create_daily_user_df(main_df)
long_df = create_weather_user_df(main_df)

# plot number of daily orders (2012)
st.header('Capital BikeShare System Dashboard :sparkles:')
st.subheader('Record')

col1, col2 = st.columns(2)

with col1:
    total_orders = daily_user_df.instant_count.sum()
    st.metric("Total record", value=total_orders)

with col2:
    total_revenue = daily_user_df.total_user.sum()
    st.metric("Total User", value=total_revenue)

fig, ax = plt.subplots(figsize=(16, 8))
ax.plot(
    daily_user_df["dteday"],
    daily_user_df["total_user"],
    marker='o', 
    linewidth=2,
    color="#90CAF9"
)
ax.tick_params(axis='y', labelsize=20)
ax.tick_params(axis='x', labelsize=15)

st.pyplot(fig)

# Product performance
st.subheader("Best & Worst Season to Ride")

fig, ax = plt.subplots(figsize=(20, 10))
sns.barplot(
        x="season_name",
        y="Total Rentals",
        hue="User Type",
        data=long_df,
        estimator=sum,
        errorbar=None
    )
ax.set_title("Casual vs Registered User by Season", loc="center", fontsize=50)
ax.set_ylabel(None)
ax.set_xlabel(None)
ax.tick_params(axis='x', labelsize=35)
ax.tick_params(axis='y', labelsize=30)
st.pyplot(fig)

# RFM Analysis
st.subheader("Total Bike Rent By Weather And Day")

col1, col2 = st.columns(2)

with col1:
    fig, ax = plt.subplots(figsize=(20, 10))

    sns.lineplot(
        x="day_of_week",
        y="cnt",
        data=main_df,
        estimator="sum",
        errorbar=None,
        marker="o",
        color="purple"
    )
    ax.set_title("Number of User by season", loc="center", fontsize=50)
    ax.set_ylabel(None)
    ax.set_xlabel(None)
    ax.tick_params(axis='x', labelsize=35)
    ax.tick_params(axis='y', labelsize=30)
    st.pyplot(fig)

with col2:
    fig, ax = plt.subplots(figsize=(20, 10))

    sns.lineplot(
        x="weather_condition",
        y="cnt",
        data=main_df,
        estimator="sum",
        errorbar=None,
        marker="o",
        color="purple"
    )
    ax.set_title("Number of User by season", loc="center", fontsize=50)
    ax.set_ylabel(None)
    ax.set_xlabel(None)
    ax.tick_params(axis='x', labelsize=35)
    ax.tick_params(axis='y', labelsize=30)
    st.pyplot(fig)
    

st.caption('Copyright © Yudisdwi 2025')