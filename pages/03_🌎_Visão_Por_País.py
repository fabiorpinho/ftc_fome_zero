#importação de bibliotecas
import pandas as pd
import inflection 
import folium
from folium.plugins import MarkerCluster
import plotly.express as px
import plotly.graph_objects as go
import numpy  as np
import streamlit as st
from PIL import Image
from streamlit_folium import folium_static

#leitura do arquivo de entrada
df = pd.read_csv( 'zomato.csv'  )

#limpeza de dados
def rename_columns(dataframe):
    df = dataframe.copy()
    title = lambda x: inflection.titleize(x)
    snakecase = lambda x: inflection.underscore(x)
    spaces = lambda x: x.replace(" ", "")
    cols_old = list(df.columns)
    cols_old = list(map(title, cols_old))
    cols_old = list(map(spaces, cols_old))
    cols_new = list(map(snakecase, cols_old))
    df.columns = cols_new
    return df
df = rename_columns(df)
df = df.drop_duplicates()
df = df.loc[df['cuisines'].notnull(), :]
COUNTRIES = {
1: "India",
14: "Australia",
30: "Brazil",
37: "Canada",
94: "Indonesia",
148: "New Zeland",
162: "Philippines",
166: "Qatar",
184: "Singapure",
189: "South Africa",
191: "Sri Lanka",
208: "Turkey",
214: "United Arab Emirates",
215: "England",
216: "United States of America",
}
def country_name(country_id):
    return COUNTRIES[country_id]
df = df.reset_index()
df["country"] = df.loc[:, "country_code"].apply(lambda x: country_name(x))
df["cuisines"] = df.loc[:, "cuisines"].apply(lambda x: x.split(",")[0])
COLORS = {
"3F7E00": "darkgreen",
"5BA829": "green",
"9ACD32": "lightgreen",
"CDD614": "orange",
"FFBA00": "red",
"CBCBC8": "darkred",
"FF7800": "darkred",
}
def color_name(color_code):
    return COLORS[color_code]
df["color_name"] = df.loc[:, "rating_color"].apply(lambda x: color_name(x))
def create_price_type(price_range):
    if price_range == 1:
        return "cheap"
    elif price_range == 2:
        return "normal"
    elif price_range == 3:
        return "expensive"
    else:
        return "gourmet"
df["price_type"] = df.loc[:, "price_range"].apply(lambda x: create_price_type(x))

# =======================================
# Barra Lateral
# =======================================

st.set_page_config(layout="wide")
with st.sidebar:
    st.markdown(
        """
        <style>
            [data-testid=stSidebar] [data-testid=stImage]{
                text-align: center;
                display: block;
                margin-left: auto;
                margin-right: auto;
                width: 100%;
            }
        </style>
        """, unsafe_allow_html=True
    )
    st.markdown( '## Filtros' )

    countries = st.multiselect( 
        'Quais países deseja filtrar?',
        ['Philippines', 'Brazil', 'Australia', 'United States of America', 'Canada', 'Singapure', 'United Arab Emirates', 'India', 'Indonesia', 'New Zeland', 'England', 'Qatar', 'South Africa', 'Sri Lanka', 'Turkey'], 
        default=['Brazil', 'Canada', 'England', 'Qatar', 'England', 'Australia', 'South Africa'] )

    st.markdown( """---""" )
    st.markdown("<h6 style='text-align: center; color: black;'>Desenvolvido por:</h6>", unsafe_allow_html=True)
    st.image('cds.png', width=180 )
    st.write("<h6 style='text-align: center; color: black;'>Time de Data Science no Discord:<br>@Fabio Rodrigues Pinho#6975</h6>", unsafe_allow_html=True)


    # Filtro de transito
    linhas_selecionadas = df['country'].isin( countries )
    df1 = df.loc[linhas_selecionadas, :]



# =======================================
# Layout no Streamlit
# =======================================
#st.header( '🌎 Visão por País' )
st.markdown("<h1 style = 'font-size: 30px; text-align: center'>🌎 Visão por País</h1>", unsafe_allow_html=True)

with st.container():
    st.markdown( """---""" )
    st.markdown("<h1 style = 'font-size: 20px; text-align: center'>Quantidade de Restaurantes Registrados por País</h1>", unsafe_allow_html=True)
    fig = px.bar(
        df1.loc[:, ['restaurant_id', 'country']].groupby('country').count().sort_values('restaurant_id', ascending=False).reset_index(),
        x="country",
        y="restaurant_id",
        text="restaurant_id",
        #title="Quantidade de Restaurantes Registrados por País",
        labels={
            "country": "Países",
            "restaurant_id": "Quantidade de Restaurantes",
        },
    )
    
    st.plotly_chart(fig, use_container_width=True)

with st.container():
    st.markdown( """---""" )
    st.markdown("<h1 style = 'font-size: 20px; text-align: center'>Quantidade de Cidades Registradas por País</h1>", unsafe_allow_html=True)
    fig = px.bar(
        df1.loc[:, ['city', 'country']].groupby('country').nunique().sort_values('city', ascending=False).reset_index(),
        x="country",
        y="city",
        text="city",
        #title="Quantidade de Cidades Registradas por País",
        labels={
            "country": "Paises",
            "city": "Quantidade de Cidades",
        },
    )
    
    st.plotly_chart(fig, use_container_width=True)

with st.container():
    st.markdown( """---""" )
    st.markdown("<h1 style = 'font-size: 30px; text-align: center'>Médias</h1>", unsafe_allow_html=True)
   
    col1, col2 = st.columns( 2 )
    with col1:
        st.markdown("<h1 style = 'font-size: 20px; text-align: center'>Média de Avaliações Feitas por País</h1>", unsafe_allow_html=True)
        fig = px.bar(
            df1.loc[:, ['votes', 'country']].groupby('country').mean().round(2).sort_values('votes', ascending=False).reset_index(),
            x="country",
            y="votes",
            text="votes",
            #title="Quantidade de Cidades Registradas por País",
            labels={
                "country": "Paises",
                "votes": "Quantidade de Avaliações",
            },
        )

        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.markdown("<h1 style = 'font-size: 20px; text-align: center'>Média do Preço de um prato para duas pessoas por País</h1>", unsafe_allow_html=True)
        fig = px.bar(
            df1.loc[:, ['average_cost_for_two', 'country']].groupby('country').mean().round(2).sort_values('average_cost_for_two', ascending=False).reset_index(),
            x="country",
            y="average_cost_for_two",
            text="average_cost_for_two",
            #title="Quantidade de Cidades Registradas por País",
            labels={
                "country": "Paises",
                "average_cost_for_two": "Preço de prato para duas pessoas",
            },
        )

        st.plotly_chart(fig, use_container_width=True)