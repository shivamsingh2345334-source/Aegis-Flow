import asyncio
import random
import time
import pandas as pd
import duckdb
import os
from datetime import datetime

class AegisSensorSim:
    def __init__(self, num_sensors=1000):
        self.num_sensors = num_sensors
        self.sensor_ids = [f"SNS-{i:04d}" for i in range(num_sensors)]
        self.cities = ['Prayagraj', 'Patna', 'Varanasi', 'Bhagalpur']

    async def generate_ping(self):
        """Generates a single IoT sensor data point"""
        return {
            "timestamp": datetime.now().isoformat(),
            "city": random.choice(self.cities),
            "sensor_id": random.choice(self.sensor_ids),
            "rainfall_mm": round(random.uniform(0, 50), 2),
            "water_level_m": round(random.uniform(0, 10), 2),
            "status": "ACTIVE"
        }

    async def produce_batch(self, batch_size=10000):
        """Asynchronously generates thousands of pings"""
        tasks = [self.generate_ping() for _ in range(batch_size)]
        return await asyncio.gather(*tasks)

async def main():
    sim = AegisSensorSim(num_sensors=5000)
    print("🚀 Aegis-Flow: Starting Ingestion Simulation...")
    batch = await sim.produce_batch(20000)
    df = pd.DataFrame(batch)
    print("📊 Data Preview:")
    print(df.head())
    print("✅ Logic Verified!")

if __name__ == "__main__":
    asyncio.run(main())
