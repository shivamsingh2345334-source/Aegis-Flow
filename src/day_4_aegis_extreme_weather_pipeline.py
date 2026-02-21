"""
Aegis Extreme Weather Stress Test Pipeline
-----------------------------------------
Simulates extreme rainfall + water level data,
stores it as partitioned parquet,
and scans it using DuckDB analytics engine.
"""

import os
import time
import duckdb
import numpy as np
import pandas as pd


# =====================================
# Setup Storage Directories
# =====================================

os.makedirs("aegis_data/rainfall", exist_ok=True)
os.makedirs("aegis_data/water_level", exist_ok=True)


# =====================================
# DuckDB Connection
# =====================================

con = duckdb.connect(database="aegis_engine.db", read_only=False)


# =====================================
# Stress Data Generator
# =====================================

def simulate_extreme_weather():
    """
    Generates biased sensor data representing
    extreme rainfall and flood risk conditions.
    """

    print("\nSimulating Extreme Weather (Stress Test)...")

    size = 100000

    extreme_rainfall = np.random.uniform(45, 70, size=size)
    extreme_water = np.random.uniform(7, 12, size=size)
    sensor_ids = np.random.randint(1, 1001, size=size)

    df = pd.DataFrame({
        "timestamp": pd.Timestamp.now(),
        "sensor_id": sensor_ids,
        "rainfall": extreme_rainfall,
        "water_level": extreme_water
    })

    return df


# =====================================
# Partitioned Storage Writer
# =====================================

def save_partitioned_data(df):
    """
    Saves dataframe as parquet partition.
    """

    path = f"aegis_data/rainfall/batch_{int(time.time())}.parquet"

    df.to_parquet(path, index=False)

    print(f"Data saved → {path}")


# =====================================
# Analytics Scanner
# =====================================

def scan_extreme_events():
    """
    DuckDB scans only stored partitions
    and detects high-risk rainfall events.
    """

    print("\nScanning Partitioned Storage...")

    result = con.execute("""
        SELECT COUNT(*) 
        FROM read_parquet('aegis_data/rainfall/*.parquet')
        WHERE rainfall > 50
    """).fetchone()[0]

    print(f"Sentinel Detected {result} Extreme Rainfall Records")


# =====================================
# Main Execution
# =====================================

if __name__ == "__main__":

    # Step 1 — Generate Stress Data
    df = simulate_extreme_weather()

    # Step 2 — Save Partition
    save_partitioned_data(df)

    # Step 3 — Scan for Risk Events
    scan_extreme_events()

    print("\nPipeline Execution Complete")
