import plotly.graph_objects as go

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