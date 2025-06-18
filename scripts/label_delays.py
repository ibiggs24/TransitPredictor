import sqlite3
import pandas as pd
import random
from datetime import datetime, timedelta

def time_to_minutes(t):
    try:
        h, m, s = map(int, t.split(":"))
        return h * 60 + m
    except:
        return None

def simulate_delay():
    # 80% on time, 20% delayed by 6-15 minutes
    return 0 if random.random() < 0.8 else random.randint(6, 15)

def main():
    conn = sqlite3.connect("smart_transit.db")
    df = pd.read_sql_query("SELECT * FROM stop_times", conn)

    print("Simulating delays...")

    delays = []
    for i, row in df.iterrows():
        scheduled = time_to_minutes(row['arrival_time'])
        if scheduled is None:
            delays.append(None)
            continue
        delay_minutes = simulate_delay()
        delayed = 1 if delay_minutes > 5 else 0
        delays.append(delayed)

    df["delayed"] = delays
    df.to_sql("labeled_stop_times", conn, if_exists="replace", index=False)

    conn.close()
    print("Delay labeling complete. Saved to labeled_stop_times.")

if __name__ == "__main__":
    main()
