import pandas as pd
import os

def ensembl_to_hugo(ensembl_list):
    df = pd.read_csv(os.path.join(os.path.dirname(__file__), 'data.csv'))
    df = df[df['ENSEMBL_ID'].isin(ensembl_list)].reset_index()
    df = df.drop('index', axis=1)
    return df

def hugo_to_ensembl(hugo_list):
    df = pd.read_csv(os.path.join(os.path.dirname(__file__), 'data.csv'))
    df = df[df['HGNC_ID'].isin(hugo_list)].reset_index()
    df = df.drop('index', axis=1)
    return df
