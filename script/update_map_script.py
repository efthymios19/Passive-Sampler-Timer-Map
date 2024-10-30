import pandas as pd
import folium 
from datetime import timedelta

### Import kobo-csv

ps=pd.read_csv('data/data.csv', sep=';')

### Filter dataframe based on the starting date of the campaing
starting_date='2024-10-22'
filtered_ps=ps[ps['Date_Time']>starting_date]

# Assuming 'filtered_ps' is your DataFrame with a 'Date_Time' and 'Sampler_Type' columns
filtered_ps['Date_Time'] = pd.to_datetime(filtered_ps['Date_Time'], utc=True).dt.tz_localize(None)

# Calculate days remaining for each row
today = pd.Timestamp.now()  # This will be timezone-naive

# Set the duration based on the sampler type
# Set the duration and calculate termination date based on the sampler type
def calculate_days_remaining(row):
    termination_date_VPS = None
    termination_date_CPS = None
    days_remaining_VPS = None
    days_remaining_CPS = None
    if row['Passive Sampler Type'] == 'All of them':
        termination_date_VPS = row['Date_Time'] + timedelta(days=12)
        termination_date_CPS = row['Date_Time'] + timedelta(days=15)
        days_remaining_VPS = max((termination_date_VPS - today).days, 0)
        days_remaining_CPS = max((termination_date_CPS - today).days, 0)
    elif row['Passive Sampler Type'] == 'VPS':
        termination_date_VPS = row['Date_Time'] + timedelta(days=12)
        days_remaining_VPS = max((termination_date_VPS - today).days, 0)
    elif row['Passive Sampler Type'] == 'CPS and DGTs':
        termination_date_CPS = row['Date_Time'] + timedelta(days=15)
        days_remaining_CPS = max((termination_date_CPS - today).days, 0)
    elif row['Passive Sampler Type'] == 'CPS':
        termination_date_CPS = row['Date_Time'] + timedelta(days=15)
        days_remaining_CPS = max((termination_date_CPS - today).days, 0)
    elif row['Passive Sampler Type'] == 'DGTs':
        termination_date_CPS = row['Date_Time'] + timedelta(days=15)
        days_remaining_CPS = max((termination_date_CPS - today).days, 0)
    elif row['Passive Sampler Type'] == 'CPS and DGTs':
        termination_date_CPS = row['Date_Time'] + timedelta(days=15)
        days_remaining_CPS = max((termination_date_CPS - today).days, 0)
    elif row['Passive Sampler Type'] == 'VPS and DGTs':
        termination_date_VPS = row['Date_Time'] + timedelta(days=12)
        days_remaining_VPS = max((termination_date_VPS - today).days, 0)
        termination_date_CPS = row['Date_Time'] + timedelta(days=15)
        days_remaining_CPS = max((termination_date_CPS - today).days, 0)
    elif row['Passive Sampler Type'] == 'VPS and CPS':
        termination_date_VPS = row['Date_Time'] + timedelta(days=12)
        termination_date_CPS = row['Date_Time'] + timedelta(days=15)
        days_remaining_VPS = max((termination_date_VPS - today).days, 0)
        days_remaining_CPS = max((termination_date_CPS - today).days, 0)
    
    return pd.Series([days_remaining_VPS, termination_date_VPS, days_remaining_CPS, termination_date_CPS])

filtered_ps[['days_remaining_VPS', 'termination_date_VPS', 'days_remaining_CPS', 'termination_date_CPS']] = filtered_ps.apply(calculate_days_remaining, axis=1)

# Create the interactive map
m = folium.Map(location=[filtered_ps['_Location_latitude'].mean(), filtered_ps['_Location_longitude'].mean()], zoom_start=10)

# Iterate through the DataFrame and add markers
for index, row in filtered_ps.iterrows():
   #remaining_days = max(row['days_remaining'], 0)  # Ensure it doesn't go negative
    
    # Prepare popup content
    popup_content = f"<b>ID:</b> {row['ID']}<br>"
    popup_content += f"<b>Type:</b> {row['Passive Sampler Type']}<br>"
    popup_content += f"<b>Installation Date:</b> {row['Date_Time']}<br>"

    # Add VPS information if available
    if pd.notna(row['termination_date_VPS']):
        termination_date_vps_str = row['termination_date_VPS'].strftime("%Y-%m-%d")
        popup_content += f"<b>VPS Days Remaining:</b> <span id='timer_vps{index}'>{row['days_remaining_VPS']}</span> days<br>"
        popup_content += f"<b>VPS End Date:</b> {termination_date_vps_str}<br>"

    # Add CPS information if available
    if pd.notna(row['termination_date_CPS']):
        termination_date_cps_str = row['termination_date_CPS'].strftime("%Y-%m-%d")
        popup_content += f"<b>CPS Days Remaining:</b> <span id='timer_cps{index}'>{row['days_remaining_CPS']}</span> days<br>"
        popup_content += f"<b>CPS End Date:</b> {termination_date_cps_str}<br>"

    # Create a marker
    initial_color = "green" if (row['days_remaining_VPS'] > 0 or row['days_remaining_CPS'] > 0) else "red"
    folium.CircleMarker(
        location=(row['_Location_latitude'], row['_Location_longitude']),
        radius=8,
        color=initial_color,
        fill=True,
        fill_color=initial_color,
        fill_opacity=0.6,
        popup=folium.Popup(popup_content, max_width=300),
        id=f"marker{index}"
    ).add_to(m)

m.save('map_timer.html')
