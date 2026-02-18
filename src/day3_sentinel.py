"""
Day 3 – Sentinel Anomaly Detection Engine
------------------------------------------

This module scans recent sensor data stored in DuckDB
and detects high-risk anomalies using SQL window functions.

Author: Aegis-Flow
"""

import duckdb
import pandas as pd
from typing import Optional, List, Dict


# -----------------------------------------------------
# Database Connection 
# -----------------------------------------------------
con = duckdb.connect("aegis.db")  # Use persistent DB in production


# -----------------------------------------------------
# Sentinel Scan Logic
# -----------------------------------------------------
def run_sentinel_scan() -> Optional[pd.DataFrame]:
    """
    Scans the latest sensor batch for flood-related anomalies.

    Detection Rules:
    - Rainfall > 45 mm
    - Water Level > 8.5 meters

    Additionally computes rolling average water level per sensor
    using SQL window functions.
    """

    print("\n🕵️ Sentinel Scanning for Anomalies...")

    query = """
    WITH RecentData AS (
        SELECT *,
               AVG(water_level) OVER (
                   PARTITION BY sensor_id
                   ORDER BY timestamp
                   ROWS BETWEEN 5 PRECEDING AND CURRENT ROW
               ) AS rolling_avg_water
        FROM sensor_logs
        LIMIT 100000
    )
    SELECT *
    FROM RecentData
    WHERE rainfall > 45.0
       OR water_level > 8.5
    """

    anomalies = con.execute(query).df()

    if not anomalies.empty:
        print(f"🚨 ALERT! {len(anomalies)} Critical Anomalies Detected!")
        return anomalies

    print("✅ System Nominal. No threats detected.")
    return None


# -----------------------------------------------------
# Alert Buffer (Feeds Agent Layer)
# -----------------------------------------------------
alert_buffer: List[Dict] = []


def trigger_executive_action(anomaly_df: Optional[pd.DataFrame]) -> None:
    """
    Pushes critical anomaly records into an alert buffer.
    This buffer can later feed automated mitigation agents.
    """

    if anomaly_df is None:
        return

    critical_alerts = anomaly_df[
        ["timestamp", "sensor_id", "rainfall", "water_level"]
    ].to_dict("records")

    alert_buffer.extend(critical_alerts)

    print(f"📤 Sent {len(critical_alerts)} alerts to Agent Buffer.")


# -----------------------------------------------------
# Main Execution (For Standalone Testing)
# -----------------------------------------------------
if __name__ == "__main__":

    print("\n--- Day 3: Sentinel Active ---")

    anomalies = run_sentinel_scan()
    trigger_executive_action(anomalies)

    print(f"\n📂 Current Agent Buffer Size: {len(alert_buffer)} events")
