# Passive Sampler Timer Map
This repository hosts a dynamic, interactive map that displays and updates passive samplers installation data using a Python script and an automated workflow via GitHub Actions. The map shows countdowns for each sampling point, with markers that adapt based on sampling type and date, removing points marked as collected and starting or restarting timers for installations.

Methodology
1. Data Preparation and Python Script

    Data Input: A CSV file provides the dataset, containing each sampling point's ID, coordinates, installation, and collection details from kobotoolbox forms.
    Date Calculations: The Python script calculates days remaining until the end of each sampling based on installation dates, using the datetime and pandas libraries for accurate time calculations.
    Map Creation: The folium library creates an HTML map:
        Sampling points are marked on the map with color-coded markers.
        Timers are displayed for each point, and points are removed if marked as "Collection"
        Countdown calculations adjust based on the type (e.g., CPS, VPS) and most recent installation or collection dates.

2. Automating Map Updates with GitHub Actions

   An automation workflow in the .github/workflows/update_map.yml file allows the map to update at regular intervals. Key steps include:
   - Triggering the Workflow: The .yml file sets up a cron job to run the script every 6 hours, checking for updated data.
   - Running the Python Script: Each run executes the map generation script in the repository, outputting an updated index.html file.
   - Committing Changes: If changes to the map are detected, GitHub Actions commits and pushes the updated HTML to the main branch.
    
## Python Package Versions

The project uses the following versions for key Python packages:

- `folium==0.14.0`
- `pandas==2.1.4`

For a complete list, refer to the [requirements.txt](requirements.txt) file.

## Dynamic Interactive Passive Samplers Map
Link: https://efthymios19.github.io/Passive-Sampler-Timer-Map/
