import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path
import numpy as np

# Folder setup

DATA_DIR = Path("data")
OUTPUT_DASHBOARD = "dashboard.png"
OUTPUT_CLEAN = "cleaned_energy_data.csv"
OUTPUT_SUMMARY = "summary.txt"
OUTPUT_BUILDING_SUMMARY = "building_summary.csv"


# Task-3 OOP Classes

class MeterReading:
    def __init__(self, timestamp, kwh):
        self.timestamp = pd.to_datetime(timestamp)
        self.kwh = float(kwh)


class Building:
    def __init__(self, name):
        self.name = name
        self.readings = []

    def add_reading(self, reading):
        self.readings.append(reading)

    def to_dataframe(self):
        return pd.DataFrame({
            "timestamp": [r.timestamp for r in self.readings],
            "kwh": [r.kwh for r in self.readings],
            "building": self.name
        })


class BuildingManager:
    def __init__(self):
        self.buildings = {}

    def get_or_create(self, name):
        if name not in self.buildings:
            self.buildings[name] = Building(name)
        return self.buildings[name]

    def load_dataframe(self, df):
        for _, row in df.iterrows():
            b = self.get_or_create(row["building"])
            b.add_reading(MeterReading(row["timestamp"], row["kwh"]))

    def summary(self):
        output = []
        for name, building in self.buildings.items():
            df = building.to_dataframe()
            total = df["kwh"].sum()
            avg = df["kwh"].mean()
            mn = df["kwh"].min()
            mx = df["kwh"].max()
            count = len(df)
            output.append([name, total, avg, mn, mx, count])
        return pd.DataFrame(output,
                            columns=["building", "total_kwh", "average_kwh", "min_kwh", "max_kwh", "readings"])
                            

#Task 1 — Read All CSV Files
                                     
def read_all_csvs():
    frames = []

    for file in DATA_DIR.glob("*.csv"):
        try:
            df = pd.read_csv(file)
            df["timestamp"] = pd.to_datetime(df["timestamp"], errors="coerce")
            df["kwh"] = pd.to_numeric(df["kwh"], errors="coerce")
            df["building"] = file.stem  # building name from filename
            df = df.dropna(subset=["timestamp", "kwh"])
            frames.append(df)

            print(f"Loaded {file.name} ({len(df)} rows)")

        except Exception as e:
            print(f"Error reading {file.name}: {e}")

    if not frames:
        print("No CSV files found in data/")
        return pd.DataFrame()

    combined = pd.concat(frames, ignore_index=True)
    combined = combined.sort_values("timestamp")
    combined.to_csv(OUTPUT_CLEAN, index=False)

    print(f"\nCombined data saved → {OUTPUT_CLEAN}")
    return combined


# Task 2 — Aggregations

def compute_aggregations(df):
    df = df.set_index("timestamp")

    daily = df.groupby("building").resample("D")["kwh"].sum().reset_index()
    weekly = df.groupby("building").resample("W")["kwh"].sum().reset_index()

    return daily, weekly



# Task 4 — Dashboard Visualization

def create_dashboard(df, daily, weekly):
    plt.close("all")
    fig, axs = plt.subplots(3, 1, figsize=(10, 14))

    # 1. Daily Trend Line
    pivot_daily = daily.pivot(index="timestamp", columns="building", values="kwh").fillna(0)
    for b in pivot_daily.columns:
        axs[0].plot(pivot_daily.index, pivot_daily[b], label=b)
    axs[0].set_title("Daily Energy Consumption Trend")
    axs[0].legend()

    # 2. Weekly Average Bar Chart
    avg_weekly = weekly.groupby("building")["kwh"].mean()
    axs[1].bar(avg_weekly.index, avg_weekly.values)
    axs[1].set_title("Weekly Average Consumption per Building")

    # 3. Peak Hour Scatter Plot
    top_points = df.nlargest(40, "kwh")   # top 40 values
    axs[2].scatter(top_points["timestamp"], top_points["kwh"], c="purple")
    axs[2].set_title("Peak Hour Energy Readings (Top 40)")
    axs[2].set_xlabel("Timestamp")
    axs[2].set_ylabel("kWh")

    plt.tight_layout()
    plt.savefig(OUTPUT_DASHBOARD)
    print(f"Dashboard saved → {OUTPUT_DASHBOARD}")


# Task 5 — Summary Report

def write_summary(df, building_summary):
    total = df["kwh"].sum()
    highest_building = building_summary.loc[building_summary["total_kwh"].idxmax()]

    peak_row = df.loc[df["kwh"].idxmax()]

    with open(OUTPUT_SUMMARY, "w") as f:
        f.write("CAMPUS ENERGY SUMMARY REPORT\n")
        f.write("============================\n\n")
        f.write(f"Total campus consumption: {total:.2f} kWh\n")
        f.write(f"Highest consuming building: {highest_building['building']} ({highest_building['total_kwh']:.2f} kWh)\n")
        f.write(f"Peak reading time: {peak_row['timestamp']} ({peak_row['kwh']} kWh)\n")

    print(f"Summary saved → {OUTPUT_SUMMARY}")



# Main

def main():
    df = read_all_csvs()
    if df.empty:
        return

    manager = BuildingManager()
    manager.load_dataframe(df)
    building_summary = manager.summary()
    building_summary.to_csv(OUTPUT_BUILDING_SUMMARY, index=False)
    print(f"Building summary saved → {OUTPUT_BUILDING_SUMMARY}")

    daily, weekly = compute_aggregations(df)
    create_dashboard(df, daily, weekly)
    write_summary(df, building_summary)

    print("\nCapstone project completed successfully!")


if __name__ == "__main__":
    main()
