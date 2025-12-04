import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

# -------------------------------
# FILE PATHS
# -------------------------------
DATA_PATH = Path("data/weather.csv")
CLEANED_PATH = "cleaned_weather.csv"
SUMMARY_PATH = "summary_report.txt"

# -------------------------------
# 1. LOAD DATA
# -------------------------------
df = pd.read_csv(DATA_PATH)

print("\n--- RAW DATA PREVIEW ---")
print(df.head())
print("\n--- RAW DATA INFO ---")
print(df.info())

# -------------------------------
# 2. DATA CLEANING
# -------------------------------

# Detect date column (dataset may use different names)
date_col = None
for col in df.columns:
    if "date" in col.lower() or "time" in col.lower():
        date_col = col
        break

if date_col is None:
    raise ValueError("Dataset must contain a date or timestamp column.")

# Convert to datetime
df[date_col] = pd.to_datetime(df[date_col], errors='coerce')
df = df.dropna(subset=[date_col])  # remove bad rows

# Rename columns (standardizing)
df = df.rename(columns={
    date_col: "date",
    "temperature": "temperature",
    "temp": "temperature",
    "rainfall": "rainfall",
    "precipitation": "rainfall",
    "humidity": "humidity"
})

# Ensure numeric columns
for col in ["temperature", "rainfall", "humidity"]:
    if col in df.columns:
        df[col] = pd.to_numeric(df[col], errors="coerce")

df = df.dropna(subset=["temperature", "rainfall", "humidity"])

# Sort by date
df = df.sort_values("date")

print("\n--- CLEANED DATA PREVIEW ---")
print(df.head())

# Save cleaned CSV
df.to_csv(CLEANED_PATH, index=False)
print(f"\nCleaned data saved to {CLEANED_PATH}")

# -------------------------------
# 3. STATISTICAL ANALYSIS
# -------------------------------
df = df.set_index("date")

daily_temp = df["temperature"].resample("D").agg(["mean", "min", "max", "std"])
monthly_rain = df["rainfall"].resample("M").sum()
monthly_temp = df["temperature"].resample("M").mean()

# Convert to numpy stats
temp_mean = np.mean(df["temperature"])
temp_min = np.min(df["temperature"])
temp_max = np.max(df["temperature"])
temp_std = np.std(df["temperature"])

# -------------------------------
# 4. VISUALIZATIONS
# -------------------------------

# 1️⃣ Temperature trend
plt.figure(figsize=(10, 5))
plt.plot(daily_temp.index, daily_temp["mean"], label="Daily Avg Temp")
plt.title("Daily Temperature Trend")
plt.xlabel("Date")
plt.ylabel("Temperature (°C)")
plt.grid(True)
plt.savefig("temperature_trend.png")
plt.close()

# 2️⃣ Monthly rainfall
plt.figure(figsize=(10, 5))
plt.bar(monthly_rain.index.strftime("%Y-%m"), monthly_rain.values)
plt.title("Monthly Rainfall")
plt.xlabel("Month")
plt.ylabel("Rainfall (mm)")
plt.xticks(rotation=45)
plt.grid(True)
plt.savefig("monthly_rainfall.png")
plt.close()

# 3️⃣ Humidity vs Temperature
plt.figure(figsize=(8, 5))
plt.scatter(df["temperature"], df["humidity"], alpha=0.5)
plt.title("Humidity vs Temperature")
plt.xlabel("Temperature (°C)")
plt.ylabel("Humidity (%)")
plt.grid(True)
plt.savefig("humidity_vs_temp.png")
plt.close()

print("\nPlots saved: temperature_trend.png, monthly_rainfall.png, humidity_vs_temp.png")

# -------------------------------
# 5. SUMMARY REPORT
# -------------------------------
hottest_day = df["temperature"].idxmax()
coldest_day = df["temperature"].idxmin()
rainiest_month = monthly_rain.idxmax()

with open(SUMMARY_PATH, "w") as f:
    f.write("WEATHER DATA SUMMARY REPORT\n")
    f.write("===========================\n\n")
    f.write(f"Overall Mean Temperature: {temp_mean:.2f}°C\n")
    f.write(f"Maximum Temperature: {temp_max:.2f}°C on {hottest_day}\n")
    f.write(f"Minimum Temperature: {temp_min:.2f}°C on {coldest_day}\n")
    f.write(f"Temperature Standard Deviation: {temp_std:.2f}\n\n")
    f.write(f"Month with Highest Rainfall: {rainiest_month.strftime('%Y-%m')}\n")
    f.write("\nDaily Temperature Summary:\n")
    f.write(daily_temp.to_string())
    f.write("\n\nMonthly Rainfall Summary:\n")
    f.write(monthly_rain.to_string())

print(f"\nSummary report saved to {SUMMARY_PATH}")
print("\nAssignment 4 completed successfully.")
