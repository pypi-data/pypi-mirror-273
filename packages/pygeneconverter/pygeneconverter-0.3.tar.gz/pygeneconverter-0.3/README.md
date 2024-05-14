The pygeneconverter package provides functions for converting Ensembl IDs to HUGO gene symbols and vice versa. It also provides corresponsing gene types, i.e, lincRNA, miRNA etc. It is designed for use in bioinformatics and computational biology applications.

### Installation:

```bash
pip install pygeneconverter
```

### Example usage:

```python
from pygeneconverter import ensembl_to_hugo, hugo_to_ensembl

ensembl_list = ['ENSG00000223972', 'ENSG00000237613', 'ENSG00000268020']
hugo_list = ['DDX11L1', 'FAM138A', 'OR4G4P']

ensembl_df = ensembl_to_hugo(ensembl_list)
hugo_df = hugo_to_ensembl(hugo_list)
```
This will output a dataframe with three columns: ENSEMBL_ID, GENE_TYPE, and HGNC_ID.

### LICENSE
No License. Use wherever you want to use.
