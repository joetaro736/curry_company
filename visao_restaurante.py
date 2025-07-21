import streamlit as st
import pandas as pd
from haversine import haversine
import plotly.express as px
import plotly.graph_objects as go
import numpy as np

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
df1 = df1.loc[linha1, :]

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

st.title('Visão restaurantes')

tab1, tab2, tab3 = st.tabs(['Visão Gerencial', '', ''])

with tab1:
    with st.container():
        st.title('Overal metrics')

        col1, col2, col3, col4, col5, col6 = st.columns(6)

        with col1:

            entregadores = df1['Delivery_person_ID'].nunique()
            col1.metric('Quantidade de entregadores únicos', entregadores)

        with col2:

            cols = ['Delivery_location_latitude', 'Delivery_location_longitude', 'Restaurant_latitude', 'Restaurant_longitude']
            df1['Distance'] = df1.loc[0:10, cols].apply(lambda x: haversine((x['Restaurant_latitude'], x['Restaurant_longitude']), (x['Delivery_location_latitude'], x['Delivery_location_longitude'])), axis=1)
            col2.metric('Distância média do reustaurante', df1['Distance'].mean())


        with col3:
            cols = ['Time_taken(min)', 'Festival']

            df_aux = (df1
                .loc[:, cols]
                .groupby('Festival')
                .agg({'Time_taken(min)': ['mean', 'std']})
            )
            df_aux.columns = ['AVG_time', 'STD_time']
            df_aux = df_aux.reset_index()

            avg_time = (
                df_aux
                .loc[df_aux['Festival'] == 'Yes', 'AVG_time']
                .astype(float)
                .iloc[0]   # pega o primeiro (único) valor
            )

            col3.metric(
                'Tempo médio de entrega com festival',
                f"{avg_time:.1f} min")


        with col4:
            cols = ['Time_taken(min)', 'Festival']

            df_aux = (df1
                .loc[:, cols]
                .groupby('Festival')
                .agg({'Time_taken(min)': ['mean', 'std']})
            )
            df_aux.columns = ['AVG_time', 'STD_time']
            df_aux = df_aux.reset_index()

            avg_time = (
                df_aux
                .loc[df_aux['Festival'] == 'Yes', 'STD_time']
                .astype(float)
                .iloc[0]   # pega o primeiro (único) valor
            )

            col4.metric(
                'Desvio padrão médio de entrega com festival',
                f"{avg_time:.1f} min")

        with col5:
            cols = ['Time_taken(min)', 'Festival']

            df_aux = (df1
                .loc[:, cols]
                .groupby('Festival')
                .agg({'Time_taken(min)': ['mean', 'std']})
            )
            df_aux.columns = ['AVG_time', 'STD_time']
            df_aux = df_aux.reset_index()

            avg_time = (
                df_aux
                .loc[df_aux['Festival'] == 'No', 'AVG_time']
                .astype(float)
                .iloc[0]   # pega o primeiro (único) valor
            )

            col5.metric(
                'Tempo médio de entrega sem festival',
                f"{avg_time:.1f} min")

        with col6:
            cols = ['Time_taken(min)', 'Festival']

            df_aux = (df1
                .loc[:, cols]
                .groupby('Festival')
                .agg({'Time_taken(min)': ['mean', 'std']})
            )
            df_aux.columns = ['AVG_time', 'STD_time']
            df_aux = df_aux.reset_index()

            avg_time = (
                df_aux
                .loc[df_aux['Festival'] == 'No', 'STD_time']
                .astype(float)
                .iloc[0]   # pega o primeiro (único) valor
            )

            col4.metric(
                'Desvio padrão médio de entrega sem festival',
                f"{avg_time:.1f} min")
    with st.container():
        st.header('-' * 30)
        st.title('Tempo médio de entrega por cidade')

        # 1. Calcular a distância (em km por padrão) entre restaurante e entrega
        df1['Distance'] = df1.apply(
            lambda x: haversine(
                (x['Restaurant_latitude'], x['Restaurant_longitude']),
                (x['Delivery_location_latitude'], x['Delivery_location_longitude'])
            ),
            axis=1
        )

        # 2. Agregar métricas por cidade

        linha = df1['City'] != 'NaN '

        city_stats = (
            df1.loc[linha, :].groupby('City')
            .agg(Distância_Média=('Distance', 'mean'), Qtde=('Distance', 'count'))
            .reset_index()
        )

        # 3. Criar gráfico de pizza com Plotly
        fig = go.Figure(data=[go.Pie(
            labels=city_stats['City'],
            values=city_stats['Distância_Média'],
            pull=[0.1] * len(city_stats),          # afasta todos os slices
            hoverinfo='label+value+percent',       # mostra detalhe ao passar mouse
            textinfo='label+percent'               # exibe labels + percentuais dentro
        )])
        fig.update_layout(title='Distância média de entrega por cidade')

        # 4. Exibir no Streamlit, ajustando à largura do container
        st.plotly_chart(fig, use_container_width=True)
    with st.container():
        st.header('-' * 30)
        st.title('Distribuição do tempo')
        col1, col2 = st.columns(2)

        with col1:
            cols = ['Time_taken(min)','City']
            df_aux = df1.loc[df1['City'] != 'NaN ', cols].groupby('City').agg({'Time_taken(min)': ['mean', 'std']})
            df_aux.columns = ['AVG_time', 'STD_time']
            df_aux = df_aux.reset_index()

            fig = go.Figure()
            fig.add_trace(go.Bar(name='Control', x=df_aux['City'], y=df_aux['AVG_time'], error_y=dict(type='data', array=df_aux['STD_time'])))
            fig.update_layout(barmode='group')

            st.plotly_chart(fig)
            

        with col2:
            

            cols = ['Time_taken(min)', 'City', 'Road_traffic_density']

            # 0. Remover linhas com NaN nas colunas necessárias
            df_aux = df1[cols].dropna(subset=cols)

            # 1. Agrupar e calcular média + desvio padrão
            df_aux = df_aux.groupby(['City', 'Road_traffic_density']) \
                        .agg({'Time_taken(min)': ['mean', 'std']})
            df_aux.columns = ['AVG_time', 'STD_time']
            df_aux = df_aux.reset_index()

            # 2. Plotar sunburst, usando desvio padrão para colorir
            fig = px.sunburst(
                df_aux,
                path=['City', 'Road_traffic_density'],
                values='AVG_time',
                color='STD_time',
                color_continuous_scale='RdBu',
                color_continuous_midpoint=np.average(df_aux['STD_time'])  # define o ponto médio da escala :contentReference[oaicite:1]{index=1}
            )

            # 3. Mostrar no Streamlit
            st.plotly_chart(fig, use_container_width=True)



    with st.container():
        st.header('-' * 30)
        st.title('Distribuição da distância')

        df_aux = (df1.loc[:, ['Time_taken(min)', 'City', 'Type_of_order']].groupby(['City', 'Type_of_order']).agg({'Time_taken(min)': ['mean', 'std']}))
        df_aux.columns = ['AVG_time', 'STD_time']
        df_aux = df_aux.reset_index()

        st.dataframe(df_aux)
