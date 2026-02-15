import duckdb
import pandas as pd
import numpy as np
import time

con = duckdb.connect(database=':memory:')

con.execute("""
    CREATE TABLE IF NOT EXISTS sensor_logs (
        timestamp TIMESTAMP,
        sensor_id INTEGER,
        rainfall FLOAT,
        humidity FLOAT,
        water_level FLOAT
    )
""")

def ingest_batch_to_duckdb(batch_dict):
    """Efficiently moving data from NumPy to DuckDB via Memory Registration"""
    df = pd.DataFrame(batch_dict['batch_data'], 
                      columns=['sensor_id', 'rainfall', 'humidity', 'water_level'])
    df['timestamp'] = batch_dict['timestamp']
    
    con.register('temp_df', df)
    con.execute("INSERT INTO sensor_logs SELECT timestamp, sensor_id, rainfall, humidity, water_level FROM temp_df")
    con.unregister('temp_df')

start_time = time.time()

for _ in range(10): 
    mock_batch = {
        "timestamp": pd.Timestamp.now(),
        "batch_data": np.random.rand(100000, 4) 
    }
    ingest_batch_to_duckdb(mock_batch)

print("\n📊 --- AEGIS-FLOW REAL-TIME ANALYTICS ---")
res = con.execute("""
    SELECT 
        COUNT(*) as Total_Rows, 
        AVG(rainfall) as Avg_Rain, 
        MAX(water_level) as Max_Flood_Level 
    FROM sensor_logs
""").df()

print(res)
print(f"\n⚡ System Performance: Processed 1,000,000 rows in {time.time()-start_time:.4f}s")
