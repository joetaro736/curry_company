import streamlit as st
import pandas as pd
from haversine import haversine
import plotly.express as px
from visao_empresa import limpeza_de_dados

df = pd.read_csv('train.csv')
# print(df.head())
st.set_page_config(page_title='Visão Entregadores', page_icon='', layout='wide')
# funções

def top_delivers_rapidos(df1):
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

def top_delivers_lentos(df1):

                
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

#limpeza de dados
df1 = limpeza_de_dados(df)

st.title('Visão entregadores')

# sidebar

st.sidebar.markdown('# Curry Company')

st.sidebar.image('logo2.jpg')

st.sidebar.markdown('## Fastest Delivery in Town')

st.sidebar.markdown('### --------------------------------------')

from datetime import datetime

# Definição do slider para intervalo de datas
data_inicial, data_final = st.sidebar.slider(
    'De – até',
    value=(datetime(2022, 2, 11), datetime(2022, 4, 1)),
    min_value=datetime(2022, 2, 11),
    max_value=datetime(2022, 4, 6),
    format='DD-MM-YYYY'
)

# Exemplo de DataFrame com coluna Order_Date
# df1['Order_Date'] deve ser do tipo datetime
linhas = (df1['Order_Date'] >= data_inicial) & (df1['Order_Date'] <= data_final)
df_filtrado = df1.loc[linhas, :]

st.write(f"Filtrando datas de {data_inicial.strftime('%d-%m-%Y')} até {data_final.strftime('%d-%m-%Y')}")
st.dataframe(df_filtrado)

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
            top_delivers_rapidos(df1)
        with col2:
            st.subheader('Top entregadores mais lentos por cidade')
            top_delivers_lentos(df1)