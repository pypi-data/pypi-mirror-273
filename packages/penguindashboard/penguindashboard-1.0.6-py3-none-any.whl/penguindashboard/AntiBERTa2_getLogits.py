from transformers import AutoTokenizer, AutoModelForMaskedLM
import torch
import numpy as np
import argparse

def load_model():
    print('Loading AntiBERTa2 model...')
    tokenizer = AutoTokenizer.from_pretrained("alchemab/antiberta2")
    model = AutoModelForMaskedLM.from_pretrained("alchemab/antiberta2")
    return model, tokenizer

def tokenize_sequences(data, tokenizer,device):
    print('Tokenizing sequences...')
    tokens = tokenizer(' '.join(data), return_tensors="pt",padding=True) # Expects spaces between amino acids
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
    np.save(f'{output_prefix}.logits.AntiBERTa2.npy', new_nplogits)

def main():
    parser = argparse.ArgumentParser(description='Process amino acid sequences using AntiBERTa2 model.')
    parser.add_argument('--amino_acid_str', type=str, help='Amino acid sequence')
    parser.add_argument('--output_prefix', type=str, help='Optional prefix to add to the output filename',default = '')
    parser.add_argument('--device', type=str, help='Specify the Cuda device index',default = '0')

    args = parser.parse_args()
    amino_acid_str = args.amino_acid_str
    output_prefix = args.output_prefix
    device = args.device

    model, tokenizer = load_model()
    device = torch.device("cuda:"+device if torch.cuda.is_available() else "cpu")
    model = model.to(device)
    batch_tokens = tokenize_sequences(amino_acid_str, tokenizer, device)

    nplogits = process_sequences(model, batch_tokens)
    standardize_vocab(tokenizer,nplogits,output_prefix)

if __name__ == "__main__":
    main()
    