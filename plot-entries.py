"""
A script for plotting the data which is available in the databases (case studies)
discussed in the data-sharing perspective.
"""
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from typing import Tuple

# set Seaborn themes and color palettes
sns.set_theme("poster", "ticks")
palette2 = sns.color_palette("muted")

# define some functions for loading the data
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

        return date, np.array(count)

def load_chembl_data(filename : str) -> Tuple[list, list, list, list, list, list]:
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

def load_pdb_data(filename : str) -> Tuple[list, list, list]:
    with open(filename, "r") as input_data:
        # read entries; each entry is a separate line
        raw_input = input_data.read().split("\n")
    
        # parse the date and separate it from the source count
        date, total_entries, annual_entries = [], [], []
        for line in raw_input[1:]:  # skip first row (header)
            split_line = line.split(", ")
            date.append(np.datetime64(split_line[0]))
            total_entries.append(int(split_line[1]))
            annual_entries.append(int(split_line[2]))
    
        return date, total_entries, annual_entries

def load_csd_data(filename : str) -> Tuple[list, list, list]:
    with open(filename, "r") as input_data:
        # read entries; each entry is a separate line
        raw_input = input_data.read().split("\n")
    
        # parse the date and separate it from the source count
        date, annual_structures, ave_n_atoms_per_structure = [], [], []
        for line in raw_input[1:]:  # skip first row (header)
            split_line = line.split(", ")
            date.append(np.datetime64(split_line[0]))
            annual_structures.append(int(split_line[1]))
            try:
                ave_n_atoms_per_structure.append(int(split_line[2]))
            except ValueError:
                ave_n_atoms_per_structure.append(np.NAN)
    
        return date, annual_structures, ave_n_atoms_per_structure

## PubChem
# load the PubChem data
substance_dates, substance_sources   = load_pubchem_data(filename="./data/pubchem-substance-sources.csv")
assay_dates, assay_sources           = load_pubchem_data(filename="./data/pubchem-assay-sources.csv")
RNAi_assay_dates, RNAi_assay_sources = load_pubchem_data(filename="./data/pubchem-RNAi-assay-sources.csv")

# plot the PubChem data
fig, ax = plt.subplots(1, 1, figsize=(15,5))
ax.plot(substance_dates, substance_sources, label=f"PubChem Substances", color=palette2[0])
ax.plot(assay_dates, assay_sources, label=f"PubChem Assays", color=palette2[1])
ax.plot(RNAi_assay_dates, RNAi_assay_sources, label=f"PubChem RNAi assays", color=palette2[2])
ax.legend()
ytick = max(substance_sources[-1], assay_sources[-1], RNAi_assay_sources[-1])
ax.set(xticks=[substance_dates[i] for i in [0, 1, -1]], yticks=[ytick])
ax.set_xticklabels(labels=[substance_dates[i].astype(object).year for i in [0, 1, -1]], rotation=45, ha="right", rotation_mode="anchor")
ax.set_yticklabels(labels=[f"{ytick:.2e}"])
fig.tight_layout()
fig.savefig("pubchem-sources.png")

## ChEMBL
# load the ChEMBL data
chembl_versions, chembl_dates, chembl_compounds, chembl_activities, chembl_assays, chembl_targets, chembl_documents = load_chembl_data(filename="./data/chembl-documents.csv")

# plot the PubChem data
fig, ax = plt.subplots(1, 1, figsize=(15,5))
ax.plot(chembl_dates, chembl_documents, color=palette2[3], label="ChEMBL documents")
ax.legend()
ytick = chembl_documents[-1]
ax.set(xticks=[chembl_dates[i] for i in [0, 1, -1]], yticks=[ytick])
ax.set_xticklabels(labels=[chembl_dates[i].astype(object).year for i in [0, 1, -1]], rotation=45, ha="right", rotation_mode="anchor")
ax.set_yticklabels(labels=[f"{ytick:.2e}"])
fig.tight_layout()
fig.savefig("chembl-documents.png")

## PDB
# load the PDB data
pdb_dates, pdb_total_entries, pdb_annual_entries = load_pdb_data(filename="./data/pdb-entries.csv")

# plot the PDB data
fig, ax = plt.subplots(1, 1, figsize=(15,5))
ax.plot(pdb_dates, pdb_total_entries, color=palette2[4], label="PDB entries")
ax.legend()
ytick = pdb_total_entries[-1]
ax.set(xticks=[pdb_dates[i] for i in [0, 1, -1]], yticks=[ytick])
ax.set_xticklabels(labels=[pdb_dates[i].astype(object).year for i in [0, 1, -1]], rotation=45, ha="right", rotation_mode="anchor")
ax.set_yticklabels(labels=[f"{ytick:.2e}"])
fig.tight_layout()
fig.savefig("pdb-entries.png")

## CSD
# load the CSD data
csd_dates, csd_structures, csd_ave_n_atoms_per_structure = load_csd_data(filename="./data/csd-structures.csv")

# plot the CSD data
fig, ax = plt.subplots(1, 1, figsize=(15,5))
ax.plot(csd_dates, np.cumsum(csd_structures), color=palette2[6], label="CSD structures")
ax.legend()
ytick = np.cumsum(csd_structures)[-1]
ax.set(xticks=[csd_dates[i] for i in [0, -1]], yticks=[ytick])
ax.set_xticklabels(labels=[csd_dates[i].astype(object).year for i in [0, -1]], rotation=45, ha="right", rotation_mode="anchor")
ax.set_yticklabels(labels=[f"{ytick:.2e}"])
fig.tight_layout()
fig.savefig("csd-structures.png")