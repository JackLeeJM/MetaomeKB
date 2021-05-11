import streamlit as st
import time
from src.utils import seq_to_uniprot_id, pairwise_predict, homology_profile, result, protein_membership_profile


def baseIETemplate(uniprot_id1, uniprot_id2):

    prediction, score, profile, label, query_df = pairwise_predict(uniprot_id1, uniprot_id2)

    st.markdown("---")

    st.header("**Results**")

    st.markdown("######")

    st.subheader(f"Both Proteins are **{prediction}**")
    st.markdown("Explore the proteins' profile below for more details")
    # st.markdown(f"Both Proteins are **{prediction}**   \nThe Pairwise MetaSim Score is **{score}**")

    protein_label_1, protein_label_2 = label[0], label[1]
    protein_query_df_1, protein_query_df_2 = query_df[0], query_df[1]
    protein_id1, protein_name1, protein_gene_name1, protein_org1 = profile[0]
    protein_id2, protein_name2, protein_gene_name2, protein_org2 = profile[1]

    query_id1, query_name1, query_type1 = homology_profile(protein_label_1)
    query_id2, query_name2, query_type2 = homology_profile(protein_label_2)

    query_results_p1 = result(protein_query_df_1.columns.tolist())
    query_results_p2 = result(protein_query_df_2.columns.tolist())

    st.markdown("#")

    st.header('**Overview Profile of Protein 1**')

    protein_1_col1, protein_1_col2, protein_1_col3 = st.beta_columns([12,1,12])

    with protein_1_col1:

        st.subheader("**Protein Profile**")
        st.markdown(f"**UniProt ID**:    \n{protein_id1}   \n**Gene Name**:   \n{protein_gene_name1}   \n**Name**:   \n{protein_name1}   \n**Organism**:   \n{protein_org1}")

    with protein_1_col3:

        st.subheader("**Predicted Protein Homology Classification**")
        st.markdown(f"**InterPro ID**:   \n{query_id1}   \n**Name**:   \n{query_name1}   \n**Type**:   \n{query_type1}")

    # Protein Metadata Attribute Profile
    st.subheader("**Metadata Attributes**")
    st.markdown("Expand/Collapse the following accordions to view metadata relevant to the protein query")

    for i in query_results_p1:
        
        df_name1, df_result1 = i[0], i[1]

        with st.beta_expander(df_name1):
            st.plotly_chart(df_result1, use_container_width=True)

    st.markdown("####")

    st.subheader("**Protein Homology Membership**")

    st.markdown("Explore the protein members under the same homology group as the query protein.")

    st.markdown(f"**InterPro ID**: {query_id1}   \n**Name**:   {query_name1}")

    protein_members, protein_members_metadata = protein_membership_profile(query_id1, query_type1)

    with st.beta_expander("Members List"):
        st.table(protein_members) 

    with st.beta_expander("Members Metadata"):
        st.table(protein_members_metadata)

    st.markdown("#")

    st.markdown("###")

    st.header('**Overview Profile of Protein 2**')

    protein_2_col1, protein_2_col2, protein_2_col3 = st.beta_columns([12,1,12])

    with protein_2_col1:

        st.subheader("**Protein Profile**")
        st.markdown(f"**UniProt ID**:    \n{protein_id2}   \n**Gene Name**:   \n{protein_gene_name2}   \n**Name**:   \n{protein_name2}   \n**Organism**:   \n{protein_org2}")

    with protein_2_col3:

        st.subheader("**Predicted Protein Homology Classification**")
        st.markdown(f"**InterPro ID**:   \n{query_id2}   \n**Name**:   \n{query_name2}   \n**Type**:   \n{query_type2}")

    # Protein Metadata Attribute Profile
    st.subheader("**Metadata Attributes**")
    st.markdown("Expand/Collapse the following accordions to view metadata relevant to the protein query")

    for i in query_results_p2:
        
        df_name2, df_result2 = i[0], i[1]

        with st.beta_expander(df_name2):
            st.plotly_chart(df_result2, use_container_width=True)

    st.markdown("####")

    st.subheader("**Protein Homology Membership**")

    st.markdown("Explore the protein members under the same homology group as the query protein.")

    st.markdown(f"**InterPro ID**: {query_id2}   \n**Name**:   {query_name2}")

    protein_members, protein_members_metadata = protein_membership_profile(query_id2, query_type2)

    with st.beta_expander("Members List"):
        st.table(protein_members) 

    with st.beta_expander("Members Metadata"):
        st.table(protein_members_metadata)

    st.markdown("#")


def fastaIEModule():

    st.markdown("######")

    st.markdown("Your FASTA file should only contain **ONE** sequence")

    st.markdown("**Note** : Computation may take several minutes")

    col1, col2, col3 = st.beta_columns([12,1,12])

    with col1:
        st.subheader("**Protein 1**")
        uploaded_file1 = st.file_uploader("Choose a FASTA File", type="fasta", key=1)
    
    with col3:
        st.subheader("**Protein 2**")
        uploaded_file2 = st.file_uploader("Choose a FASTA File", type="fasta", key=2)
    
    if st.button("Predict"):

        if uploaded_file1 is not None and uploaded_file2 is not None:

            file_obj1 = uploaded_file1.getvalue()
            file_obj2 = uploaded_file2.getvalue()

            uniprot_id1 = seq_to_uniprot_id(file_obj1)
            time.sleep(2)
            uniprot_id2 = seq_to_uniprot_id(file_obj2)

            baseIETemplate(uniprot_id1, uniprot_id2)

        else:
            st.error("Please provide a pair of FASTA files.")


def seqIEModule():

    st.markdown("######")

    st.markdown("**Note** : Computation may take several minutes")

    col1, col2, col3 = st.beta_columns([12,1,12])

    with col1:
        st.subheader("**Protein 1**")
        sequence_text1 = st.text_area("Enter Sequence", height=250, key=1)
    
    with col3:
        st.subheader("**Protein 2**")
        sequence_text2 = st.text_area("Enter Sequence", height=250, key=2)
    
    if st.button("Predict"):

        if sequence_text1 is not None and sequence_text2 is not None:

            uniprot_id1 = seq_to_uniprot_id(sequence_text1)
            time.sleep(2)
            uniprot_id2 = seq_to_uniprot_id(sequence_text2)

            baseIETemplate(uniprot_id1, uniprot_id2)

        else:
            st.error("Please provide a pair of sequences.")


def uniprotIEModule():

    st.markdown('######')

    st.markdown("**Note** : Computation may take several minutes")

    col1, col2, col3 = st.beta_columns([12,1,12])

    with col1:
        st.subheader('**Protein 1**')
        uniprot_id1 = st.text_input('Enter UniProt ID', key=1)
    
    with col3:
        st.subheader('**Protein 2**')
        uniprot_id2 = st.text_input('Enter UniProt ID', key=2)
    
    if st.button("Predict"):
        
        if uniprot_id1 is not None and uniprot_id2 is not None:

            baseIETemplate(uniprot_id1, uniprot_id2)

        else:
            st.error("Please provide a pair of IDs.")