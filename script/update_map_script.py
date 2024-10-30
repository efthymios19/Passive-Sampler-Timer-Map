import pandas as pd
import folium 
from datetime import timedelta

### Import kobo-csv

ps=pd.read_csv('data/data.csv', sep=';')

# Convert 'Date_Time' to datetime and sort by date for each sampling point
filtered_ps=ps
filtered_ps['Date_Time'] = pd.to_datetime(filtered_ps['Date_Time'])
filtered_ps = filtered_ps.sort_values(by=['ID', 'Date_Time']).groupby('ID').last().reset_index()

# Calculate days remaining for each row with the same function as before
today = pd.Timestamp.now(tz='Europe/Athens')

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

# Create the map
m = folium.Map(location=[filtered_ps['_Location_latitude'].mean(), filtered_ps['_Location_longitude'].mean()], zoom_start=10)

# Add markers based on the 'Installation', 'Collection', or 'Installation/Collection' status
for index, row in filtered_ps.iterrows():
    if row['Installation/Collection'] == 'Collection':
        # Skip this point; it won't appear on the map
        continue
    
    # Popup content setup
    popup_content = f"<b>ID:</b> {row['ID']}<br><b>Type:</b> {row['Passive Sampler Type']}<br><b>Installation Date:</b> {row['Date_Time']}<br>"
    
    # Add VPS or CPS information if relevant
    if pd.notna(row['termination_date_VPS']):
        termination_date_vps_str = row['termination_date_VPS'].strftime("%Y-%m-%d")
        popup_content += f"<b>VPS Days Remaining:</b> <span id='timer_vps{index}'>{row['days_remaining_VPS']}</span> days<br><b>VPS End Date:</b> {termination_date_vps_str}<br>"
    if pd.notna(row['termination_date_CPS']):
        termination_date_cps_str = row['termination_date_CPS'].strftime("%Y-%m-%d")
        popup_content += f"<b>CPS Days Remaining:</b> <span id='timer_cps{index}'>{row['days_remaining_CPS']}</span> days<br><b>CPS End Date:</b> {termination_date_cps_str}<br>"
    
    # Marker color based on days remaining
    initial_color = "green" if (row['days_remaining_VPS'] > 0 or row['days_remaining_CPS'] > 0) else "red"
    folium.CircleMarker(
        location=(row['_Location_latitude'], row['_Location_longitude']),
        radius=8,
        color=initial_color,
        fill=True,
        fill_color=initial_color,
        fill_opacity=0.6,
        popup=folium.Popup(popup_content, max_width=300),
    ).add_to(m)

# Add a legend
legend_html = """
<div style="position: fixed; 
     bottom: 50px; left: 50px; width: 150px; height: 90px; 
     background-color: white; z-index:9999; font-size:14px;
     border:2px solid grey; border-radius:8px; padding: 10px;">
     <strong>Legend</strong><br>
     <i class="fa fa-circle" style="color:green"></i> Installed<br>
     <i class="fa fa-circle" style="color:red"></i> Ready to Collect
</div>
"""

m.get_root().html.add_child(folium.Element(legend_html))
m.save('index.html')
