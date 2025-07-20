import streamlit as st
from PIL import Image

st.set_page_config(page_title='Home', page_icon='Data-FTC🎲')
# image_path = 'c:/Users/Luísa Aragão A Dias/Desktop/joe/sst/analise_de_dados/ftc/'
image = Image.open('logo2.jpg')
st.image(image, width=120)

# sidebar

st.sidebar.markdown('# Curry Company')

st.sidebar.image('logo2.jpg')

st.sidebar.markdown('## Fastest Delivery in Town')

st.sidebar.markdown('### --------------------------------------')

st.write('# Curry Company Growth Dashboard')