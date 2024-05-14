import argparse
import requests

def main(args):
    # Input sequence
    prefix = f'{args.dir}/{args.name}'
    sequence = f'{args.sequence}'

    # Making a POST request to the ESMFold API
    url = "https://api.esmatlas.com/foldSequence/v1/pdb/"
    headers = {'Content-Type': 'text/plain'}
    pdb_str = requests.post(url, headers=headers, data=sequence, verify=False)  # `verify=False` ignores SSL certificate validation

    # Check if the request was successful
    if pdb_str.status_code == 200:
        with open(f"{prefix}.pdb", "w") as out:
            out.write(pdb_str.text)
        print(f"Output saved to {prefix}.pdb")
    else:
        print("Failed to retrieve data:", pdb_str.status_code)


if __name__ == '__main__':
    # argparsing
    parser = argparse.ArgumentParser(description='Fold a protein sequence using ESMFold API.')
    parser.add_argument('--name', type=str, help='ID in FASTA file')
    parser.add_argument('--sequence', type=str, help='Amino acid sequence to fold')
    parser.add_argument('--dir', type=str, help='Directory to save the output file')
    args = parser.parse_args()
    
    main(args)