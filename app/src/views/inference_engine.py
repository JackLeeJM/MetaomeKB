import streamlit as st
from src.view_modules.inference_engine_utils import fastaIEModule, seqIEModule, uniprotIEModule

def inferenceEngine():

    st.header("**Pairwise Query**")

    st.markdown("######")

    options = ('FASTA', 'Sequence', 'UniProt ID')
    status = st.radio("Preferred Input", options)

    if status == "FASTA":

        fastaIEModule()

    if status == "Sequence":

        seqIEModule()

    if status == "UniProt ID":

        uniprotIEModule()

    st.markdown("###")