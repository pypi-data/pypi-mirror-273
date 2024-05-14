import argparse
from Bio.Blast import NCBIWWW, NCBIXML
from io import StringIO
import pandas as pd
from Bio.Seq import Seq
from Bio.SeqRecord import SeqRecord
from Bio import SeqIO
import os
import numpy as np
import subprocess

def perform_blast_search(sequence):
    print('Performing BLAST search...')
    blast_result = NCBIWWW.qblast("blastp", "nr", sequence, hitlist_size=100, format_type='XML', expect=0.001)
    return blast_result.read()

def parse_blast_xml(xml_blast):
    result_handle = StringIO(xml_blast)
    return next(NCBIXML.parse(result_handle))

def create_df(blast_record, sequence):
    df = pd.DataFrame([{'description': 'query_sequence', 'seq': sequence}] +
                        [{'description': alignment.hit_def, 'seq': hsp.sbjct} for alignment in blast_record.alignments for hsp in alignment.hsps if hsp.expect < 0.04])
    return df

def write_sequences(df):
    records = [SeqRecord(Seq(row['seq']), id=row['description'], description='') for index, row in df.iterrows()]
    # make dir if it does not exist
    SeqIO.write(records, f'{args.outdir}/BLAST/all_sequences.fasta', 'fasta')
    SeqIO.write(records[0], f'{args.outdir}/BLAST/query.fasta', 'fasta')
    SeqIO.write(records[1:], f'{args.outdir}/BLAST/targets.fasta', 'fasta')

def perform_msa():
    input_path = f'{args.outdir}/BLAST/all_sequences.fasta'
    output_path = f'{args.outdir}/BLAST/msa.fasta'
    
    # Build the command as a list
    command = ['mafft', '--auto', input_path]
    
    # Execute the command, capturing stdout (the MSA result)
    result = subprocess.run(command, capture_output=True, text=True, check=True)
    
    # Write the MSA result to the output file
    with open(output_path, 'w') as handle:
        handle.write(result.stdout)

    # Optionally, handle stderr or errors
    if result.stderr:
        print("MAFFT generated warnings/errors:", result.stderr)

def calculate_percentages():
    sequences = [str(record.seq) for record in SeqIO.parse(f'{args.outdir}/BLAST/msa.fasta', "fasta")]
    non_gap_indices = [i for i, char in enumerate(sequences[0]) if char != '-']
    filtered_sequences = [''.join(seq[i] for i in non_gap_indices) for seq in sequences]
    transposed_sequences = list(map(list, zip(*filtered_sequences)))

    # Create a DataFrame from the transposed list for easier manipulation.
    df = pd.DataFrame(transposed_sequences)

    aa_list = ['A', 'R', 'N', 'D', 'C', 'Q', 'E', 'G', 'H', 'I', 'L', 'K', 'M', 'F', 'P', 'S', 'T', 'W', 'Y', 'V']

    # Initialize an empty DataFrame to store frequencies
    percentage_df = pd.DataFrame(0, columns=aa_list, index=range(len(df)), dtype=float)

    # Calculate frequencies.
    for index, row in df.iterrows():
        row_counts = row.value_counts(normalize=True)  # Get normalized counts as frequencies directly.
        for aa in aa_list:
            if aa in row_counts:  # Check if the amino acid is present in the row_counts.
                percentage_df.at[index, aa] = row_counts.get(aa, 0)  # Update frequency.

    # softmax across columns
    percentage_df = percentage_df.div(percentage_df.sum(axis=1), axis=0)

    return percentage_df


def main(args):
    xml_blast = perform_blast_search(args.sequence)
    blast_record = parse_blast_xml(xml_blast)
    df = create_df(blast_record, args.sequence)
    write_sequences(df)
    perform_msa()
    df = calculate_percentages()
    
    # save to np array
    np.save(f"{args.outdir}/{args.name}.logits.blast_phylogeny.npy", df.to_numpy())

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='BLAST search and analysis')
    parser.add_argument('--sequence', type=str, required=True, help='Amino acid sequence for BLAST search')
    parser.add_argument('--outdir', type=str, required=True, help='Output directory for results')
    parser.add_argument('--name', type=str, required=True, help='Name of the sequence')
    args = parser.parse_args()
    # create directory if it does not exist
    os.makedirs(args.outdir, exist_ok=True)
    os.makedirs(args.outdir + '/BLAST', exist_ok=True)

    main(args)
    