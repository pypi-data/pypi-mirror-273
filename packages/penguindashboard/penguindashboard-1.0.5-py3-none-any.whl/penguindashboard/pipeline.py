
def main(args):
    import os
    import sys
    import subprocess
    
    script_dir = os.path.dirname(os.path.realpath(__file__))

    os.makedirs(args.output_dir, exist_ok=True)

    if not os.path.isfile(args.fasta_file):
        print(f"Error: The file {args.fasta_file} does not exist.")
        sys.exit(1)

    with open(args.fasta_file) as f:
        for line in f:
            if line.startswith('>'):
                name = line[1:].strip()
                break

    with open(args.fasta_file) as f:
        seq = ''.join(line.strip() for line in f if not line.startswith('>'))

    os.makedirs(args.output_dir, exist_ok=True)

    print(f"Running ESMFold for {name}")
    subprocess.run(f"python3 {script_dir}/esm_fold.py --sequence {seq} --name {name} --dir {args.output_dir}", shell=True)

    pdb_file = os.path.join(args.output_dir, f"{name}.pdb")

    ############### Running Models ###############
    print(f"Running models for {name}")

    if args.saprot:
        os.makedirs(f"{args.output_dir}/foldseek", exist_ok=True)
        subprocess.run(f"foldseek createdb \"{pdb_file}\" \"{args.output_dir}/foldseek/{name}\" -v 1", shell=True)
        subprocess.run(f"foldseek lndb \"{args.output_dir}/foldseek/{name}_h\" \"{args.output_dir}/foldseek/{name}_ss_h\" -v 1", shell=True)
        subprocess.run(f"foldseek convert2fasta \"{args.output_dir}/foldseek/{name}_ss\" \"{args.output_dir}/foldseek/{name}_ss.fasta\" -v 1", shell=True)
        print("Running SaProt...")
        subprocess.run(f"python3 {script_dir}/SaProt_getLogits.py --amino_acid_str \"{seq}\" --foldseek_tokens \"{args.output_dir}/foldseek/{name}_ss.fasta\" --output_prefix \"{args.output_dir}/{name}\" --device \"{args.device}\"", shell=True)

    if args.antiberta:
        print("Running AntiBERTa2...")
        subprocess.run(f"python3 {script_dir}/AntiBERTa2_getLogits.py --amino_acid_str \"{seq}\" --output_prefix \"{args.output_dir}/{name}\" --device \"{args.device}\"", shell=True)

    if args.esm:
        print("Running ESM2 (650M)...")
        subprocess.run(f"python3 {script_dir}/ESM2_getLogits.py --sequence \"{seq}\" --model_choice esm2_t33_650M_UR50D --output_prefix \"{args.output_dir}/{name}\" --device \"{args.device}\"", shell=True)

    if args.proteinmpnn:
        proteinmpnn_dir = os.path.join(args.output_dir, "../LigandMPNN")
        if not os.path.isdir(proteinmpnn_dir):
            print("Setting up ProteinMPNN...")
            subprocess.run(f"git clone https://github.com/dauparas/LigandMPNN.git \"{proteinmpnn_dir}\"", shell=True)
            os.makedirs(f"{proteinmpnn_dir}/model_params", exist_ok=True)
            subprocess.run(f"wget https://github.com/dauparas/ProteinMPNN/raw/main/vanilla_model_weights/v_48_020.pt -P \"{proteinmpnn_dir}/model_params\"", shell=True)
            subprocess.run(f"cp \"{script_dir}/score.py\" \"{proteinmpnn_dir}/score.py\"", shell=True)
        else:
            print("ProteinMPNN already set up.")

        print("Running ProteinMPNN...")
        subprocess.run(f"python3 {script_dir}/ProteinMPNN_getLogits.py --output_prefix \"{args.output_dir}\" --proteinmpnn_dir {proteinmpnn_dir} --pdb_file \"{pdb_file}\" --device \"{args.device}\"", shell=True)

    if args.blast:
        print("Running BLAST phylogeny...")
        subprocess.run(f"python3 {script_dir}/BLAST_phylo.py --outdir \"{args.output_dir}\" --sequence \"{seq}\" --name \"{name}\"", shell=True)


    ### MUTCOMPUTE SECITON ###
    if args.mutcompute:
        print("Running MutCompute...")
        docker_command = (
        f"docker run --rm -v $(pwd)/{args.output_dir}:/mutcompute/input "
        f"aaronfeller/penguin "
        f"-c 'cd scripts && python run.py -p {name}.pdb -d ../input/ > ../input/{name}.mutcompute.txt'"
        )
        
        # Execute the Docker command
        subprocess.run(docker_command, shell=True)

        print("Editing MutCompute output...")
        subprocess.run(f"python {script_dir}/edit_mutcompute_output.py --output {args.output_dir} --name {name}", shell=True)

    print(f"Predictions complete for {name}")

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Process a FASTA file and run a sequence analysis pipeline.")
    parser.add_argument("fasta_file", type=str, help="Path to the input FASTA file.")
    parser.add_argument("output_dir", type=str, help="Path to the output directory.")
    parser.add_argument("--device", type=str, default="0", help="CUDA device number (default: 0)")
    parser.add_argument("--saprot", type=bool, default="True", help="Run SaProt")
    parser.add_argument("--esm", type=bool, default="True", help="Run ESM2")
    parser.add_argument("--proteinmpnn", type=bool, default="True", help="Run ProteinMPNN")
    parser.add_argument("--blast", type=bool, default="True", help="Run BLAST phylogeny")
    parser.add_argument("--mutcompute", type=bool, default="True", help="Run MutCompute")
    parser.add_argument("--antiberta", type=bool, default="False", help="Run AntiBERTa2")    
    args = parser.parse_args()
    main(args)
