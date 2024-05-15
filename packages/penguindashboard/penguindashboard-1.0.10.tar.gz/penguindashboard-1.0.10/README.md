# PEngUIN - Protein Engineering Using Independent Networks

PEngUIN (Protein Engineering Using Independent Networks) is a comprehensive protein engineering dashboard designed to streamline the process of protein analysis and engineering using advanced deep learning models. By inputting a protein sequence or fasta file, users can leverage powerful tools such as BLAST, ESM-2, SaProt, MutCompute, ProteinMPNN, and AntiBERTa to generate suggested mutations for protein engineering.

## Installation

To get started with PEngUIN, you can install the package using pip:

```bash
pip install penguindashboard
```


### Prerequisites

(Required packages and setup instructions will be listed here)

## Usage

To use PEngUIN, simply input your protein sequence or fasta file. The dashboard will handle the rest, running various deep learning models to analyze the input and suggest potential modifications.

(Commands and detailed usage instructions will be provided here)

## Features

PEngUIN offers a range of functionalities centered around protein engineering:

- **BLAST**: Provides mutational analysis based on homologues sequences from an API BLAST call.
- **ESM-2**: Mutation residue prediction across all positions in a sequence using ESM-2 (650M).
- **SaProt**: Mutation residue prediction using the Steinnegar Lab's structure aware language model, SaProt.
- **MutCompute**: Structure-based masked prediction using Ellington Lab's MutCompute model.
- **ProteinMPNN**: In-painting of single residues across the entire sequence using Baker Lab's ProteinMPNN.
- **AntiBERTa**: Mutation prediction the Antibody specific protein language model AntiBERTa.

## Output

The output from PEngUIN consists of npy logits files, which contain detailed predictions in a specific amino acid order. 

Sequence order is as follows:
```bash
amino_acids = ['A', 'R', 'N', 'D', 'C', 'Q', 'E', 'G', 'H', 'I', 'L', 'K', 'M', 'F', 'P', 'S', 'T', 'W', 'Y', 'V']
```

## License

PEngUIN is available under the MIT License. See the LICENSE file for more details.
