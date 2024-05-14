import argparse
import numpy as np
import torch
from transformers import AutoTokenizer, AutoModelForMaskedLM


def get_data(fasta_file):
    data = []
    with open(fasta_file, 'r') as inf:
        header, seq = None, None
        for line in inf:
            if line.startswith('>'):
                if header and seq:
                    data.append((header, seq))
                header, seq = line.strip('\n')[1:], ''
            else:
                seq += line.strip()
        if header and seq:
            data.append((header, seq))
    return data

def combine_data(amino_acids_str, foldseek_str):
    foldseek_str = foldseek_str.lower()
    sequence = ''
    for i in range(len(foldseek_str)):
        sequence += amino_acids_str[i]+foldseek_str[i]
    return sequence

def load_model():
    print('Loading SaProt model...')
    tokenizer = AutoTokenizer.from_pretrained("westlake-repl/SaProt_650M_PDB")
    model = AutoModelForMaskedLM.from_pretrained("westlake-repl/SaProt_650M_PDB")
    return model, tokenizer

def tokenize_sequences(data, tokenizer,device):
    print('Tokenizing sequences...')
    tokens = tokenizer(data, return_tensors="pt")
    tokens = {k: v.to(device) for k, v in tokens.items()}
    return tokens

def process_sequences(model, tokens):
    print('Processing sequences...')
    with torch.no_grad():
        outputs = model(**tokens)
    logits = outputs['logits'][0]
    return logits.cpu().numpy().astype(np.float128)

def standardize_vocab(tokenizer,nplogits,output_prefix):
    amino_acids = ['A', 'R', 'N', 'D', 'C', 'Q', 'E', 'G', 'H', 'I', 'L', 'K', 'M', 'F', 'P', 'S', 'T', 'W', 'Y', 'V']
    ### Changing vocab by summing logits ###
    vocab = tokenizer.get_vocab()
    filtered_vocab = {token: index for token, index in vocab.items() if "<" not in token and "#" not in token} # remove special tokens

    new_nplogits = []
    for aa in amino_acids:
        aa_ls = []
        for key,item in filtered_vocab.items():
            if aa in key:
                aa_ls.append(item)
        new_nplogits.append(np.sum(nplogits[1:-1,aa_ls],axis=1))
    new_nplogits = np.array(new_nplogits).T
    
    np.save(f'{output_prefix}.logits.SaProt_650M_PDB.npy', new_nplogits)


def main():
    amino_acid_str = args.amino_acid_str
    foldseek_tokens_input = args.foldseek_tokens
    output_prefix = args.output_prefix
    device = args.device

    model, tokenizer = load_model()
    device = torch.device("cuda:"+device if torch.cuda.is_available() else "cpu")
    model = model.to(device)
    foldseek_str = get_data(foldseek_tokens_input)[0][1]
    data = combine_data(amino_acid_str, foldseek_str)
    batch_tokens = tokenize_sequences(data, tokenizer,device)

    nplogits = process_sequences(model, batch_tokens)
    standardize_vocab(tokenizer,nplogits,output_prefix)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Process amino acid and 3Di sequences using SaProt model.')
    parser.add_argument('--amino_acid_str', type=str, help='Amino acid sequence')
    parser.add_argument('--foldseek_tokens', type=str, help='Path to the amino acid fasta file')
    parser.add_argument('--output_prefix', type=str, help='Optional prefix to add to the output filename',default = '')
    parser.add_argument('--device', type=str, help='Specify the Cuda device index',default = '0')

    args = parser.parse_args()

    main(args)

