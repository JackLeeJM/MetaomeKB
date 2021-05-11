import streamlit as st
import src
from src.views.home import homePage
from src.views.about import aboutPage
from src.views.search_engine import searchEngine
from src.views.inference_engine import inferenceEngine

def main():

    st.set_page_config(initial_sidebar_state="expanded", layout="wide")

    st.title("MetaomeKB")

    st.markdown("""
        <style>
        .big-font {
            font-size:20px !important;
        }
        </style>
    """, unsafe_allow_html=True)

    st.header("Meta-ome for Homology Search")

    description =   '''
                    An AI-powered protein homology classifier that is built to assist researchers in collecting and 
                    analysing relevant metadata across multi-omics databases to conduct their experiments
                    '''

    st.markdown(f'<p class="big-font">{description}</p>', unsafe_allow_html=True)
    # st.markdown(description)

    st.markdown("---")

    menu = ['Home', 'Search Engine', 'Inference Engine']
    st.sidebar.title("Menu")
    choice = st.sidebar.selectbox("Selection", menu)

    if choice == "Home":

        homePage()

    # if choice == 'About':

    #     aboutPage()

    if choice == "Search Engine":

        searchEngine()

    if choice == "Inference Engine":

        inferenceEngine()

if __name__ == '__main__':
	main()