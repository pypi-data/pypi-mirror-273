
from pysam import VariantFile
import requests
import pandas as pd
import re
from Bio.SeqUtils import seq1
import numpy as np


def affipred_pred(input_file, output_file="output.csv"):

    f2 = VariantFile(input_file)

    ref = []
    alt = []
    pos = []
    chr = []
    for rec in f2.fetch():
        if rec.alts != None:
            ref.append(rec.ref)
            alt.append(rec.alts[0])
            pos.append(rec.pos)
            chr.append(rec.chrom)
        chr1 = [re.sub('chr', '', i) for i in chr]
        df = pd.DataFrame({'chr':chr1, 'pos':pos, 'ref':ref, 'alt':alt})

    conc_df = df.astype(str).apply(lambda row: ' '.join(row), axis=1).tolist()

    api_url = "https://www.ebi.ac.uk/ProtVar/api/mappings"
    params = {"function":"false", "population":"false", "structure":"false", "assembly":"AUTO"}
    #todo = ["19 1010539 G C", "P80404 Gln56Arg", "rs1042779"]
    dfx = conc_df
    response = requests.post(api_url, json=dfx, params=params)
    out = response.json()

    df = pd.DataFrame({
        'input_str': [None] * len(dfx),
        'uniprot': [None] * len(dfx),
        'position': [None] * len(dfx),
        'native': [None] * len(dfx),
        'mutant': [None] * len(dfx)
    })

    for i in range(len(dfx)):
        try:
            if len(out['inputs'][i]['mappings']) > 0 and len(out['inputs'][i]['mappings'][0]['genes']) > 0:
                input_str = out['inputs'][i]['inputStr']
                uniprot = out['inputs'][i]['mappings'][0]['genes'][0]['isoforms'][0]['canonicalAccession']
                position = out['inputs'][i]['mappings'][0]['genes'][0]['isoforms'][0]['isoformPosition']
                native = out['inputs'][i]['mappings'][0]['genes'][0]['isoforms'][0]['refAA']
                mutant = out['inputs'][i]['mappings'][0]['genes'][0]['isoforms'][0]['variantAA']
                
                if all([input_str, uniprot, position, native, mutant]):
                    df.loc[i] = [input_str, uniprot, position, native, mutant]
                else:
                    continue
                    
        except:
            pass

    df = df.dropna()

    aa_lst1 = df['native'].tolist()
    aa_lst2 = df['mutant'].tolist()

    a_list1 = [seq1(aa) for aa in aa_lst1]
    a_list2 = [seq1(aa) for aa in aa_lst2]

    df['native'] = a_list1
    df['mutant'] = a_list2

    df = df[['input_str','uniprot', 'native', 'position', 'mutant']]
    df1 = df[['uniprot', 'native', 'position', 'mutant']]

    response.status_code

    # Query database
    mut_vals = df['mutant'].unique()
    mut_vals = mut_vals[mut_vals != "*"]
    ind = 0
    dfs = []
    for i in mut_vals:
        dfx = df1[df1['mutant'] == i]
        tbl = "variants_" + i
        query_list = df1.astype(str).apply(lambda row: '_'.join(row), axis=1).tolist()
        queries = ','.join(query_list)
        api_url = "https://affipred.timucinlab.com/api/" + tbl + "/" + queries
        response = requests.get(api_url)
        data = response.json()
        results = pd.DataFrame(data)
        results = results.iloc[:, [2, 7, 6] + list(range(8, 19)) + list(range(23, 25))]
        dfs.append(results)

        ind = ind + 1

    final_response = pd.concat(dfs, ignore_index=True)
    colnames = ['uniprot_id','position','native_aa','mutant_aa','GO_number','plddt','plddt_mean','ASA','wt_psic','mt_psic',
                'dpsic','BLOSUM62','kdHydrophobicity_DELTAmn','Volume_(A3)_n','AFFIPred_score','AFFIPred_SD']

    final_response.columns = colnames
    final_response['AFFIPred_Result'] = final_response['AFFIPred_score'].apply(lambda x: "Pathogenic" if x >= 0.5 else "Benign")

    final_response.to_csv(output_file, index=False)

# print(final_response)