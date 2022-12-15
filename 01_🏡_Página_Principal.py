import streamlit as st
import pandas as pd
from PIL import Image


st.set_page_config( 
    page_title="Página Principal",
    page_icon="📊"
)


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
    
    st.write("<h1 style='text-align: center; color: red; line-height:0em'>Fome Zero</h1><h2 style='text-align: center; color: black;'>O Melhor lugar para encontrar seu mais novo restaurante favorito!</h2>", unsafe_allow_html=True)
    
    st.image('logo.png' )
    

    st.markdown( """---""" )
    st.markdown("<h6 style='text-align: center; color: black;'>Desenvolvido por:</h6>", unsafe_allow_html=True)
    st.image('cds.png', width=180 )
    st.write("<h6 style='text-align: center; color: black;'>Time de Data Science no Discord:<br>@Fabio Rodrigues Pinho#6975</h6>", unsafe_allow_html=True)
    
    


st.markdown("<h1 style = 'font-size: 50px; text-align: center'>Fome Zero Statistics Dashboard</h1>", unsafe_allow_html=True)
st.markdown("<h6 style = 'text-align: justify'>A empresa Fome Zero é uma marketplace de restaurantes. Ou seja, seu core business é facilitar o encontro e negociações de clientes e restaurantes. Os restaurantes fazem o cadastro dentro da plataforma da Fome Zero, que disponibiliza informações como endereço, tipo de culinária servida, se possui reservas, se faz entregas e também uma nota de avaliação dos serviços e produtos do restaurante, dentre outras informações.<br><br>O presente 'Statistics Dashboard' foi construído para acompanhar os cadastros e as avaliações dos restaurantes.</h6>", unsafe_allow_html=True)

            
st.markdown(
    """

    ### Como utilizar este 'Statistics Dashboard'?
    - Visão Geral:
        - Resumo dos restaurantes cadastrados na plataforma por localização geográfica e por culinária.
    - Visão por País:
        - Quantidade de restaurantes registrados, média de avaliações e média de preços de pratos por país.
    - Visão por Cidades:
        - Cidades com mais restaurantes cadastrados, cidades com restaurantes mais bem avaliados e cidades com maior diversidade de culinária.
    - Visão por Culinária:
        - Melhores restaurantes por tipo de culinária.
    ### Como obter ajuda:
    - Time de Data Science no Discord
        - @Fabio Rodrigues Pinho#6975
""" )

st.markdown("### Dados Tratados:")
processed_data = pd.read_csv("data.csv")

st.download_button(
    label="Download",
    data=processed_data.to_csv(index=False),
    file_name="dados_fabio.csv",
    mime="text/csv",
)
    

