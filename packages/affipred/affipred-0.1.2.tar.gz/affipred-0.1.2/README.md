# AFFIPred: AlphaFold based Functional Impact Prediction of Missense Variations

## Usage:
First, install the tool using pip.
```
pip install affipred
```

Provide input and output files with relative or absolute path:
```
affipred variants.vcf -o affipred_results.csv
```
The input should be a `.vcf` file while the output file name extension should be `.csv`. 

The output file will contain all the features used to predict the impact of the variants alongside the AFFIPred scores and the prediction of functional impact of the variants.