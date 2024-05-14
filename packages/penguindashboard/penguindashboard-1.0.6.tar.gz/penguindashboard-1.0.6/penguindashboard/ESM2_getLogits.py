from transformers import AutoTokenizer, AutoModelForMaskedLM
import torch
import numpy as np
import argparse

print("ESM started running.")

def load_model(model_choice):
    print('Loading ESM2 model...')
    if model_choice == 'esm2_t48_15B_UR50D':
        tokenizer = AutoTokenizer.from_pretrained("facebook/esm2_t48_15B_UR50D")
        model = AutoModelForMaskedLM.from_pretrained("facebook/esm2_t48_15B_UR50D")
        return model, tokenizer
    elif model_choice == 'esm2_t36_3B_UR50D':
        tokenizer = AutoTokenizer.from_pretrained("facebook/esm2_t36_3B_UR50D")
        model = AutoModelForMaskedLM.from_pretrained("facebook/esm2_t36_3B_UR50D")
        return model, tokenizer
    elif model_choice == 'esm2_t33_650M_UR50D':
        tokenizer = AutoTokenizer.from_pretrained("facebook/esm2_t33_650M_UR50D")
        model = AutoModelForMaskedLM.from_pretrained("facebook/esm2_t33_650M_UR50D")
        return model, tokenizer
    else:
        print(f"Invalid model choice: {model_choice}. Running with default model esm2_t33_650M_UR50D")
        tokenizer = AutoTokenizer.from_pretrained("facebook/esm2_t33_650M_UR50D")
        model = AutoModelForMaskedLM.from_pretrained("facebook/esm2_t33_650M_UR50D")
        return model, tokenizer

def tokenize_sequences(data, tokenizer, device):
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

def standardize_vocab(tokenizer,nplogits,model_choice,output_prefix):
    amino_acids = ['A', 'R', 'N', 'D', 'C', 'Q', 'E', 'G', 'H', 'I', 'L', 'K', 'M', 'F', 'P', 'S', 'T', 'W', 'Y', 'V']
    ### Changing vocab by summing logits ###
    vocab = tokenizer.get_vocab()
    filtered_vocab = {token: index for token, index in vocab.items() if token in amino_acids} # Saving only amino acid {token:index} pairs

    new_nplogits = []
    for aa in amino_acids:
        new_nplogits.append(nplogits[1:-1,filtered_vocab[aa]])
    new_nplogits = np.array(new_nplogits).T
    np.save(f'{output_prefix}.logits.{model_choice}.npy', new_nplogits)

def main():
    parser = argparse.ArgumentParser(description='Process sequences using ESM-2 model.')
    parser.add_argument('--sequence', type=str, help='Sequence to pass through ESM-2 model')
    parser.add_argument('--model_choice', type=str, help='Choice of ESM2 model. Options: [esm2_t48_15B_UR50D, esm2_t36_3B_UR50D, esm2_t33_650M_UR50D] Default: esm2_t33_650M_UR50D', default = 'esm2_t33_650M_UR50D')
    parser.add_argument('--output_prefix', type=str, help='Optional prefix to add to the output filename')
    parser.add_argument('--device', type=str, help='Specify the Cuda device index', default = '0')

    args = parser.parse_args()
    sequence = args.sequence
    model_choice = args.model_choice
    output_prefix = args.output_prefix
    device = args.device

    model, tokenizer = load_model(model_choice)
    device = torch.device(f"cuda:{device}" if torch.cuda.is_available() else "cpu")
    model = model.to(device)
    tokens = tokenize_sequences(sequence, tokenizer, device)

    nplogits = process_sequences(model, tokens)
    standardize_vocab(tokenizer,nplogits,model_choice,output_prefix)

if __name__ == "__main__":
    main()
