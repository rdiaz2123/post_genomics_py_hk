#Ricardo Diaz 
#Post Genomics 
#HW6 

#Part 1 Data Manipulation

#Using the Normal and Tumor CSV files from Homework 3. Subset the two CSV files with only 
#the columns, ["chrom", "left", "ref_seq", "alt_seq", “Patient_ID”, ‘VCF_ID”]

import os
import numpy as np 
import pandas as pd

#get the needed csv files from hk3 and get them 
hk3_normal_csv = pd.read_csv("C:/Users/Ricardo/Desktop/Output_Final_Normal_and_Tumor/Final_Normal.csv")
hk3_tumor_csv = pd.read_csv("C:/Users/Ricardo/Desktop/Output_Final_Normal_and_Tumor/Final_Tumor.csv")

#I will also strip any spaces in these csvs 
hk3_normal_csv.columns = hk3_normal_csv.columns.str.strip()
hk3_tumor_csv.columns  = hk3_tumor_csv.columns.str.strip()

#the targeted cols are: 
target_col = ["chrom", "left", "ref_seq", "alt_seq", "Patient_ID", "VCF_ID"]

#function to get the cols for specific question 
def subset_col(df, cols):
    cols_new = [i for i in cols if i in df.columns]
    return df[cols_new].copy()

normal_subset = subset_col(hk3_normal_csv, target_col)
tumor_subset = subset_col(hk3_tumor_csv, target_col)

print(normal_subset)
print(tumor_subset)

#just create csv to check I get the right cols
output_folder = "C:/Users/Ricardo/Desktop/Output_Final_Normal_and_Tumor"
normal_subset_path = os.path.join(output_folder, "Subset_Normal.csv")
tumor_subset_path  = os.path.join(output_folder, "Subset_Tumor.csv")

normal_subset.to_csv(normal_subset_path, index=False)
tumor_subset.to_csv(tumor_subset_path, index=False)

#how many unique normal and tumor patients do we have
normal_unique_patients = normal_subset["Patient_ID"].nunique()
tumor_unique_patients = tumor_subset["Patient_ID"].nunique()

print("Unique normal patients: ", normal_unique_patients)
print("Unique tumor patients: ", tumor_unique_patients)

#group by variant info,chrom, left, ref_seq, and alt_seq, let the other columns turn into 

variant_cols = ["chrom", "left", "ref_seq", "alt_seq"]

def variant_info(df):
    return df.groupby(variant_cols, dropna=False, as_index=False).agg(list)
     
normal_grouped = variant_info(normal_subset)
tumor_grouped  = variant_info(tumor_subset)

#new col with number of patients per variant 
normal_grouped["N#"] = normal_grouped["Patient_ID"].apply(lambda x: len(set(x)))
tumor_grouped["T#"]  = tumor_grouped["Patient_ID"].apply(lambda x: len(set(x)))

print(normal_grouped)
print(tumor_grouped)

#rename cols with : Patient_ID and VCF_ID, to have, _Normal or _Tumor, added depending 
#which file you are working with. 
normal_grouped.rename(columns={"Patient_ID": "Patient_ID_Normal", "VCF_ID": "VCF_ID_Normal"}, inplace=True)
tumor_grouped.rename(columns={"Patient_ID": "Patient_ID_Tumor", "VCF_ID": "VCF_ID_Tumor"}, inplace=True)

print(normal_grouped)
print(tumor_grouped)


#Part 1.2 
# Using the output from part A, merge (how = outer) the Normal and Tumor together based 
#on the columns [chrom, left, ref_seq, alt_seq] into a single CSV file named AML
normal_unique_variants = (normal_grouped[variant_cols].drop_duplicates().shape[0])
tumor_unique_variants = (tumor_grouped[variant_cols].drop_duplicates().shape[0])

print(normal_unique_variants)
print(tumor_unique_variants)

print(normal_unique_variants - normal_unique_variants)
print(tumor_unique_variants - normal_unique_variants)

#how many unique normal and tumor variants shared between both, common 
common_variants = (normal_grouped[variant_cols].drop_duplicates().merge(tumor_grouped[variant_cols].drop_duplicates(), on= variant_cols, how= "inner"))

print(common_variants)
print(common_variants.shape[0])

#AML csv file 
AML = normal_grouped.merge(tumor_grouped, on=variant_cols, how="outer")
aml_out_path = "C:/Users/Ricardo/Desktop/Output_Final_Normal_and_Tumor/AML.csv"
AML.to_csv(aml_out_path, index=False)

#Part 1.3 
#Using the Normal and Tumor files from Homework 3, concatenate these files along the axis = 0, 
#with this Expand/Explode the rows based on the CSQ columns and save this file
#as AML_Expand.csv. Remove duplicate rows.

aml_concat = pd.concat([hk3_normal_csv, hk3_tumor_csv], axis=0, ignore_index=True)
print(aml_concat.shape[0])

aml_expand = aml_concat.drop_duplicates()

csq_columns = ["Allele", "Consequence", "IMPACT", "SYMBOL", "Gene", "Feature_type", "Feature", "BIOTYPE", "EXON", "INTRON", "HGVSc", "HGVSp", "cDNA_position", "CDS_position", "Protein_position", "Amino_acids", "Codons", "Existing_variation", "ALLELE_NUM", "DISTANCE", "STRAND", "FLAGS", "VARIANT_CLASS", "SYMBOL_SOURCE", "HGNC_ID", "CANONICAL", "TSL", "APPRIS", "CCDS", "ENSP", "SWISSPROT", "TREMBL", "UNIPARC", "RefSeq", "GENE_PHENO", "SIFT", "PolyPhen", "DOMAINS", "HGVS_OFFSET", "GMAF", "AFR_MAF", "AMR_MAF", "EAS_MAF", "EUR_MAF", "SAS_MAF", "AA_MAF", "EA_MAF", "ExAC_MAF", "ExAC_Adj_MAF", "ExAC_AFR_MAF", "ExAC_AMR_MAF", "ExAC_EAS_MAF", "ExAC_FIN_MAF", "ExAC_NFE_MAF", "ExAC_OTH_MAF", "ExAC_SAS_MAF", "CLIN_SIG", "SOMATIC", "PHENO", "PUBMED", "MOTIF_NAME", "MOTIF_POS", "HIGH_INF_POS", "MOTIF_SCORE_CHANGE", "ENTREZ","EVIDENCE"]

aml_merged = aml_expand.copy() 

for col in csq_columns:
    if col in aml_merged.columns:
        for row in range(aml_merged.shape[0]):
            temp = str(aml_merged[col][row])
            temp = temp.strip("[]").replace('"', "").replace("'", "").replace(" ", "")
            aml_merged.at[row, col] = temp.split(",")
            if type(aml_merged[col][row]) != list:
                print(aml_merged[col][row])
                print(type(aml_merged[col][row]))

aml_exploded = aml_merged.explode(csq_columns, ignore_index=True)

aml_expand_path = "C:/Users/Ricardo/Desktop/Output_Final_Normal_and_Tumor/AML_Expand.csv"
aml_exploded.to_csv(aml_expand_path, index=False)

print(aml_exploded.shape)
print(aml_exploded.shape[0])

gene_cols = ["SYMBOL", "Gene", "Feature"]
gene_cols = [c for c in gene_cols if c in aml_expand.columns]
aml_gene = aml_expand[gene_cols].drop_duplicates() if gene_cols else pd.DataFrame()
aml_gene_path = "C:/Users/Ricardo/Desktop/Output_Final_Normal_and_Tumor/AML_gene.csv"
aml_gene.to_csv(aml_gene_path, index=False)

print(aml_gene.shape)
print(aml_gene.shape[0])

tx_cols = ["chrom", "left", "right", "ref_seq", "alt_seq", "Feature", "cDNA_position", "BIOTYPE"]
tx_cols = [c for c in tx_cols if c in aml_expand.columns]
aml_tx = aml_expand[tx_cols].drop_duplicates() if tx_cols else pd.DataFrame()
aml_tx_path = "C:/Users/Ricardo/Desktop/Output_Final_Normal_and_Tumor/AML_tx.csv"
aml_tx.to_csv(aml_tx_path, index=False)

print(aml_tx)
print(aml_tx.shape[0])







