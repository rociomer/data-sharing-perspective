import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from typing import Tuple

# set Seaborn themes and color palettes
sns.set_theme("talk", "white")
palette1 = sns.color_palette("Paired")  # for visualizing data that comes in pairs
palette2 = sns.color_palette("tab10")   # for visualizing other data

# define some functions
def load_pubchem_data(filename : str) -> Tuple[list, list]:
    with open(filename, "r") as input_data:
        # read entries; each entry is a separate line
        raw_input = input_data.read().split("\n")
    
        # parse the date and separate it from the source count
        date, count = [], []
        for line in raw_input[1:]:  # skip first row (header)
            split_line = line.split(", ")
            date.append(np.datetime64(split_line[0]))
            count.append(int(split_line[1]))
    
        return date, count

def load_chembl_data(filename : str) -> Tuple[list, list]:
    with open(filename, "r") as input_data:
        # read entries; each entry is a separate line
        raw_input = input_data.read().split("\n")
    
        # parse the date and separate it from the source count
        version, date, compounds, activities, assays, targets, documents= [], [], [], [], [], [], []
        for line in raw_input[1:]:  # skip first row (header)
            split_line = line.split(", ")
            version.append(split_line[0])
            date.append(np.datetime64(split_line[1]))
            compounds.append(int(split_line[2]))
            activities.append(int(split_line[3]))
            assays.append(int(split_line[4]))
            targets.append(int(split_line[5]))
            documents.append(int(split_line[6]))
    
        return version, date, compounds, activities, assays, targets, documents

## PubChem
# load the PubChem data
substance_dates, substance_sources   = load_pubchem_data(filename="./data/pubchem-substance-sources.csv")
assay_dates, assay_sources           = load_pubchem_data(filename="./data/pubchem-assay-sources.csv")
RNAi_assay_dates, RNAi_assay_sources = load_pubchem_data(filename="./data/pubchem-RNAi-assay-sources.csv")

# plot the PubChem data
fig, ax = plt.subplots(1, 1, figsize=(12,6))
x = np.arange(len(substance_dates))
ax.bar(x=x[::2], height=substance_sources[::2], label=f"Substances", color=palette2[0], width=2, align="edge")
ax.bar(x=x[::2], height=assay_sources[::2], label=f"Assays", bottom=substance_sources[::2], color=palette2[1], width=2, align="edge")
ax.bar(x=x[::2], height=RNAi_assay_sources[::2], label=f"RNAi assays", bottom=(np.array(substance_sources[::2])+np.array(assay_sources[::2])), color=palette2[2], width=2, align="edge")
ax.legend()
ax.set(xlabel="Date",
       ylabel="Data sources",
	   xticks=x[::14])
ax.set_xticklabels(labels=substance_dates[::14], rotation=45)
fig.tight_layout()
fig.savefig("pubchem-sources.png")

## ChEMBL
# load the ChEMBL data
chembl_versions, chembl_dates, chembl_compounds, chembl_activities, chembl_assays, chembl_targets, chembl_documents = load_chembl_data(filename="./data/chembl-documents.csv")
# plot the PubChem data
fig, ax = plt.subplots(1, 1, figsize=(12,6))
x = np.arange(len(chembl_dates))
ax.bar(x=x, height=chembl_documents, label=f"Documents", color=palette2[3], width=1, align="edge")
ax.legend()
ax.set(xlabel="Date",
       ylabel="Documents",
	   xticks=x[::2])
ax.set_xticklabels(labels=chembl_dates[::2], rotation=45)
fig.tight_layout()
fig.savefig("chembl-documents.png")

## PDB

## CSD