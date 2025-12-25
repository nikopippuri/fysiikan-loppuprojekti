# import necessary libraries

import streamlit as st
from streamlit_folium import st_folium
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import butter, filtfilt, find_peaks, periodogram

# read the CSV file into a DataFrame
# Use relative path
csv_path = "https://github.com/nikopippuri/fysiikan-loppuprojekti/blob/main/Linear%20Acceleration.csv"
df = pd.read_csv(csv_path)

# display title and description in Streamlit app
st.title("Askelten laskenta kiihtyvyysdatan perusteella ja reitin näyttäminen kartalla")
st.write("Keskinopeus on laskettu GPS-paikannusdatan perusteella.")




# define filter functions

from scipy.signal import butter,filtfilt
def butter_lowpass_filter(data, cutoff, nyq, order):
    normal_cutoff = cutoff / nyq
    
    b, a = butter(order, normal_cutoff, btype='low', analog=False)
    y = filtfilt(b, a, data)
    return y

def butter_highpass_filter(data, cutoff,  nyq, order):
    normal_cutoff = cutoff / nyq
    
    b, a = butter(order, normal_cutoff, btype='high', analog=False)
    y = filtfilt(b, a, data)
    return y

# plot the y-axis linear acceleration data
st.subheader("Kiihtyvyydet y-akselilla")
fig1, ax1 = plt.subplots(figsize=(12, 5))
ax1.plot(df['Time (s)'], df['Linear Acceleration y (m/s^2)'])
ax1.set_title('Kiihtyvyydet y-akselilla')
ax1.set_ylabel('Kiihtyvyys (m/s^2)')
ax1.set_xlabel('Aika (s)')
ax1.set_xlim([0, 570])
ax1.set_ylim([-20, 40])
ax1.grid(True)
ax1.legend(['Kiihtyvyys y-akselilla'])
st.pyplot(fig1)
plt.close(fig1)

# apply low-pass filter to the data and plot the results
st.subheader("Suodatettu vs. alkuperäinen data")
data = df['Linear Acceleration y (m/s^2)']
T_tot = df['Time (s)'].max() 
n = len(df['Time (s)'])
fs = n/T_tot
nyq = fs/2 
order = 3
cutoff = 1/0.4
data_filt = butter_lowpass_filter(data, cutoff, nyq, order)
fig2, ax2 = plt.subplots(figsize=(12, 5))
ax2.plot(df['Time (s)'], data, label='Alkuperäinen data')
ax2.plot(df['Time (s)'], data_filt, label='Suodatettu data')
ax2.set_xlim([420, 460])
ax2.set_ylim([-10, 20])
ax2.grid()
ax2.legend()
ax2.set_xlabel('Aika (s)')
ax2.set_ylabel('Kiihtyvyys (m/s^2)')
st.pyplot(fig2)
plt.close(fig2)

# count the number of steps based on zero crossings in the filtered data
jaksot = 0
for i in range(n-1):
    if data_filt[i]/data_filt[i+1] < 0: 
        jaksot = jaksot + 1/2

# Display the number of steps without decimals
st.write(f'**Askelten määrä on suodatetusta kiihtyvyysdatasta {int(jaksot)} askelta**, laskettuna jokaisesta nollakohdan ylityksestä.') 

#Count the number of steps using Fourier analysis

signal = df['Linear Acceleration y (m/s^2)']
t = df['Time (s)']
N = len(signal)  
dt = np.max(t) / N

# Fourier-analys

fourier = np.fft.fft(signal,n=N)
psd = fourier * np.conj(fourier) / N 
freq = np.fft.fftfreq(N, dt)
L = np.arange(1, int(N/2)) 

# Piirretään tehotiheys
st.subheader("Teho Fourier-muunnoksesta")
fig3, ax3 = plt.subplots(figsize=(12, 5))
ax3.plot(freq[L], psd[L].real)
ax3.set_xlabel('Taajuus (Hz)')
ax3.set_ylabel('Teho')
ax3.set_title('Teho Fourier-muunnoksesta')
ax3.set_xlim([0, 10])
ax3.set_ylim([0, 47600])
ax3.grid(True)
st.pyplot(fig3)
plt.close(fig3)

# Find the frequency with maximum power
f_max = freq[L][psd[L] == np.max(psd[L])][0]
# print(f'Maksimiteho taajuudella: {f_max} Hz')

# Calculate step duration
T = 1 / f_max #Askelten välinen aika,eli jaksonaika eli askeleeseen kuluva aika
# print(f'Askeleen kesto: {T} s')

# Calculate total number of steps
steps = f_max*np.max(t) #Askeleiden kokonaismäärä
st.write(f'**Askeleiden kokonaismäärä on {int(steps)} askelta**, Fourier-analyysin perusteella.')

#import necessary libraries for GPS data processing

from math import radians, cos, sin, asin, sqrt

# read the GPS location data from CSV file
location_csv_path = "https://github.com/nikopippuri/fysiikan-loppuprojekti/blob/main/Location.csv"
df = pd.read_csv(location_csv_path)

# define haversine function to calculate distance between two GPS coordinates

def haversine(lon1, lat1, lon2, lat2):
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a))
    r = 6371  # km
    return c * r


# calculate distances and velocities between consecutive GPS points
df['dist_km'] = 0.0
df['time_h'] = 0.0

for i in range(len(df) - 1):
    df.loc[i, 'dist_km'] = haversine(df.loc[i,'Longitude (°)'], df.loc[i,'Latitude (°)'],
                                     df.loc[i+1,'Longitude (°)'], df.loc[i+1,'Latitude (°)'])
    df.loc[i, 'time_h'] = (df.loc[i+1,'Time (s)'] - df.loc[i,'Time (s)']) / 3600

# vältä jako nollalla (paikallaan olo / sama timestamp)
df['velocity_kmh'] = np.where(df['time_h'] > 0, df['dist_km'] / df['time_h'], np.nan)
df['tot_dist_km'] = df['dist_km'].cumsum()

# calculate total distance and average speed
st.subheader("GPS-datan analyysi")
total_distance_m = df['dist_km'].sum() * 1000
average_speed_kmh = df['velocity_kmh'].mean()

col1, col2 = st.columns(2)
with col1:
    st.metric("Kuljettu matka", f"{int(total_distance_m)} metriä")
with col2:
    st.metric("Keskinopeus", f"{int(average_speed_kmh)} km/h")

# Count step distance based on total distance and number of steps
step_distance_m = total_distance_m / int(steps)

# Display the average step distance with two decimal places
st.metric("Askelten keskipituus", f"{step_distance_m:.2f} metriä")

# Summary section
st.divider()
st.subheader("Yhteenveto")
summary_col1, summary_col2, summary_col3 = st.columns(3)
with summary_col1:
    st.metric("Askeleita (Fourier)", f"{int(steps)}")
with summary_col2:
    st.metric("Kuljettu matka", f"{int(total_distance_m)} m")
with summary_col3:
    st.metric("Keskipituus/askel", f"{step_distance_m:.2f} m")

import folium
from folium.plugins import Fullscreen, MiniMap, MeasureControl

# Trim first 10 seconds
df_filtered = df[df['Time (s)'] > 10].copy()

# Coordinates list
coords = df_filtered[['Latitude (°)', 'Longitude (°)']].values.tolist()

# Modern basemap 
my_map = folium.Map(
    location=coords[len(coords)//2],
    zoom_start=14,
    tiles="CartoDB positron",
    control_scale=True
)

# Fit map to route bounds
my_map.fit_bounds(coords)

#Route "outerline"
folium.PolyLine(
    coords,
    color="#ff7f0e",
    weight=8,
    opacity=0.9
).add_to(my_map)

# Main route line
folium.PolyLine(
    coords,
    color="#1f77b4",  
    weight=4,
    opacity=1
).add_to(my_map)

# Start / End markers
start = coords[0]
end = coords[-1]

# Add start and end markers

folium.Marker(
    start,
    popup="Start",
    tooltip="Start",
    icon=folium.Icon(color="green", icon="play", prefix="fa")
).add_to(my_map)

folium.Marker(
    end,
    popup="Finish",
    tooltip="Finish",
    icon=folium.Icon(color="red", icon="stop", prefix="fa")
).add_to(my_map)

# UI plugins
Fullscreen(position="topright").add_to(my_map)
MiniMap(toggle_display=True, position="bottomright").add_to(my_map)
MeasureControl(position="topleft", primary_length_unit="meters").add_to(my_map)

# Display map in Streamlit
st.subheader("Reitti kartalla")
st_folium(my_map, width=700, height=500)


