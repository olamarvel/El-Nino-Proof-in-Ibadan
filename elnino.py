import requests
import pandas as pd
import matplotlib.pyplot as plt
import os

# Coordinates for Ibadan, Nigeria
lat, lon = 7.3775, 3.9470

print("Fetching 15 years of historical data for Ibadan...")
# 1. Fetch historical data (2010 to 2025) for October 
url_archive = f"https://archive-api.open-meteo.com/v1/archive?latitude={lat}&longitude={lon}&start_date=2010-10-01&end_date=2025-10-27&daily=temperature_2m_max&timezone=Africa%2FLagos"
res_archive = requests.get(url_archive).json()

print("Fetching current 2026 El Niño data...")
# 2. Fetch recent data (2026) for October
url_recent = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&start_date=2026-10-01&end_date=2026-10-27&daily=temperature_2m_max&timezone=Africa%2FLagos"
res_recent = requests.get(url_recent).json()

if 'daily' in res_archive and 'daily' in res_recent:
    # Process historical baseline
    df_arch = pd.DataFrame({
        'date': pd.to_datetime(res_archive['daily']['time']), 
        'max_temp': res_archive['daily']['temperature_2m_max']
    })
    df_arch['day'] = df_arch['date'].dt.day
    
    # Process 2026 data
    df_rec = pd.DataFrame({
        'date': pd.to_datetime(res_recent['daily']['time']), 
        'max_temp': res_recent['daily']['temperature_2m_max']
    })
    df_rec['day'] = df_rec['date'].dt.day
    
    # Calculate historical average for each day in October
    hist_avg = df_arch.groupby('day')['max_temp'].mean().reset_index()
    hist_avg.columns = ['day', 'hist_avg_temp']
    
    # Merge for comparison
    comparison = pd.merge(df_rec, hist_avg, on='day')
    
    # 3. Create the Visualization
    plt.figure(figsize=(10, 6))
    
    # Plot the 15-year average vs the 2026 spike
    plt.plot(comparison['day'], comparison['hist_avg_temp'], 'b--', label='Historical Average (2010-2025)', linewidth=2)
    plt.plot(comparison['day'], comparison['max_temp'], 'r-o', label='2026 (El Niño Year)', linewidth=2)
    
    # Highlight the "Heat Anomaly" (where 2026 is hotter than normal)
    plt.fill_between(comparison['day'], comparison['hist_avg_temp'], comparison['max_temp'], 
                     where=(comparison['max_temp'] > comparison['hist_avg_temp']), 
                     color='red', alpha=0.3, label='Excess Heat Anomaly')
    
    plt.title('Ibadan Extreme Heat: October 2026 vs. 15-Year Historical Average')
    plt.xlabel('Day in October')
    plt.ylabel('Maximum Temperature (°C)')
    plt.legend()
    plt.grid(True, alpha=0.3)
    
    if not os.path.exists('data'):
        os.makedirs('data')
        
    plt.savefig('data/ibadan_heatwave_anomaly.png')
    print("Chart saved to 'data/ibadan_heatwave_anomaly.png'. You can now see the exact El Niño heat gap!")
else:
    print("Error fetching data from the API.")