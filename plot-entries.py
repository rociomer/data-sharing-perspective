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
substance_dates, substance_count   = load_pubchem_data(filename="./data/pubchem-substances-data-count.csv")
assay_dates, assay_count           = load_pubchem_data(filename="./data/pubchem-bioassays-data-count.csv")
compound_dates, compound_count     = load_pubchem_data(filename="./data/pubchem-compounds-data-count.csv")

# plot the PubChem data
fig, ax = plt.subplots(1, 1, figsize=(15,5))
#ax.plot(substance_dates, substance_count, label=f"PubChem Substances", color=palette2[0])
ax.plot(assay_dates, assay_count, label=f"PubChem BioAssays", color=palette2[1])
#ax.plot(compound_dates, compound_count, label=f"PubChem Compounds", color=palette2[2])
ax.legend(frameon=False)
ytick = max(assay_count[-1], assay_count[-1], assay_count[-1])
ax.set(xticks=[assay_dates[i] for i in [0, -1]], yticks=[ytick])
ax.set_xticklabels(labels=[assay_dates[i].astype(object).year for i in [0, -1]], rotation=45, ha="right", rotation_mode="anchor")
ax.set_yticklabels(labels=[f"{ytick:.2e}"])
fig.tight_layout()
fig.savefig("pubchem-count.png")

## ChEMBL
# load the ChEMBL data
chembl_versions, chembl_dates, chembl_compounds, chembl_activities, chembl_assays, chembl_targets, chembl_documents = load_chembl_data(filename="./data/chembl-documents.csv")

# plot the ChEMBL data
fig, ax = plt.subplots(1, 1, figsize=(15,5))
ax.plot(chembl_dates, chembl_compounds, color=palette2[3], label="ChEMBL compounds")
ax.legend(frameon=False)
ytick = chembl_compounds[-1]
ax.set(xticks=[chembl_dates[i] for i in [0, -1]], yticks=[ytick])
ax.set_xticklabels(labels=[chembl_dates[i].astype(object).year for i in [0, -1]], rotation=45, ha="right", rotation_mode="anchor")
ax.set_yticklabels(labels=[f"{ytick:.2e}"])
fig.tight_layout()
fig.savefig("chembl-compounds.png")

## PDB
# load the PDB data
pdb_dates, pdb_total_entries, pdb_annual_entries = load_pdb_data(filename="./data/pdb-entries.csv")

# plot the PDB data
fig, ax = plt.subplots(1, 1, figsize=(15,5))
ax.plot(pdb_dates, pdb_total_entries, color=palette2[4], label="PDB entries")
ax.legend(frameon=False)
ytick = pdb_total_entries[-1]
ax.set(xticks=[pdb_dates[i] for i in [0, -1]], yticks=[ytick])
ax.set_xticklabels(labels=[pdb_dates[i].astype(object).year for i in [0, -1]], rotation=45, ha="right", rotation_mode="anchor")
ax.set_yticklabels(labels=[f"{ytick:.2e}"])
fig.tight_layout()
fig.savefig("pdb-entries.png")

## CSD
# load the CSD data
csd_dates, csd_structures, csd_ave_n_atoms_per_structure = load_csd_data(filename="./data/csd-structures.csv")

# plot the CSD data
fig, ax = plt.subplots(1, 1, figsize=(15,5))
ax.plot(csd_dates, np.cumsum(csd_structures), color=palette2[6], label="CSD structures")
ax.legend(frameon=False)
ytick = np.cumsum(csd_structures)[-1]
ax.set(xticks=[csd_dates[i] for i in [0, -1]], yticks=[ytick])
ax.set_xticklabels(labels=[csd_dates[i].astype(object).year for i in [0, -1]], rotation=45, ha="right", rotation_mode="anchor")
ax.set_yticklabels(labels=[f"{ytick:.2e}"])
fig.tight_layout()
fig.savefig("csd-structures.png")

# plot all the data together
fig, ax = plt.subplots(1, 1, figsize=(18, 4.5))
ax.plot(csd_dates, np.cumsum(csd_structures), color=palette2[6], label="CSD structures")
ax.scatter(csd_dates[0], np.cumsum(csd_structures)[0], color=palette2[6], marker="o")
ax.scatter(csd_dates[-1], np.cumsum(csd_structures)[-1], color=palette2[6], marker=">")
ax.plot(pdb_dates, pdb_total_entries, color=palette2[4], label="PDB entries")
ax.scatter(pdb_dates[0], pdb_total_entries[0], color=palette2[4], marker="o")
ax.scatter(pdb_dates[-1], pdb_total_entries[-1], color=palette2[4], marker=">")
#ax.plot(substance_dates, substance_count, label=f"PubChem Substances", color=palette2[0])
#ax.scatter(substance_dates[0], substance_count[0], color=palette2[0], marker="o")
#ax.scatter(substance_dates[-1], substance_count[-1], color=palette2[0], marker=">")
ax.plot(assay_dates, assay_count, label=f"PubChem BioAssays", color=palette2[1])
ax.scatter(assay_dates[0], assay_count[0], color=palette2[1], marker="o")
ax.scatter(assay_dates[-1], assay_count[-1], color=palette2[1], marker=">")
#ax.plot(compound_dates, compound_count, label=f"PubChem Compounds", color=palette2[2])
#ax.scatter(compound_dates[0], compound_count[0], color=palette2[2], marker="o")
#ax.scatter(compound_dates[-1], compound_count[-1], color=palette2[2], marker=">")
ax.plot(chembl_dates, chembl_compounds, color=palette2[3], label="ChEMBL compounds")
ax.scatter(chembl_dates[0], chembl_compounds[0], color=palette2[3], marker="o")
ax.scatter(chembl_dates[-1], chembl_compounds[-1], color=palette2[3], marker=">")
ax.legend(frameon=False, bbox_to_anchor=(1.01, 1), borderaxespad=0)
ax.set_yscale("log")
ax.set(xlabel="Year", ylabel="Count")
fig.tight_layout()
fig.savefig("all.png")