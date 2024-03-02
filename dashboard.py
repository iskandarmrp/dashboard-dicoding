import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
sns.set(style='dark')

def create_data_byweather(df):
    byweather_df = df.groupby(by="weathersit").agg({
        "cnt": "sum"
    })
    byweather_df.rename(columns={
        "cnt": "customer_count"
    }, inplace=True)
    return byweather_df

def create_data_monthly_rents(df):
    df['dteday'] = pd.to_datetime(df['dteday'])
    monthly_rents_df = df.resample(rule='M', on='dteday').agg({
        "instant": "nunique",
        "cnt": "sum"
    })
    monthly_rents_df.rename(columns={
        "cnt": "customer_count"
    }, inplace=True)
    return monthly_rents_df

def create_data_bytemp(df):
    bytemp_df = df.groupby(by="temp").agg({
        "cnt": "sum"
    })
    bytemp_df.rename(columns={
        "cnt": "customer_count"
    }, inplace=True)
    return bytemp_df

def create_data_byseason(df):
    byseason_df = hour_df.groupby(by="season").agg({
        "cnt": "sum"
    })
    byseason_df.rename(columns={
        "cnt": "customer_count"
    }, inplace=True)
    return byseason_df

hour_df = pd.read_csv('hour_df.csv')
day_df = pd.read_csv('day_df.csv')

byweather_df = create_data_byweather(hour_df)
monthly_rents_df = create_data_monthly_rents(day_df)
byseason_df = create_data_byseason(hour_df)
bytemp_df = create_data_bytemp(hour_df)

st.header("Dashboard :sparkles:")

st.subheader("Number of Customer")

col1, col2, col3 = st.columns(3)

plt.figure(figsize=(10, 5))
 
sns.barplot(
    y=byweather_df['customer_count'], 
    x=byweather_df.index,
    data=byweather_df.sort_values(by="customer_count", ascending=False),
    palette= ["#72BCD4", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3"]
)
plt.title("Number of Customer by Weather", loc="center", fontsize=15)
plt.ylabel("Number of Customer")
plt.xlabel("Weather")
plt.tick_params(axis='x', labelsize=12)

labels = ["1: Clear / Partly Cloudy", "2: Mist / Cloudy", "3: Light Snow / Light Rain / Thunderstorm / Scattered Clouds", "4: Heavy Rain, Ice Palletes, Snow, Fog"]
colors = ["#72BCD4", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3"]

for i, label in enumerate(labels):
    plt.plot([], [], color=colors[i], label=label)
    
plt.legend()

st.pyplot(plt)

plt.figure(figsize=(10, 5))

top_5 = bytemp_df.nlargest(5, 'customer_count')

palette = ['#72BCD4' if index in top_5.index else '#D3D3D3' for index in bytemp_df.index]

sns.barplot(
    y=bytemp_df['customer_count'], 
    x=bytemp_df.index,
    data=bytemp_df.sort_values(by="customer_count", ascending=False),
    palette= palette
)
plt.title("Number of Customer by Temperature (Celcius / 41)", loc="center", fontsize=15)
plt.ylabel("Number of Customer")
plt.xlabel("Temperature")
plt.tick_params(axis='x', labelsize=8)
plt.xticks(rotation=45, ha='right')
plt.tight_layout()

st.pyplot(plt)

plt.figure(figsize=(10, 5))

top = byseason_df.nlargest(1, 'customer_count')

palette = ['#72BCD4' if index in top.index else '#D3D3D3' for index in byseason_df.index]

sns.barplot(
    y=byseason_df['customer_count'], 
    x=byseason_df.index,
    data=byseason_df.sort_values(by="customer_count", ascending=False),
    palette= palette
)
plt.title("Number of Customer by Season", loc="center", fontsize=15)
plt.ylabel("Number of Customer")
plt.xlabel("Season")
plt.tick_params(axis='x', labelsize=12)

labels = ["1: Springer", "2: Summer","3: Fall", "4: Winter"]
colors = palette

for i, label in enumerate(labels):
    plt.plot([], [], color=colors[i], label=label)
    
plt.legend()

st.pyplot(plt)

st.subheader("Total Customer per Month")

plt.figure(figsize=(10, 5))
plt.plot(
    monthly_rents_df.index,
    monthly_rents_df["customer_count"],
    marker='o', 
    linewidth=0.4,
    color="#72BCD4"
)
plt.title("Total Customer per Month", loc="center", fontsize=20)

month_labels = monthly_rents_df.index.strftime('%b %Y')

plt.xticks(monthly_rents_df.index, month_labels, rotation=45, ha='right', fontsize=10)
plt.yticks(fontsize=10)
plt.show()

st.pyplot(plt)