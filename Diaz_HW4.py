# Ricardo Diaz 
# Post Genomics HW4 


#Part 1
import argparse, pandas as pd
from pathlib import Path

#read the final csv from previous homeworks first from wherever they are 
normal_df_1 = pd.read_csv("C:/Users/ricar/OneDrive/Desktop/Output_Final_Normal_and_Tumor/Final_Normal.csv")
tumor_df_1  = pd.read_csv("C:/Users/ricar/OneDrive/Desktop/Output_Final_Normal_and_Tumor/Final_Tumor.csv")

#trim header spaces to avoid silent rename misses
normal_df_1.columns = normal_df_1.columns.str.strip()
tumor_df_1.columns  = tumor_df_1.columns.str.strip()

#need to rename some coloumns as well for snpnexus format  
rename_col = {"position": "left", "ref": "ref_seq", "alt": "alt_seq"}
normal_df_1.rename(columns=rename_col, inplace=True)
tumor_df_1.rename(columns=rename_col, inplace=True)

print(normal_df_1)

#strand column
normal_df_1["strand"] = -1
tumor_df_1["strand"]  = -1

#adding the chromoso 
def add_chrom_id(df):
    df["chromosome"] = df["chrom"].astype(str).str.replace(r"^chr", "", regex=True)
    if "var_index" in df.columns:
        df["ID"] = df["var_index"]
    else:
        df["ID"] = range(1, len(df) + 1)

add_chrom_id(normal_df_1)
add_chrom_id(tumor_df_1)

def build_snpnexus(df):
    return pd.DataFrame({
        "Type":      "Chromosome",                                   
        "Id":        df["chromosome"].astype(str),            
        "Position":  df["left"],                                    
        "Allele1":   df["ref_seq"].astype(str),
        "Allele2":   df["alt_seq"].astype(str),
        "Strand":    df["strand"]                                     
    })

extracted_df_normal = build_snpnexus(normal_df_1)
extracted_df_tumor  = build_snpnexus(tumor_df_1)

#check outgoing headers
print("NORMAL headers:", list(extracted_df_normal.columns))
print("TUMOR  headers:", list(extracted_df_tumor.columns))

#write with exact headers preserved
extracted_df_normal.to_csv("C:/Users/ricar/OneDrive/Desktop/Output_Final_Normal_and_Tumor/Output_normal.txt",sep="\t", index=False, header=True)
extracted_df_tumor.to_csv("C:/Users/ricar/OneDrive/Desktop/Output_Final_Normal_and_Tumor/Output_tumor.txt", sep="\t", index=False, header=True)


#part 1.2 

#merge the snpnexus results with original csv file 

snpnexus_tsv_normal = pd.read_csv("C:/Users/ricar/OneDrive/Desktop/Output_Final_Normal_and_Tumor/Normal_txt_pervariant/Normal_txt_pervariant.tsv" , sep ="\t")
snpnexus_tsv_tumor = pd.read_csv("C:/Users/ricar/OneDrive/Desktop/Output_Final_Normal_and_Tumor/Normal_txt_pervariant/Normal_txt_pervariant.tsv", sep = "\t")

normal_df_1 = normal_df_1.reset_index(drop=True)
tumor_df_1 = tumor_df_1.reset_index(drop=True)


snpnexus_normal_merged = pd.concat([normal_df_1, snpnexus_tsv_normal], axis= 1)
snpnexus_tumor_merged = pd.concat([tumor_df_1, snpnexus_tsv_tumor] ,axis= 1)

print(snpnexus_normal_merged)

snpnexus_normal_merged.to_csv("C:/Users/ricar/OneDrive/Desktop/Output_Final_Normal_and_Tumor/Normal_snpnexus.csv")
snpnexus_tumor_merged.to_csv("C:/Users/ricar/OneDrive/Desktop/Output_Final_Normal_and_Tumor/Tumor_snpnexus.csv")

#also merge the FATHMM-XF results with the previous snpnexus + original csv 

snpnexus_normal_merged = snpnexus_normal_merged.reset_index(drop=True)
snpnexus_tumor_merged = snpnexus_tumor_merged.reset_index(drop=True)

fathm_normal = pd.read_csv("C:/Users/ricar/OneDrive/Desktop/Output_Final_Normal_and_Tumor/normal_fathmm.txt", sep="\t")
fathm_tumor = pd.read_csv("C:/Users/ricar/OneDrive/Desktop/Output_Final_Normal_and_Tumor/tumor_fathmm.txt", sep="\t")


fathmm_normal_merged = pd.concat([snpnexus_normal_merged, fathm_normal], axis=1)
fathmm_tumor_merged = pd.concat([snpnexus_tumor_merged, fathm_tumor], axis=1)


#drop some coloumns unecessary coloumns
#fathmm_normal_merged = fathmm_normal_merged.drop(columns=["strand", "chrom", "# Chromosome", "ID"])

fathmm_normal_merged.to_csv("C:/Users/ricar/OneDrive/Desktop/Output_Final_Normal_and_Tumor/all_merged_hw4_normal.csv")
fathmm_tumor_merged.to_csv("C:/Users/ricar/OneDrive/Desktop/Output_Final_Normal_and_Tumor/all_merged_hw4_tumor.csv")

