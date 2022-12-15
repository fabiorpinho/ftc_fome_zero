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
#st.header( '📊 Visão Geral' )
st.markdown("<h1 style = 'font-size: 30px; text-align: center'>📊 Visão Geral</h1>", unsafe_allow_html=True)

with st.container():
    st.markdown( """---""" )
    st.markdown("<h1 style = 'font-size: 30px; text-align: center'>Métricas Gerais</h1>", unsafe_allow_html=True)
   
    col1, col2, col3, col4, col5 = st.columns( 5 )
    with col1:
        restaurantes = df.loc[:,'restaurant_id'].nunique()
        col1.metric( 'Restaurantes Cadastrados', restaurantes )  
        
    with col2:
        paises = df.loc[:,'country_code'].nunique()
        col2.metric( 'Países Cadastrados', paises )        

    with col3:
        cidades = df.loc[:,'city'].nunique()
        col3.metric( 'Cidades Cadastradas', cidades )

    with col4:
        avaliacoes = df.loc[:,'votes'].sum()
        col4.metric( 'Avaliações Feitas na Plataforma', f"{avaliacoes:,}".replace(",", "."))
        
    with col5:
        tipos = df.loc[:,'cuisines'].nunique()
        col5.metric( 'Tipos de Culinárias Oferecidas', tipos )
        
    st.markdown('''
    <style>
    /*center metric label*/
    [data-testid="stMetricLabel"] > div:nth-child(1) {
        justify-content: center;
       
    }

    /*center metric value*/
    [data-testid="stMetricValue"] > div:nth-child(1) {
        justify-content: center;
        
    }
    </style>
    ''', unsafe_allow_html=True)
    
    st.markdown("""
    <style>
    div[data-testid="metric-container"] {
       background-color: rgba(28, 131, 225, 0.1);
       border: 1px solid rgba(28, 131, 225, 0.1);
       justify-content: center
       padding: 5% 5% 5% 10%;
       border-radius: 5px;
       color: rgb(30, 103, 119);
       overflow-wrap: break-word;
    }

    /* breakline for metric text         */
    div[data-testid="metric-container"] > label[data-testid="stMetricLabel"] > div {
       overflow-wrap: break-word;
       justify-content: center
       white-space: break-spaces;
       color: rgb(138,0,0); 
       font-weight:900;
       
    }
    </style>
    """
    , unsafe_allow_html=True)
    
   
    


with st.container():
    st.markdown( """---""" )
    #st.title( "Localização Geográfica dos Restaurantes" )
    st.markdown("<h1 style = 'font-size: 30px; text-align: center'>Localização Geográfica dos Restaurantes</h1>", unsafe_allow_html=True)

    
    mapa = folium.Map( max_bounds=True )

    marker_cluster = MarkerCluster().add_to(mapa)
    for index, line in df1.iterrows():
        name = line["restaurant_name"]
        price_for_two = line["average_cost_for_two"]
        cuisine = line["cuisines"]
        currency = line["currency"]
        rating = line["aggregate_rating"]
        #color = f'{line["color_name"]}'
        color = line["color_name"]

        html = "<p><strong>{}</strong></p>"
        html += "<p>Price: {},00 ({}) for two"
        html += "<br />Type: {}"
        html += "<br />Aggregate Rating: {}/5.0"
        html = html.format(name, price_for_two, currency, cuisine, rating)

        popup = folium.Popup(
            folium.Html(html, script=True),
            max_width=500,
        )

        folium.Marker(
            [line["latitude"], line["longitude"]],
            popup=popup,
            #icon=folium.Icon(color=color, icon="home", prefix="fa"),
            icon=folium.Icon(color=color, icon="cutlery", prefix="fa"),
        ).add_to(marker_cluster)
        
    #folium_static(mapa, width=1024 , height=600)
    folium_static(mapa, width=1400 , height=600)


