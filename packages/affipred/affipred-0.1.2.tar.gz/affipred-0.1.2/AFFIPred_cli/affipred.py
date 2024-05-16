
from pysam import VariantFile
import requests
import pandas as pd
import re
from Bio.SeqUtils import seq1
import numpy as np
from tqdm import tqdm

def get_total_records(input_file):
        total_records = 0

        with VariantFile(input_file) as vcf_file:
            for _ in vcf_file:
                total_records += 1

        return total_records

def affipred(input_file, output_file="output.csv", type = "VCF"):

    f2 = VariantFile(input_file)

    total_variants = get_total_records(input_file)

    vcf_data = []
    progress_bar = tqdm(total=total_variants, desc='Reading the vcf file', position=0, leave=True)
    for rec in f2.fetch():
        if rec.alts != None:
            vcf_data.append({
                'chr': rec.chrom,
                'pos': rec.pos,
                'ref': rec.ref,
                'alt': rec.alts[0]
            })
            progress_bar.update(1)
    progress_bar.close()
    data = pd.DataFrame(vcf_data)
    data['chr'] = data['chr'].str.replace('chr', '')

    conc_df = data.astype(str).apply(lambda row: ' '.join(row), axis=1).tolist()

    api_url = "https://www.ebi.ac.uk/ProtVar/api/mappings"
    params = {"function":"false", "population":"false", "structure":"false", "assembly":"AUTO"}
    #todo = ["19 1010539 G C", "P80404 Gln56Arg", "rs1042779"]
    dfx = conc_df

    num = 1  # Start from index 1
    num2 = len(dfx)
    numx = 9300
    numy = num2 // numx

    df = pd.DataFrame({
        'input_str': [None] * len(dfx),
        'uniprot': [None] * len(dfx),
        'position': [None] * len(dfx),
        'native': [None] * len(dfx),
        'mutant': [None] * len(dfx)
    })

    print(" ")

    progress_bar = tqdm(total=num2, desc='Converting genomic positions to amino acid positions', position=0, leave=True)
    for j in range(1, numy + 2):
        dfx1 = dfx[num - 1:numx * j - 1]
        dfx1 = [value for value in dfx1 if value is not None]

        response = requests.post(api_url, json=dfx1, params=params)
        out = response.json()

        df2 = pd.DataFrame({
            'input_str': [None] * len(dfx1),
            'uniprot': [None] * len(dfx1),
            'position': [None] * len(dfx1),
            'native': [None] * len(dfx1),
            'mutant': [None] * len(dfx1)
        })

        for i in range(len(dfx1)):
            try:
                if len(out['inputs'][i]['mappings']) > 0 and len(out['inputs'][i]['mappings'][0]['genes']) > 0:
                    input_str = out['inputs'][i]['inputStr']
                    uniprot = out['inputs'][i]['mappings'][0]['genes'][0]['isoforms'][0]['canonicalAccession']
                    position = out['inputs'][i]['mappings'][0]['genes'][0]['isoforms'][0]['isoformPosition']
                    native = out['inputs'][i]['mappings'][0]['genes'][0]['isoforms'][0]['refAA']
                    mutant = out['inputs'][i]['mappings'][0]['genes'][0]['isoforms'][0]['variantAA']
                    
                    if all([input_str, uniprot, position, native, mutant]):
                        df2.loc[i] = [input_str, uniprot, position, native, mutant]
                    else:
                        continue
                        
            except:
                pass
            progress_bar.update(1)

        df = pd.concat([df, df2])
        num = (numx * j) + 1

    progress_bar.close()

    dfa = df.dropna()

    aa_lst1 = dfa['native'].tolist()
    aa_lst2 = dfa['mutant'].tolist()

    a_list1 = [seq1(aa) for aa in aa_lst1]
    a_list2 = [seq1(aa) for aa in aa_lst2]

    dfa.loc[:, 'native'] = a_list1
    dfa.loc[:, 'mutant'] = a_list2

    dfa = dfa[['input_str','uniprot', 'native', 'position', 'mutant']]
    df1 = dfa[['uniprot', 'native', 'position', 'mutant']]

    response.status_code

    print(" ")
    # Query database
    mut_vals = dfa['mutant'].unique()
    mut_vals = mut_vals[mut_vals != "*"]
    ind = 0

    num = 1  # Start from index 1
    num2 = len(df1)
    numx = 5000
    numy = num2 // numx

    #df2 = df1.head(5000)
    dfs = []
    progress_bar = tqdm(total=numy+1, desc='Querying the database', position=0, leave=True)
    for j in range(1, numy + 2):
        # print(j)
        df2 = df1.iloc[num - 1:numx * j - 1]
        for i in mut_vals:
            # print(i)
            
            dfx = df2[df2['mutant'] == i]
            tbl = "variants_" + i
            query_list = dfx.astype(str).apply(lambda row: '_'.join(row), axis=1).tolist()
            queries = ','.join(query_list)
            api_url = "https://affipred.timucinlab.com/api/" + tbl + "/" + queries
            response = requests.get(api_url)
            data = response.json()
            results = pd.DataFrame(data)
            if not results.empty:
                results = results.iloc[:, [2, 7, 6] + list(range(8, 19)) + list(range(23, 25))]
                dfs.append(results)

            ind = ind + 1
        num = (numx * j) + 1
        progress_bar.update(1)

    progress_bar.close()

    final_response = pd.concat(dfs, ignore_index=True)
    colnames = ['uniprot_id','position','native_aa','mutant_aa','GO_number','plddt','plddt_mean','ASA','wt_psic','mt_psic',
                'dpsic','BLOSUM62','kdHydrophobicity_DELTAmn','Volume_(A3)_n','AFFIPred_score','AFFIPred_SD']

    final_response.columns = colnames
    final_response['AFFIPred_Result'] = final_response['AFFIPred_score'].apply(lambda x: "Pathogenic" if x >= 0.5 else "Benign")

    final_response.to_csv(output_file, index=False)

# print(final_response)