import pandas as pd

def ensembl_to_hugo(ensembl_list):
    df = pd.read_csv('pygeneconverter/data/query_table.csv')
    df = df[df['ENSEMBL_ID'].isin(ensembl_list)]
    return df

def hugo_to_ensembl(hugo_list):
    df = pd.read_csv('pygeneconverter/data/query_table.csv')
    df = df[df['HGNC_ID'].isin(hugo_list)]
    return df
