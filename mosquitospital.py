import geopandas as gpd
import math
import folium
from folium.plugins import MarkerCluster, FloatImage

def popcolormap(pop):
    if pop <= 1.1:
        return '#F3F3F3'
    elif pop > 1.1 and pop <= 3.5:
        return '#EBC5DE'
    else:
        return '#E6A3CF'
    
def popcolormap_v2(pop):
    if pop <= 1.1:
        return '#EBC5DE'
    elif pop > 1.1 and pop <= 3.5:
        return '#E6A3CF'
    else:
        return '#E171BB'

def envcolormap(env):
    if env <= 0.35:
        return '#F3F3F3'
    elif env > 0.35 and env <= 0.74:
        return '#C2F1CD'
    else:
        return '#8BE2AF'

def envcolormap_v2(env):
    if env <= 0.35:
        return '#C2F1CD'
    elif env > 0.35 and env <= 0.74:
        return '#8BE2AF'
    else:
        return '#50E18C'

def combcolormap(pop, env):
    if pop <= 1.1 and env <= 0.35:
        return '#F3F3F3'
    elif (pop > 1.1 and pop <= 3.5) and  env <= 0.35:
        return '#EBC5DE'
    elif pop > 3.5 and env < 0.35:
        return '#E6A3CF'
    elif pop <= 1.1 and (env > 0.35 and env <= 0.74):
        return '#C2F1CD'
    elif pop <= 1.1 and env > 0.74:
        return '#8BE2AF'
    elif (pop > 1.1 and pop <= 3.5) and (env > 0.35 and env <= 0.74):
        return '#9FC7D3'
    elif (pop > 1.1 and pop <= 3.5) and env > 0.74:
        return '7EC6B0'
    elif pop > 3.5 and (env > 0.35 and env <= 0.74):
        return '#BC9FCF'
    elif pop > 3.5 and env > 0.74:
        return '#7B8EAF'
    
def combcolormap_v2(pop, env):
    if pop <= 1.1 and env <= 0.35:
        return '#F3F3F3'
    elif (pop > 1.1 and pop <= 3.5) and  env <= 0.35:
        return '#E6A3CF'
    elif pop > 3.5 and env < 0.35:
        return '#E171BB'
    elif pop <= 1.1 and (env > 0.35 and env <= 0.74):
        return '#8BE2AF'
    elif pop <= 1.1 and env > 0.74:
        return '#50E18C'
    elif (pop > 1.1 and pop <= 3.5) and (env > 0.35 and env <= 0.74):
        return '#76C3DA'
    elif (pop > 1.1 and pop <= 3.5) and env > 0.74:
        return '#46C9A1'
    elif pop > 3.5 and (env > 0.35 and env <= 0.74):
        return '#AD6DD6'
    elif pop > 3.5 and env > 0.74:
        return '#5579B6'
    
def read_data():
    gdf = gpd.read_file('RS_Pop_Envi.shp')
    return gdf

def marker():
    new_hospi = read_data()
    
    m = folium.Map(location=[0.7893,113.9213], zoom_start=5)

    mc = MarkerCluster()

    for idx, row in new_hospi.iterrows():
        if not math.isnan(row['Long']) and not math.isnan(row['Lat']):
            mc.add_child(folium.Marker([row['Lat'], row['Long']], 
                                    tooltip='This is a tooltip with <br> multiple lines')).add_to(m)

    return m

def popmap():
    new_hospi = read_data()

    m1 = folium.Map(location=[0.7893,113.9213], zoom_start=5, tiles='CartoDB dark_matter')
    pop_leg = 'Pop.png'

    for i in range(len(new_hospi)):
        # print(i)
        folium.Circle(
            location=[new_hospi.iloc[i].geometry.y, new_hospi.iloc[i].geometry.x],
            radius=5000,
            fill=True,
            fill_color=popcolormap_v2(new_hospi.iloc[i]['sum']),
            weight = 0,
        ).add_to(m1)

    FloatImage(pop_leg, bottom=5, left=3).add_to(m1)

    return m1

def envmap():
    new_hospi = read_data()

    m2 = folium.Map(location=[0.7893,113.9213], zoom_start=5, tiles='CartoDB dark_matter')
    env_leg = 'Env.png'

    for i in range(len(new_hospi)):
        # print(i)
        folium.Circle(
            location=[new_hospi.iloc[i].geometry.y, new_hospi.iloc[i].geometry.x],
            radius=5000,
            fill=True,
            fill_color=envcolormap_v2(new_hospi.iloc[i].sum_1),
            weight = 0,
        ).add_to(m2)


    FloatImage(env_leg, bottom=5, left=3).add_to(m2)

    return m2

def combmap():
    new_hospi = read_data()

    m3 = folium.Map(location=[0.7893,113.9213], zoom_start=5, tiles='CartoDB dark_matter')
    comb_leg = 'Combine 1.png'

    for i in range(len(new_hospi)):
        # print(i)
        folium.Circle(
            location=[new_hospi.iloc[i].geometry.y, new_hospi.iloc[i].geometry.x],
            radius=5000,
            fill=True,
            fill_color=combcolormap_v2(new_hospi.iloc[i]['sum'],new_hospi.iloc[i].sum_1),
            weight = 0,
        ).add_to(m3)


    FloatImage(comb_leg, bottom=5, left=3).add_to(m3)

    return m3

def popmapmarker():
    new_hospi = read_data()

    m4 = folium.Map(location=[0.7893,113.9213], zoom_start=5, tiles='CartoDB dark_matter')

    mc = MarkerCluster()

    for idx, row in new_hospi.iterrows():
        if not math.isnan(row['Long']) and not math.isnan(row['Lat']):
            mc.add_child(folium.Marker([row['Lat'], row['Long']], 
                                    tooltip='{} <br> Population Vulnerability : {}<br> Mosquito Resistance : {}'.format(row['Name'], row['sum'], row['sum']))).add_to(m4)


    comb_leg = 'Combine 1.png'

    for i in range(len(new_hospi)):
        # print(i)
        folium.Circle(
            location=[new_hospi.iloc[i].geometry.y, new_hospi.iloc[i].geometry.x],
            radius=5000,
            fill=True,
            fill_color=combcolormap_v2(new_hospi.iloc[i]['sum'],new_hospi.iloc[i].sum_1),
            weight = 0,
        ).add_to(m4)


    FloatImage(comb_leg, bottom=5, left=3).add_to(m4)

    return m4

def envmapmarker():
    new_hospi = read_data()

    m5 = folium.Map(location=[0.7893,113.9213], zoom_start=5, tiles='CartoDB dark_matter')

    mc = MarkerCluster()

    for idx, row in new_hospi.iterrows():
        if not math.isnan(row['Long']) and not math.isnan(row['Lat']):
            mc.add_child(folium.Marker([row['Lat'], row['Long']], 
                                    tooltip='{} <br> Population Vulnerability : {}'.format(row['Name'], row['sum']))).add_to(m5)


    pop_leg = 'Pop.png'

    for i in range(len(new_hospi)):
        # print(i)
        folium.Circle(
            location=[new_hospi.iloc[i].geometry.y, new_hospi.iloc[i].geometry.x],
            radius=5000,
            fill=True,
            fill_color=popcolormap_v2(new_hospi.iloc[i]['sum']),
            weight = 0,
        ).add_to(m5)

    FloatImage(pop_leg, bottom=5, left=3).add_to(m5)

    return m5

def combmapmarker():
    new_hospi = read_data()

    m6 = folium.Map(location=[0.7893,113.9213], zoom_start=5, tiles='CartoDB dark_matter')

    mc = MarkerCluster()

    for idx, row in new_hospi.iterrows():
        if not math.isnan(row['Long']) and not math.isnan(row['Lat']):
            mc.add_child(folium.Marker([row['Lat'], row['Long']], 
                                    tooltip='{} <br> Mosquito Resistance : {}'.format(row['Name'], row['sum_1']))).add_to(m6)


    env_leg = 'Env.png'

    for i in range(len(new_hospi)):
        # print(i)
        folium.Circle(
            location=[new_hospi.iloc[i].geometry.y, new_hospi.iloc[i].geometry.x],
            radius=5000,
            fill=True,
            fill_color=envcolormap_v2(new_hospi.iloc[i].sum_1),
            weight = 0,
        ).add_to(m6)

    FloatImage(env_leg, bottom=5, left=3).add_to(m6)

    return m6



