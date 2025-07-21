import streamlit as st
from PIL import Image
from pathlib import Path
BASE = Path(__file__).parent
logo = Image.open(BASE / "logo2.jpg")
st.image(logo)

# sidebar

st.sidebar.markdown('# Curry Company')

st.sidebar.image(logo)

st.sidebar.markdown('## Fastest Delivery in Town')

st.sidebar.markdown('### --------------------------------------')

st.write('# Curry Company Growth Dashboard')