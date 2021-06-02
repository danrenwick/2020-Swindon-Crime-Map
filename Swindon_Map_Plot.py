import numpy as np
import pandas as pd
import folium
import webbrowser
from glob import glob
from folium import plugins
from folium.plugins import HeatMap

directory = #enter your directory for where you have the crime data saved

folders = glob(directory+'*')[0:-2]

li = []

#loop through folders and pull out relevant files
for folder in folders:
    tmp_df = pd.read_csv(folder+'\\'+folder[-7:]+'-wiltshire-street.csv')
    li.append(tmp_df)

df = pd.concat(li, axis = 0, ignore_index = True)

#get rid of unnecessary columns
df.drop(['Crime ID','Reported by','Falls within',
        'Location','LSOA code', 'LSOA name','Context'],
        axis = 1, inplace = True)

#filter data down to Swindon area
swindon_df = df.query('Latitude >= 51.51099 & Latitude <= 51.62152 & Longitude >= -1.91988 & Longitude <= -1.67057')

#create seperate dfs for each type so we can use specific icons for each
swindon_df_asb = swindon_df.query('`Crime type` == "Anti-social behaviour"')
swindon_df_bike = swindon_df.query('`Crime type` == "Bicycle theft"')
swindon_df_burg = swindon_df.query('`Crime type` == "Burglary"')
swindon_df_cd = swindon_df.query('`Crime type` == "Criminal damage and arson"')
swindon_df_drugs = swindon_df.query('`Crime type` == "Drugs"')
swindon_df_other_c = swindon_df.query('`Crime type` == "Other crime"')
swindon_df_other_t = swindon_df.query('`Crime type` == "Other theft"')
swindon_df_weap = swindon_df.query('`Crime type` == "Possession of weapons"')
swindon_df_pub = swindon_df.query('`Crime type` == "Public order"')
swindon_df_robb = swindon_df.query('`Crime type` == "Robbery"')
swindon_df_shop = swindon_df.query('`Crime type` == "Shoplifting"')
swindon_df_theft = swindon_df.query('`Crime type` == "Theft from the person"')
swindon_df_vehi = swindon_df.query('`Crime type` == "Vehicle crime"')
swindon_df_viol = swindon_df.query('`Crime type` == "Violence and sexual offences"')

dfs = [swindon_df_asb, swindon_df_bike, swindon_df_burg, swindon_df_cd,
       swindon_df_drugs, swindon_df_other_c, swindon_df_other_t,
       swindon_df_weap, swindon_df_pub, swindon_df_robb, swindon_df_shop,
       swindon_df_theft, swindon_df_vehi, swindon_df_viol]

icons = ['user-times','bicycle', 'unlock', 'fire', 'eyedropper', 'exclamation',
         'exclamation','warning', 'hand-stop-o', 'truck', 'shopping-basket',
         'user-times', 'car', 'warning']

icon_colors = ['orange','blue','red','red','green','gray','gray',
               'darkred','lightred','red','orange','orange','blue','darkred']

layers = ['Anti-Social Behaviour', 'Bike Theft', 'Burglary', 'Criminal Damage and Arson',
          'Drugs', 'Other Crime', 'Other Theft', 'Possession of Weapons', 'Public Order',
          'Robbery', 'Shoplifting', 'Theft from the Person', 'Vehicle Crime', 'Violence and Sexual Offences']

#set map's default load location
start_latitude = 51.5727683
start_longitude = -1.7851852

#add a basic map
swindon_map = folium.Map(
    location=[start_latitude, start_longitude],
    zoom_start=12)

#define heatmap parameters
hmap = HeatMap(list(zip(swindon_df['Latitude'].tolist(),swindon_df['Longitude'].tolist())), radius=10,ngradient={0.4:'blue',0.65:'lime',1:'red'}, show=False)
hmap.layer_name = 'Heatmap'

#loop through frames and add relevant colours, markers etc.
incidents = plugins.MarkerCluster().add_to(swindon_map)

for dfx, iconx, icon_colorx in zip(dfs, icons, icon_colors):
    for lat, lng, label, month in zip(dfx['Latitude'], dfx['Longitude'], dfx['Crime type'], dfx['Month']):
        incidents.add_child(
            folium.Marker(
                [lat, lng],
                icon = folium.Icon(color=icon_colorx,icon=iconx, prefix='fa'),
                popup = folium.Popup(folium.IFrame(f'''<html style="text-align:center; font-family:verdana; font-size:80%;width:100%; height:100%;"><strong>Month:</strong><br>{month}<br><strong>Crime Type:</strong><br>{label}</html>'''),
                                     min_width=150,max_width=150)
            )
            
        )
        
#tidy up the layers
incidents.layer_name = 'Markers'

swindon_map.add_child(incidents)
hmap.add_to(swindon_map)
folium.LayerControl(collapsed=False).add_to(swindon_map)

#save and open!
swindon_map.save('swindon_crime.html')
webbrowser.open('swindon_crime.html')
