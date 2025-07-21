import streamlit as st
import pandas as pd
from haversine import haversine
import plotly.express as px

df = pd.read_csv('train.csv')
# print(df.head())

#limpeza de dados

df1 = df.copy()

linha = (df1['Delivery_person_Age'] != 'NaN ')

df1 = df1.loc[linha, :].copy()
df1['Delivery_person_Age'] = df1['Delivery_person_Age'].astype(int)


df1 = df1.loc[ df1['Road_traffic_density'].notnull(), : ]
df1 = df1.loc[ df1['Road_traffic_density'] != 'NaN ', : ]

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

st.title('Visão entregadores')

# sidebar

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
    options=df1.loc[df1['Road_traffic_density'] != 'NaN ', 'Road_traffic_density'].dropna().unique().tolist(),
    default=df1.loc[df1['Road_traffic_density'] != 'NaN ', 'Road_traffic_density'].dropna().unique().tolist()    
)
# if len(traffic_density) > 0:
linha2 = df1['Road_traffic_density'].isin(traffic_density)
df1 = df1.loc[linha2, :]


st.sidebar.header('--------------------------------------')

st.sidebar.markdown('### Feito por Comunidade DS')

# layout no streamlit

tab1, tab2, tab3 = st.tabs(['Visão Gerencial', '', ''])

with tab1:
    with st.container():
        col1, col2, col3, col4 = st.columns(4)

        st.title('Overall metrics')

        with col1:
            age = df1['Delivery_person_Age'].max()
            col2.metric('Maior idade', age)

        
        with col2:
            age = df1['Delivery_person_Age'].min()
            col1.metric('Menor idade', age)

        with col3:
            # st.subheader('Melhor condição de veículo')
            condition = df1['Vehicle_condition'].max()
            col3.metric('Melhor condição de veículo', condition)

        with col4:
            # st.subheader('Pior condição de veículo')
            condition = df1['Vehicle_condition'].min()
            col4.metric('Pior condição de veículo', condition)
        st.header('----------------------------------------------------------')
    with st.container():
        st.title('Avaliações')
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader('Avaliações médias por entregador')
            df_aux = df1.loc[:, ['Delivery_person_ID', 'Delivery_person_Ratings']].groupby('Delivery_person_ID').mean().reset_index()
            st.dataframe(df_aux)

        with col2:
            st.subheader('Avaliação média por trânsito')
            
            media = df1.loc[:, ['Delivery_person_Ratings', 'Road_traffic_density']].groupby('Road_traffic_density').agg({'Delivery_person_Ratings':['mean', 'std']})

            # mudança de nome das colunas
            media.columns = ['Média', 'Desvio de padrão']

            st.dataframe(media.reset_index())

            st.subheader('Avaliação média por clima')

            media = df1.loc[:, ['Delivery_person_Ratings', 'Weatherconditions']].groupby('Weatherconditions').agg({'Delivery_person_Ratings':['mean', 'std']})

            # mudança de nome das colunas
            media.columns = ['Média', 'Desvio de padrão']

            st.dataframe(media.reset_index())
    
    with st.container():
        st.header('----------------------------------------------------------')
        st.title('Velocidade de entrega')
        col1, col2 = st.columns(2)
        with col1:
            st.subheader('Top entregadores mais rápidos por cidade')

            
            df2 = (
                df1[['Delivery_person_ID', 'City', 'Time_taken(min)']]
                .groupby(['Delivery_person_ID', 'City'], as_index=False)
                .min()
                .sort_values(['City', 'Time_taken(min)'])
            )

            cidades = df2['City'].unique()
            top_por_cidade = [
                df2[df2['City'] == cidade].head(10)
                for cidade in cidades
            ]
            df3 = pd.concat(top_por_cidade, ignore_index=True)

            st.dataframe(df3)
        with col2:
            st.subheader('Top entregadores mais lentos por cidade')

            
            df2 = (
                df1[['Delivery_person_ID', 'City', 'Time_taken(min)']]
                .groupby(['Delivery_person_ID', 'City'], as_index=False)
                .max()
                .sort_values(['City', 'Time_taken(min)'])
            )

            cidades = df2['City'].unique()
            top_por_cidade = [
                df2[df2['City'] == cidade].head(10)
                for cidade in cidades
            ]
            df3 = pd.concat(top_por_cidade, ignore_index=True)

            st.dataframe(df3)