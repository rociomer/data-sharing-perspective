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
        version, date, sources = [], [], []
        for line in raw_input[1:]:  # skip first row (header)
            split_line = line.split(", ")
            version.append(split_line[0])
            date.append(np.datetime64(split_line[1]))
            sources.append(int(split_line[2]))

        return version, date, sources

def load_pdb_data(filename : str) -> Tuple[list, list, list]:
    with open(filename, "r") as input_data:
        # read entries; each entry is a separate line
        raw_input = input_data.read().split("\n")

        # parse the date and separate it from the source count
        date, depositors, = [], []
        for line in raw_input[1:]:  # skip first row (header)
            split_line = line.split(", ")
            date.append(np.datetime64(split_line[0]))
            depositors.append(int(split_line[1]))

        return date, depositors

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
ax.legend(frameon=False)
ytick = max(substance_sources[-1], assay_sources[-1], RNAi_assay_sources[-1])
ax.set(xticks=[substance_dates[i] for i in [0, -1]], yticks=[ytick])
ax.set_xticklabels(labels=[substance_dates[i].astype(object).year for i in [0, -1]], rotation=45, ha="right", rotation_mode="anchor")
ax.set_yticklabels(labels=[f"{ytick:.2e}"])
fig.tight_layout()
fig.savefig("plots/pubchem-sources.png")

## ChEMBL
# load the ChEMBL data
chembl_versions, chembl_dates, chembl_sources = load_chembl_data(filename="./data/chembl-sources.csv")

# plot the ChEMBL data
fig, ax = plt.subplots(1, 1, figsize=(15,5))
ax.plot(chembl_dates, chembl_sources, color=palette2[3], label="ChEMBL sources")
ax.legend(frameon=False)
ytick = chembl_sources[-1]
ax.set(xticks=[chembl_dates[i] for i in [0, -1]], yticks=[ytick])
ax.set_xticklabels(labels=[chembl_dates[i].astype(object).year for i in [0, -1]], rotation=45, ha="right", rotation_mode="anchor")
ax.set_yticklabels(labels=[f"{ytick:.2e}"])
fig.tight_layout()
fig.savefig("plots/chembl-sources.png")

## PDB
# load the PDB data
pdb_dates, pdb_depositors = load_pdb_data(filename="./data/pdb-depositors.csv")

# plot the PDB data
fig, ax = plt.subplots(1, 1, figsize=(15,5))
ax.plot(pdb_dates, pdb_depositors, color=palette2[4], label="PDB depositors")
ax.legend(frameon=False)
ytick = pdb_depositors[-1]
ax.set(xticks=[pdb_dates[i] for i in [0, -1]], yticks=[ytick])
ax.set_xticklabels(labels=[pdb_dates[i].astype(object).year for i in [0, -1]], rotation=45, ha="right", rotation_mode="anchor")
ax.set_yticklabels(labels=[f"{ytick:.2e}"])
fig.tight_layout()
fig.savefig("plots/pdb-depositors.png")

# plot all the data together
fig, ax = plt.subplots(1, 1, figsize=(18, 4.5))
ax.plot(pdb_dates, pdb_depositors, color=palette2[4], label="PDB depositors")
ax.scatter(pdb_dates[0], pdb_depositors[0], color=palette2[4], marker="o")
ax.scatter(pdb_dates[-1], pdb_depositors[-1], color=palette2[4], marker=">")
ax.plot(substance_dates, substance_sources, label=f"PubChem Substances sources", color=palette2[0])
ax.scatter(substance_dates[0], substance_sources[0], color=palette2[0], marker="o")
ax.scatter(substance_dates[-1], substance_sources[-1], color=palette2[0], marker=">")
ax.plot(assay_dates, assay_sources, label=f"PubChem Assays sources", color=palette2[1])
ax.scatter(assay_dates[0], assay_sources[0], color=palette2[1], marker="o")
ax.scatter(assay_dates[-1], assay_sources[-1], color=palette2[1], marker=">")
ax.plot(RNAi_assay_dates, RNAi_assay_sources, label=f"PubChem RNAi Assay sources", color=palette2[2])
ax.scatter(RNAi_assay_dates[0], RNAi_assay_sources[0], color=palette2[2], marker="o")
ax.scatter(RNAi_assay_dates[-1], RNAi_assay_sources[-1], color=palette2[2], marker=">")
ax.plot(chembl_dates, chembl_sources, color=palette2[3], label="ChEMBL sources")
ax.scatter(chembl_dates[0], chembl_sources[0], color=palette2[3], marker="o")
ax.scatter(chembl_dates[-1], chembl_sources[-1], color=palette2[3], marker=">")
ax.legend(frameon=False, bbox_to_anchor=(1.01, 1), borderaxespad=0)
ax.set_yscale("log")
ax.set(xlabel="Year", ylabel="Count")
fig.tight_layout()
fig.savefig("plots/all-contributors.png")