import pandas as pd
import torch
import numpy as np
import subprocess
import os
import argparse

def run_mpnn(proteinmpnn_dir, pdb_file, device, output_prefix):
    cwd = os.getcwd() # Save current working directory
    os.chdir(proteinmpnn_dir) # Change directory to where MPNN scripts are centered at
    command = (
        'python ./score.py '
        '--model_type protein_mpnn '
        '--checkpoint_protein_mpnn ./model_params/v_48_020.pt '
        '--seed 42 '
        '--single_aa_score 1 '
        f'--out_folder {cwd}/{output_prefix}/ProteinMPNN '
        f'--pdb_path {cwd}/{pdb_file} '
        '--use_sequence 1 '
        '--batch_size 1 '
        '--number_of_batches 20 '
        f'--device {device}'
    )
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    out, err = process.communicate() # for debugging
    # print(out)
    # print('\n')
    # print(err)
    os.chdir(cwd) # Change directory back to original
    output = torch.load(f'{output_prefix}/ProteinMPNN/{pdb_file.split("/")[-1].split(".")[0]}.pt')
    logits = output['logits'].mean(axis=0)
    return logits

def standardize_vocab(nplogits, output_prefix, pdb_file):
    amino_acids = ['A', 'R', 'N', 'D', 'C', 'Q', 'E', 'G', 'H', 'I', 'L', 'K', 'M', 'F', 'P', 'S', 'T', 'W', 'Y', 'V']
    mpnn_alphabet = {"A": 0,"C": 1,"D": 2,"E": 3,"F": 4,"G": 5,"H": 6,"I": 7,"K": 8,"L": 9,
    "M": 10,"N": 11,"P": 12,"Q": 13,"R": 14,"S": 15,"T": 16,"V": 17,"W": 18,"Y": 19
    }
    ### Changing vocab by summing logits ###
    new_nplogits = []
    for aa in amino_acids:
        new_nplogits.append(nplogits[:,mpnn_alphabet[aa]])
    new_nplogits = np.array(new_nplogits).T
    np.save(f'{output_prefix}/{pdb_file.split("/")[-1].split(".")[0]}.logits.ProteinMPNN_v_48_020.npy', new_nplogits)

def main():
    proteinmpnn_dir = args.proteinmpnn_dir
    pdb_file = args.pdb_file
    output_prefix = args.output_prefix
    device = args.device

    # make directory {output_prefix}/ProteinMPNN/ if it does not exist
    os.makedirs(f'{output_prefix}/ProteinMPNN/', exist_ok=True)

    nplogits = run_mpnn(proteinmpnn_dir, pdb_file, device, output_prefix).astype(np.float128)
    
    standardize_vocab(nplogits, output_prefix, pdb_file)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Process amino acid and 3Di sequences using SaProt model.')
    parser.add_argument('--proteinmpnn_dir', type=str, help='Path to the proteinmpnn directory')
    parser.add_argument('--pdb_file', type=str, help='Path to the pdb file')
    parser.add_argument('--output_prefix', type=str, help='Optional prefix to add to the output filename')
    parser.add_argument('--device', type=str, help='Specify the Cuda device index', default = '0')

    args = parser.parse_args()

    main(args)
