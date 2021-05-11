import json
import time
import streamlit as st
import bioservices
import xmltodict
import pandas as pd
import scipy
import tensorflow as tf
import pickle
import plotly.graph_objects as go
from Bio import SeqIO
from bioservices import NCBIblast


def load_data():
    encoder_path = "./assets/reference/encoder"
    ref_path = "./assets/reference/reference_df.pkl"
    # model_path = "./assets/model/multiclass_fam_sfam_32k_model.h5"
    model_architecture_path = "./assets/model/model_architecture.json"
    model_weights_path = "./assets/model/model_weights.h5"
    ref_database_path = "./assets/reference/reference_database.json"
    uniprot_database_path = "./assets/reference/uniprot_database_df_18-3-21.pkl"
    family_interpro_path = "./assets/reference/interpro_fam_count_df.pkl"
    superfamily_interpro_path = "./assets/reference/interpro_sfam_count_df.pkl"

    ref = pd.read_pickle(ref_path)
    refList = list(ref.columns)
    # model = tf.keras.models.load_model(model_path)
    uniprot_db = pd.read_pickle(uniprot_database_path)
    fam_df = pd.read_pickle(family_interpro_path)
    sfam_df = pd.read_pickle(superfamily_interpro_path)

    with open(encoder_path, "rb") as f, open(model_architecture_path, 'r') as g: 
        encoder = pickle.load(f) 
        model_config = g.read() 

    model = tf.keras.models.model_from_json(model_config)
    model.load_weights(model_weights_path)

    with open(ref_database_path) as f:
        ref_database = json.load(f)

    return ref, refList, model, encoder, ref_database, uniprot_db, fam_df, sfam_df

ref, refList, model, encoder, ref_database, uniprot_db, fam_df, sfam_df = load_data()

def fasta_to_plain_seq(fasta_file):
    record = SeqIO.read(fasta_file, format="fasta")
    record_seq = record.seq

    return str(record_seq)

def seq_to_uniprot_id(seq):
    s = NCBIblast(verbose=False)
    jobid = s.run(program="blastp", sequence=seq, stype="protein", database="uniprotkb_swissprot", email="test@yahoo.com")
    xml_result = s.get_result(jobid, "xml")
    json_dict = xmltodict.parse(xml_result)
    protein_id = json_dict['EBIApplicationResult']['SequenceSimilaritySearchResult']['hits']['hit'][0]['@ac']

    return protein_id

def retrieve(uniprot_id):
    
    def protein_profile(protein_df):
        protein_id = protein_df.ID.values[0]
        protein_name = protein_df.Protein_Name.values[0]
        protein_gene_name = protein_df.Gene_Name.values[0]
        protein_organism = protein_df.Organism.values[0]

        return protein_id, protein_name, protein_gene_name, protein_organism

    def protein_db_reference(protein_metadata):
        entry = protein_metadata

        # Checking for extra elements in query's reference compared to reference template
        extra = [i for i in entry if i not in refList]
        if len(extra) != 0:
            for ext in extra:
                entry.remove(ext)
            dict_ = {i:1 for i in entry}
            df = pd.DataFrame.from_dict(dict_, orient="index").T
        else:
            dict_ = {i:1 for i in entry}
            df = pd.DataFrame.from_dict(dict_, orient="index").T

        return df

    protein_df = uniprot_db[uniprot_db.ID == uniprot_id]
    protein_query_profile = protein_profile(protein_df)
    protein_metadata = protein_df.Metadata.values[0]
    query_df = protein_db_reference(protein_metadata)

    reference = ref.append(query_df, sort=False, ignore_index=True).fillna(0).tail(1).values

    # return reference, query_df, protein_profile
    return reference, query_df, protein_query_profile

def predict(uniprot_id):

    query = retrieve(uniprot_id)
    query_df = query[1]
    profile = query[2]
    model_prediction = model.predict(query[0])
    query_label = encoder.inverse_transform(model_prediction)
    string_label = str(query_label[0][0])

    return string_label, query_df, profile

def pairwise_predict(uniprot_id1, uniprot_id2):
    
    # Predictions comprising 2 results, [0] = Prediction Label ; [1] = Query's DF for calculating scores
    protein_1_prediction = predict(uniprot_id1)
    protein_2_prediction = predict(uniprot_id2)

    # Profiles
    profiles = protein_1_prediction[2], protein_2_prediction[2]

    protein_query_df = protein_1_prediction[1], protein_2_prediction[1]
    
    prediction_label = protein_1_prediction[0], protein_2_prediction[0]

    # Calculating similarity score for both protein using Jaccard Distance metric
    dual_reference_df = protein_1_prediction[1].append(protein_2_prediction[1], sort=False, ignore_index=True).fillna(0).astype(int)
    arr1, arr2 = dual_reference_df.iloc[:1], dual_reference_df.iloc[1:]
    MetaSim_score = scipy.spatial.distance.cdist(arr1, arr2, metric='jaccard')[0][0]

    if protein_1_prediction[0] == protein_2_prediction[0]:  
        verdict = "Homologous"
        score = f"{MetaSim_score:.5f}"
        return verdict, score, profiles, prediction_label, protein_query_df
        
    else:
        verdict = "Non-Homologous"
        score = f"{MetaSim_score:.5f}"
        return verdict, score, profiles, prediction_label, protein_query_df

def homology_profile(string_label):

    def homology_index(string_label):
        for k,v in ref_database['InterPro'].items():
            for k1,v1 in v.items():
                if v1 == string_label:
                    return k

    index = homology_index(string_label)
    id_ = ref_database['InterPro'][index]['ID']
    name_ = ref_database['InterPro'][index]['Name']
    type_ = ref_database['InterPro'][index]['Type']

    return id_, name_, type_

def df_to_plotly_conversion(df_tuple):
    df_name = df_tuple[0]
    df_result = df_tuple[1]

    def plot_config(df):
        height_constant = (33 * len(df.ID)) + 33
        margin_constant = dict(r=0, l=0, t=5, b=0)
        
        return height_constant, margin_constant

    def go_table(df):
    
        df = df[['ID', 'Ontology' , 'Name', 'Definition']]

        height_constant, margin_constant = plot_config(df)

        fig = go.Figure(data=[go.Table(
            columnorder = [1,2,3,4],
            columnwidth = [65, 90, 110, 400],
            header=dict(
                        values=[['<b>ID</b>'],['<b>Ontology</b>'],['<b>Name</b>'],['<b>Definition</b>']],
                        font_size = 13,
                        align='center'),
            cells=dict(values=[df.ID, df.Ontology, df.Name, df.Definition],
                    font_size = 12,
                    align='left',
                    height=27))
        ])
        fig.update_layout(height=height_constant, margin=margin_constant)
        return fig

    def interpro_table(df):
        
        height_constant, margin_constant = plot_config(df)

        fig = go.Figure(data=[go.Table(
            columnorder = [1,2,3],
            columnwidth = [25, 25, 100],
            header=dict(
                        values=[['<b>ID</b>'],['<b>Type</b>'],['<b>Name</b>']],
                        font_size = 13,
                        align='center'),
            cells=dict(values=[df.ID, df.Type, df.Name],
                    font_size = 12,
                    align='left',
                    height=27))
        ])
        # fig.update_layout(autosize=True, margin=margin_constant)
        fig.update_layout(height=height_constant, margin=margin_constant)
        return fig

    def reactome_table(df):

        height_constant, margin_constant = plot_config(df)
        
        fig = go.Figure(data=[go.Table(
            columnorder = [1,2],
            columnwidth = [50,100],
            header=dict(
                        values=[['<b>ID</b>'],['<b>Name</b>']],
                        font_size = 13,
                        align='center'),
            cells=dict(values=[df.ID, df.Name],
                    font_size = 12,
                    align='left',
                    height=27))
        ])
        fig.update_layout(height=height_constant, margin=margin_constant)
        return fig

    def omim_table(df):

        height_constant, margin_constant = plot_config(df)

        fig = go.Figure(data=[go.Table(
            columnorder = [1,2],
            columnwidth = [50,100],
            header=dict(
                        values=[['<b>ID</b>'],['<b>Name</b>']],
                        font_size = 13,
                        align='center'),
            cells=dict(values=[df.ID, df.Name],
                    font_size = 12,
                    align='left',
                    height=27))
        ])
        fig.update_layout(height=height_constant, margin=margin_constant)
        return fig

    case_switch={
        'GO':go_table,
        'InterPro':interpro_table,
        'Reactome': reactome_table,
        'Omim': omim_table
        }

    plotly_df = case_switch[df_name](df_result)

    return (df_name, plotly_df)

def result(query_ref):
    db_ref_tuple_iter = [ ('GO', [], []), ('InterPro', [], []), ('Reactome', [], []), ('Omim', [], []) ]
    non_empty_results = []
    non_empty_results_plotly = []

    for i in db_ref_tuple_iter:

        reference_db_name = i[0]
        reference_db_list = i[1]
        reference_results = i[2]

        for k,v in ref_database[reference_db_name].items():
            for k1,v1 in v.items():
                if v1 in query_ref:
                    reference_db_list.append(k)

        for j in reference_db_list:
            reference_results.append(ref_database[reference_db_name][j])

        if len(reference_db_list) != 0:
            results_df = pd.DataFrame(reference_results)
            non_empty_results.append((reference_db_name, results_df))

    for i in non_empty_results:
        converted_df = df_to_plotly_conversion(i)
        non_empty_results_plotly.append(converted_df)

    # return non_empty_results
    return non_empty_results_plotly

def protein_membership_profile(homology_label, homology_type):
    
    def protein_members(homology_label, homology_type):

        homology_group_df_dict = {'Family': fam_df,
                                  'Homologous_superfamily': sfam_df}

        selected_df = homology_group_df_dict[homology_type]
        query_selection = selected_df[selected_df.accession == homology_label]
        query_homologs_acc = query_selection.protein.values[0]
        query_metaome_selection = uniprot_db[uniprot_db.ID.isin(query_homologs_acc)].drop(['Status', 'Annotation'], axis=1)

        protein_profile_df = query_metaome_selection[['ID', 'Protein_Name', 'Gene_Name']].reset_index(drop=True)
        protein_profile_df.Gene_Name.replace('[]', '-', inplace=True)
        protein_profile_df = protein_profile_df[['ID', 'Gene_Name', 'Protein_Name']]

        # Query's metadata profile
        query_metadata_profile = query_metaome_selection[['ID', 'Metadata']]
        query_metadata_profile = query_metadata_profile.reset_index(drop=True)

        pd.set_option('colheader_justify', 'center')

        def protein_profile_table(df):
    
            df = df[['ID', 'Gene_Name' , 'Protein_Name']]

            height_constant = (33 * len(df.ID)) + 33
            margin_constant = dict(r=0, l=0, t=5, b=0)

            fig = go.Figure(data=[go.Table(
                columnorder = [1,2,3],
                columnwidth = [25,25,100],
                header=dict(
                            values=[['<b>ID</b>'],['<b>Gene_Name</b>'],['<b>Protein_Name</b>']],
                            font_size = 13,
                            align='center'),
                cells=dict(values=[df.ID, df.Gene_Name, df.Protein_Name],
                        font_size = 12,
                        align='left',
                        height=27))
            ])
            fig.update_layout(height=height_constant, margin=margin_constant)

            return fig

        query_members_table = protein_profile_table(protein_profile_df)
        
        return protein_profile_df, query_metadata_profile

    homology_group_profile = protein_members(homology_label, homology_type)

    return homology_group_profile