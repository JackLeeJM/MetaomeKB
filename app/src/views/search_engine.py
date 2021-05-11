import streamlit as st
from src.view_modules.search_engine_utils import fastaSEModule, seqSEModule, uniprotSEModule

def searchEngine():

    st.header("**Single Query**")

    st.markdown("######")

    options = ('FASTA', 'Sequence', 'UniProt ID')
    status = st.radio("Preferred Input", options)

    if status == "FASTA":

        fastaSEModule()

    if status == "Sequence":

        seqSEModule()

    if status == "UniProt ID":

        uniprotSEModule()

    st.markdown("###")