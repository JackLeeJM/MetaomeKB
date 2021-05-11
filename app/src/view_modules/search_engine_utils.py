import streamlit as st
from src.utils import seq_to_uniprot_id, predict, homology_profile, result, protein_membership_profile


def baseSETemplate(uniprot_id):

    prediction = predict(uniprot_id)

    st.markdown("---")

    st.header("**Results**")

    st.markdown("######")

    profile_col1, profile_col2, profile_col3 = st.beta_columns([12,1,12])

    with profile_col1:

        # Protein Profile
        protein_id, protein_name, protein_gene_name, protein_org = prediction[2]
        
        st.subheader("**Protein Profile**")

        st.markdown(f"**UniProt ID**:    \n{protein_id}   \n**Gene Name**:   \n{protein_gene_name}   \n**Name**:   \n{protein_name}   \n**Organism**:   \n{protein_org}")

        st.markdown("###")

    with profile_col3:

        # Query Homology Profile

        query_id, query_name, query_type = homology_profile(prediction[0])
        
        st.subheader("**Predicted Protein Homology Classification**")

        st.markdown(f"**InterPro ID**:   \n{query_id}   \n**Name**:   \n{query_name}   \n**Type**:   \n{query_type}")

        st.markdown("###")

    query_reference = prediction[1].columns.tolist()
    query_results = result(query_reference)

    # Protein Metadata Attribute Profile
    st.subheader("**Protein Metadata Attributes**")

    st.markdown("Expand/Collapse the following accordions to view metadata relevant to the protein query")

    for i in query_results:
        
        df_name, df_result = i[0], i[1]

        with st.beta_expander(df_name):
            st.plotly_chart(df_result, use_container_width=True)

    st.markdown("#")

    st.subheader("**Protein Homology Membership**")

    st.markdown("Explore the protein members under the same homology group as the query protein.")

    # st.markdown("###")

    st.markdown(f"**InterPro ID**: {query_id}   \n**Name**:   {query_name}")

    protein_members, protein_members_metadata = protein_membership_profile(query_id, query_type)

    with st.beta_expander("Members List"):
        st.table(protein_members) 

    with st.beta_expander("Members Metadata"):
        st.table(protein_members_metadata)



def fastaSEModule():

    col1, col2 = st.beta_columns(2)

    with col1:

        st.markdown("######")

        st.markdown("Your FASTA file should only contain **ONE** sequence")

        st.markdown("**Note** : Computation may take several minutes")

        uploaded_file = st.file_uploader("Choose a FASTA File", type="fasta")
    
    if st.button("Predict"):

        if uploaded_file is not None:

            file_obj = uploaded_file.getvalue()

            uniprot_id = seq_to_uniprot_id(file_obj)

            baseSETemplate(uniprot_id)

        else:
            st.error("Please provide a FASTA file.")


def seqSEModule():

    st.markdown("######")

    st.markdown("**Note** : Computation may take several minutes")
    
    sequence_text = st.text_area("Enter Sequence", "Type Here", height=250)
    
    if st.button("Predict"):

        if sequence_text is not None:

            uniprot_id = seq_to_uniprot_id(sequence_text)

            baseSETemplate(uniprot_id)

        else:
            st.error("Please provide a sequence.")


def uniprotSEModule():

    st.markdown('######')

    st.markdown("**Note** : Computation may take several minutes")

    col1, col2 = st.beta_columns(2)

    with col1:

        uniprot_id = st.text_input('UniProt ID')
    
    if st.button("Predict"):

        if uniprot_id is not None:

            baseSETemplate(uniprot_id)

        else:
            st.error("Please provide an ID.")