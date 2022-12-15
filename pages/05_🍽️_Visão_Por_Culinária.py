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
df1=df.copy()

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
    
    top_n = st.slider(
        "Selecione a quantidade de Restaurantes que deseja visualizar", 1, 20, 10
    )


    countries = st.multiselect( 
        'Quais países deseja filtrar?',
        ['Philippines', 'Brazil', 'Australia', 'United States of America', 'Canada', 'Singapure', 'United Arab Emirates', 'India', 'Indonesia', 'New Zeland', 'England', 'Qatar', 'South Africa', 'Sri Lanka', 'Turkey'], 
        default=['Brazil', 'Canada', 'England', 'Qatar', 'England', 'Australia', 'South Africa'] )
    
    cuisines = st.sidebar.multiselect(
            "Escolha os Tipos de Culinária ",
            df.loc[:, "cuisines"].unique().tolist(),
            default=[
                "Home-made",
                "BBQ",
                "Japanese",
                "Brazilian",
                "Arabian",
                "American",
                "Italian",
            ],
        )
    
    st.markdown( """---""" )
    st.markdown("<h6 style='text-align: center; color: black;'>Desenvolvido por:</h6>", unsafe_allow_html=True)
    st.image('cds.png', width=180 )
    st.write("<h6 style='text-align: center; color: black;'>Time de Data Science no Discord:<br>@Fabio Rodrigues Pinho#6975</h6>", unsafe_allow_html=True)


    
    linhas_selecionadas1 = df1['country'].isin( countries )
    df1 = df1.loc[linhas_selecionadas1, :]
    
    linhas_selecionadas2 = df1['cuisines'].isin( cuisines )
    df1 = df1.loc[linhas_selecionadas2, :]



# =======================================
# Layout no Streamlit
# =======================================
#st.header( '🍽️Visão Por Tipo de Culinária' )
st.markdown("<h1 style = 'font-size: 30px; text-align: center'>🍽️ Visão por Tipo de Culinária</h1>", unsafe_allow_html=True)

with st.container():
    st.markdown( """---""" )
    st.markdown("<h1 style = 'font-size: 30px; text-align: center'>Melhores Restaurantes dos Principais tipos Culinários</h1>", unsafe_allow_html=True)
   
    col1, col2, col3, col4, col5 = st.columns( 5 )
    with col1:
        df_aux1 = df.loc[df['cuisines'] == 'Italian', :]
        df_aux2 = df_aux1.loc[:, ['restaurant_id', 'restaurant_name', 'aggregate_rating']].groupby(['restaurant_id', 'restaurant_name']).mean().reset_index().round(2)
        df_aux3 = df.loc[:, ['restaurant_id', 'country', 'city', 'average_cost_for_two', 'currency']]
        df_aux = pd.merge( df_aux2, df_aux3, how='inner' )
        df_aux = df_aux.sort_values('aggregate_rating', ascending = False).reset_index()
        restaurante = df_aux.loc[0, 'restaurant_name']
        avaliacao = df_aux.loc[0, 'aggregate_rating']
        country = df_aux.loc[0, 'country']
        city = df_aux.loc[0, 'city']
        preco = df_aux.loc[0, 'average_cost_for_two']
        moeda = df_aux.loc[0, 'currency']
        
        col1.metric(
            label=f'Italiana: {restaurante}',
            value=f'{avaliacao}/5.0',
            help=f"""
            País: {country}\n
            Cidade: {city}\n
            Média Prato para dois: {preco} ({moeda})
            """,
        )
        
   
    with col2:
        df_aux1 = df.loc[df['cuisines'] == 'American', :]
        df_aux2 = df_aux1.loc[:, ['restaurant_id', 'restaurant_name', 'aggregate_rating']].groupby(['restaurant_id', 'restaurant_name']).mean().reset_index().round(2)
        df_aux3 = df.loc[:, ['restaurant_id', 'country', 'city', 'average_cost_for_two', 'currency']]
        df_aux = pd.merge( df_aux2, df_aux3, how='inner' )
        df_aux = df_aux.sort_values('aggregate_rating', ascending = False).reset_index()
        restaurante = df_aux.loc[0, 'restaurant_name']
        avaliacao = df_aux.loc[0, 'aggregate_rating']
        country = df_aux.loc[0, 'country']
        city = df_aux.loc[0, 'city']
        preco = df_aux.loc[0, 'average_cost_for_two']
        moeda = df_aux.loc[0, 'currency']
        
        col2.metric(
            label=f'Americana: {restaurante}',
            value=f'{avaliacao}/5.0',
            help=f"""
            País: {country}\n
            Cidade: {city}\n
            Média Prato para dois: {preco} ({moeda})
            """,
        )
        
    with col3:
        df_aux1 = df.loc[df['cuisines'] == 'Arabian', :]
        df_aux2 = df_aux1.loc[:, ['restaurant_id', 'restaurant_name', 'aggregate_rating']].groupby(['restaurant_id', 'restaurant_name']).mean().reset_index().round(2)
        df_aux3 = df.loc[:, ['restaurant_id', 'country', 'city', 'average_cost_for_two', 'currency']]
        df_aux = pd.merge( df_aux2, df_aux3, how='inner' )
        df_aux = df_aux.sort_values('aggregate_rating', ascending = False).reset_index()
        restaurante = df_aux.loc[0, 'restaurant_name']
        avaliacao = df_aux.loc[0, 'aggregate_rating']
        country = df_aux.loc[0, 'country']
        city = df_aux.loc[0, 'city']
        preco = df_aux.loc[0, 'average_cost_for_two']
        moeda = df_aux.loc[0, 'currency']
        
        col3.metric(
            label=f'Árabe: {restaurante}',
            value=f'{avaliacao}/5.0',
            help=f"""
            País: {country}\n
            Cidade: {city}\n
            Média Prato para dois: {preco} ({moeda})
            """,
        )
        
    with col4:
        df_aux1 = df.loc[df['cuisines'] == 'Japanese', :]
        df_aux2 = df_aux1.loc[:, ['restaurant_id', 'restaurant_name', 'aggregate_rating']].groupby(['restaurant_id', 'restaurant_name']).mean().reset_index().round(2)
        df_aux3 = df.loc[:, ['restaurant_id', 'country', 'city', 'average_cost_for_two', 'currency']]
        df_aux = pd.merge( df_aux2, df_aux3, how='inner' )
        df_aux = df_aux.sort_values('aggregate_rating', ascending = False).reset_index()
        restaurante = df_aux.loc[0, 'restaurant_name']
        avaliacao = df_aux.loc[0, 'aggregate_rating']
        country = df_aux.loc[0, 'country']
        city = df_aux.loc[0, 'city']
        preco = df_aux.loc[0, 'average_cost_for_two']
        moeda = df_aux.loc[0, 'currency']
        
        col4.metric(
            label=f'Japonesa: {restaurante}',
            value=f'{avaliacao}/5.0',
            help=f"""
            País: {country}\n
            Cidade: {city}\n
            Média Prato para dois: {preco} ({moeda})
            """,
        )
        
    with col5:
        df_aux1 = df.loc[df['cuisines'] == 'Brazilian', :]
        df_aux2 = df_aux1.loc[:, ['restaurant_id', 'restaurant_name', 'aggregate_rating']].groupby(['restaurant_id', 'restaurant_name']).mean().reset_index().round(2)
        df_aux3 = df.loc[:, ['restaurant_id', 'country', 'city', 'average_cost_for_two', 'currency']]
        df_aux = pd.merge( df_aux2, df_aux3, how='inner' )
        df_aux = df_aux.sort_values('aggregate_rating', ascending = False).reset_index()
        restaurante = df_aux.loc[0, 'restaurant_name']
        avaliacao = df_aux.loc[0, 'aggregate_rating']
        country = df_aux.loc[0, 'country']
        city = df_aux.loc[0, 'city']
        preco = df_aux.loc[0, 'average_cost_for_two']
        moeda = df_aux.loc[0, 'currency']
        
        col5.metric(
            label=f'Brasileira: {restaurante}',
            value=f'{avaliacao}/5.0',
            help=f"""
            País: {country}\n
            Cidade: {city}\n
            Média Prato para dois: {preco} ({moeda})
            """,
        )
        
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
    }
    </style>
    """
    , unsafe_allow_html=True)


    


with st.container():
    st.markdown( """---""" )
    #st.title( "Localização Geográfica dos Restaurantes" )
    st.markdown(f"<h1 style = 'font-size: 30px; text-align: center'>Top {top_n} Restaurantes</h1>", unsafe_allow_html=True)
    df_aux1 = df1.loc[:, ['restaurant_id', 'restaurant_name', 'aggregate_rating']].groupby(['restaurant_id', 'restaurant_name']).mean().reset_index().round(2)
    df_aux2 = df1.loc[:, ['restaurant_id', 'country', 'city', 'cuisines', 'average_cost_for_two', 'currency', 'aggregate_rating', 'votes']]
    df_aux = pd.merge( df_aux1, df_aux2, how='inner' )
    df_aux = df_aux.sort_values('aggregate_rating', ascending = False).reset_index()
    
    st.markdown(
        """<style>
            .dataframe {text-align: center}
        </style>
        """, unsafe_allow_html=True)     
    
    st.dataframe(df_aux.head(top_n), use_container_width=True) 
    
with st.container():
    st.markdown( """---""" )
    st.markdown("<h1 style = 'font-size: 30px; text-align: center'>Melhores e Piores Tipos de Culinárias</h1>", unsafe_allow_html=True)
   
    col1, col2 = st.columns( 2 )
    with col1:
        st.markdown(f"<h1 style = 'font-size: 20px; text-align: center'>Top {top_n} Melhores Tipos de Culinárias</h1>", unsafe_allow_html=True)
        
        fig = px.bar(df.loc[:, ['aggregate_rating', 'cuisines']].groupby('cuisines').mean().round(2).sort_values("aggregate_rating", ascending=False).reset_index().head(top_n),
                     x='cuisines',
                     y='aggregate_rating',
                     text='aggregate_rating',
                     labels={
                         "cuisines": "Tipo de Culinária",
                         "aggregate_rating": "Média da Avaliação Média",
                     },
                    )
            
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.markdown(f"<h1 style = 'font-size: 20px; text-align: center'>Top {top_n} Piores Tipos de Culinárias</h1>", unsafe_allow_html=True)
        total = df.loc[:, ['aggregate_rating', 'cuisines']].groupby('cuisines').mean().round(2).sort_values("aggregate_rating", ascending=True).reset_index()        
        fig = px.bar(total.loc[(total['aggregate_rating'] > 0), ['aggregate_rating', 'cuisines']].head(top_n),
                     
                     x='cuisines',
                     y='aggregate_rating',
                     text='aggregate_rating',
                     labels={
                         "cuisines": "Tipo de Culinária",
                         "aggregate_rating": "Média da Avaliação Média",
                     },
                    )
            
        st.plotly_chart(fig, use_container_width=True)


