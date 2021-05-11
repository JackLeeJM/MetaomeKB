import streamlit as st
from PIL import Image

def homePage():

    sq_path = './assets/image/Single_Query.png'
    pq_path = './assets/image/Pairwise_Query.png'

    single_query_img = Image.open(sq_path)
    pairwise_query_img = Image.open(pq_path)

    st.markdown("""
    <style>
    .big-font {
        font-size:20px !important;
    }
    </style>
    """, unsafe_allow_html=True)

    search_engine_desc = '''
                         Query a protein sequence against the Meta-ome database to find similar 
                         proteins in the query’s homologous group label, be it of family or superfamily level.
                         '''
    
    inference_engine_desc = '''
                         Query TWO proteins against the Meta-ome database and compute the similarity between them to determine homology,
                         either both was predicted to be Homologous or Non-Homologous.
                         '''

    with st.beta_expander("Search Engine"):
        st.markdown("###")
        st.markdown(f'<p class="big-font"><b>{search_engine_desc}</b></p>', unsafe_allow_html=True)
        st.markdown("###")
        st.image(single_query_img)

        st.markdown("###")

    st.markdown("#")

    with st.beta_expander("Inference Engine"):
        st.markdown("###")
        st.markdown(f'<p class="big-font"><b>{inference_engine_desc}</b></p>', unsafe_allow_html=True)
        st.markdown("###")
        st.image(pairwise_query_img)

        st.markdown("###")