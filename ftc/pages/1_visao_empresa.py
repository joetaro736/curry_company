import pandas as pd
from haversine import haversine
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
import folium
from streamlit_folium import folium_static
st.set_page_config(page_title='Visão Empresa', page_icon='', layout='wide')
df = pd.read_csv('train.csv')
# print(df.head())

# funções



def order_share_by_week(df1):

            df['week'] = df['Order_Date'].dt.strftime('%U')
            df1['week'] = df['week']
            cols = ['ID', 'week']
            df_aux = df1.loc[:, cols].groupby('week').count().reset_index()
            fig = px.line(df_aux, x='week', y='ID')
            st.plotly_chart(fig, use_container_width=True)

def traffic_order_city(df1):
    st.header('Tipo de tráfego por cidade')
    df_aux = df1.loc[:, ['ID', 'Road_traffic_density', 'City']].groupby(['City','Road_traffic_density']).count().reset_index()
    df_aux = df_aux.loc[df_aux['Road_traffic_density'] != 'NaN ', :]
    df_aux = df_aux.loc[df_aux['City'] != 'NaN ', :]

    fig=px.scatter(df_aux, x='City', y='Road_traffic_density', size='ID')
    st.plotly_chart(fig, use_container_width=True)


def traffic_order_share(df1):
    st.header('Número de entregas por tipo de tráfego')
    df_aux = df1.loc[:, ['ID', 'Road_traffic_density']].groupby('Road_traffic_density').count().reset_index()
    df_aux = df_aux.loc[df_aux['Road_traffic_density'] != 'NaN ', :]
    df_aux['perc'] = df_aux['ID'] / df_aux['ID'].sum()

    fig = px.pie(df_aux, values='perc', names='Road_traffic_density')
    st.plotly_chart(fig, use_container_width=True)

def order_metric(df1):
    st.markdown('## Entregas por dia')
    cols = ['ID', 'Order_Date']
    df_aux = df1.loc[: , cols].groupby('Order_Date').count().reset_index()
    fig = px.bar(df_aux, x='Order_Date', y='ID')
    st.plotly_chart(fig, use_container_width=True)

def limpeza_de_dados(df):

    df1 = df.copy()

    linha = (df1['Delivery_person_Age'] != 'NaN ')
    linha1 = (df1['Road_traffic_density'] != 'NaN ')
    df1 = df1.loc[linha, :].copy()
    df1['Delivery_person_Age'] = df1['Delivery_person_Age'].astype(int)

    df1 = df1.loc[linha1, :].copy()

    linha1 = (df1['City'] != 'NaN ')
    df1 = df1.loc[linha1, :].copy()

    df1 = df.loc[df['Delivery_person_Ratings'] != 'NaN ', :]
    df['Delivery_person_Ratings'] = df1['Delivery_person_Ratings'].astype(float)

    df1 = df.loc[df['Delivery_person_Ratings'] != 'NaN ', :]
    df['Delivery_person_Ratings'] = df1['Delivery_person_Ratings'].astype(float)

    df1['Order_Date'] = pd.to_datetime(df1['Order_Date'], format='%d-%m-%Y')
    df['Order_Date'] = df1['Order_Date']

    #df1 = df1.loc[df1['multiple_deliveries'] != 'NaN ', :]
    # df1['multiple_deliveries'] = df1['multiple_deliveries'].astype(int)

    linha1 = (df1['Festival'] != 'NaN ')
    df1 = df1.loc[linha, :]

    df1.loc[: , 'Festival'] = df1.loc[: , 'Festival'].str.strip()

    df1.loc[: , 'ID'] = df1.loc[: , 'ID'].str.strip()

    df1['Time_taken(min)'] = df1['Time_taken(min)'].apply(lambda x: x.split(' ')[1])
    df1['Time_taken(min)'] = df1['Time_taken(min)'].astype( int )

    # visão empresa
    st.title('Curry Company')

    return df1

df1 = limpeza_de_dados(df)


# layout no streamlit



st.sidebar.markdown('# Curry Company')

st.sidebar.image('logo2.jpg')

st.sidebar.markdown('## Fastest Delivery in Town')

st.sidebar.markdown('### --------------------------------------')

from datetime import datetime

data_slider = st.sidebar.slider(
    'Até qual valor?',
    value=datetime(2022, 4, 1),
    min_value=datetime(2022, 2, 11),
    max_value=datetime(2022, 4, 6),
    format='DD-MM-YYYY')

linhas = df1['Order_Date'] < data_slider
df1 = df1.loc[linhas, :]

# st.header(data_slider)

traffic_density = st.sidebar.multiselect(
    'Selecione o nível de tráfego:',
    options=df1['Road_traffic_density'].dropna().unique().tolist(),
    default=df1['Road_traffic_density'].dropna().unique().tolist()    
)
# if len(traffic_density) > 0:
linha2 = df1['Road_traffic_density'].isin(traffic_density)
df1 = df1.loc[linha2, :]

st.dataframe(df1.head())

st.sidebar.header('--------------------------------------')

st.sidebar.markdown('### Feito por Comunidade DS')

# layout no streamlit

tab1, tab2, tab3 = st.tabs(['Visão Gerencial', 'Visão Tática', 'Visão Geográfica'])

with tab1:
    
    order_metric(df1)

    with st.container():
        col1, col2 = st.columns(2)

        with col1:
            traffic_order_share(df1)
        
        with col2:
            traffic_order_city(df1)
with tab2:
    with st.container():
        st.markdown('## Pedidos por semana')
        
        order_share_by_week(df1)

    with st.container():
        st.markdown('## Pedidos por entregador')
        df_aux = df1.copy()
        df_aux1 = df1.loc[:, ['ID', 'week']].groupby('week').count().reset_index()
        df_aux2 = df1.loc[:, ['Delivery_person_ID', 'week']].groupby('week').nunique().reset_index()
        df_aux['week'] = df_aux1['week'].astype(int)
        df_aux['Delivery_person_ID'] = df_aux2['Delivery_person_ID'].astype(int)
        df_aux = pd.merge(df_aux1, df_aux2, how='inner')
        df_aux['Order_by_delivery'] = df_aux['ID'] / df_aux['Delivery_person_ID']
        fig=px.line(df_aux, x='week', y='Order_by_delivery')
        st.plotly_chart(fig, use_container_width=True)
with tab3:
    st.markdown('## Localizção dos pedidos')
    df_aux = df1.loc[:, ['City', 'Road_traffic_density', 'Delivery_location_latitude', 'Delivery_location_longitude']].groupby(['City', 'Road_traffic_density']).median().reset_index()
    df_aux = df_aux.loc[df_aux['City'] != 'NaN ', :]
    df_aux = df_aux.loc[df_aux['Road_traffic_density'] != 'NaN ', :]

    map = folium.Map()

    for index, location_info in df_aux.iterrows():
        folium.Marker([location_info['Delivery_location_latitude'], location_info['Delivery_location_longitude']], popup=location_info[['City', 'Road_traffic_density']]).add_to(map)
    folium_static(map, width=1024, height=600)